"""Ask evaluation: retrieval quality, answer quality and abstention for every retriever, plus latency.

Two passes, so a judge problem never throws away the slow local generation:
  1. generate: one warm-up query, then every retriever x every question of the split. Each answer, its
     chunks, rerank scores, timings and retrieval metrics go to raw/answers.jsonl as soon as they exist.
  2. judge: grade the answers with the Claude judge (eval/judge.py) -> raw/per_question.jsonl, then
     write metrics.json and summary.md (eval/report.py). If judging fails part-way, re-run this pass
     alone with --rejudge RUN_DIR (cached verdicts cost nothing).

What gets judged:
  - answerable, answered:      correctness + faithfulness
  - answerable, abstained:     incorrect (no judge call); faithfulness n/a
  - unanswerable, answered:    incorrect by definition (no judge call); faithfulness judged
  - unanswerable, abstained:   nothing to judge (abstention metrics cover it)

Usage: uv run --env-file .env python -m eval.eval_ask [--split test|dev] [--retrievers bm25 dense ...]
"""

import argparse
import json
import time
from pathlib import Path

from eval.common import EVAL_DATA, load_qa, new_run_dir, require_benchmark_index, run_config, sha256_text
from eval.judge import Judge, JudgeError, prompt_hashes
from eval.metrics import notes_by_fact, retrieval_metrics
from eval.report import write_report
from notecabinet import config
from notecabinet.ask import SYSTEM_PROMPT, USER_PROMPT, Asker, format_excerpts
from notecabinet.retrieve import RETRIEVERS

WARMUP_QUESTION = "What did I work on this week?"


def check_llm():
    import urllib.request

    try:
        urllib.request.urlopen(f"{config.LLM_URL}/health", timeout=5)
    except OSError as e:  # URLError, HTTPError and refused connections are all OSErrors
        raise SystemExit(f"llama-server is not answering at {config.LLM_URL} ({e}); start it first (see CLAUDE.md)")


def excerpts_for(asker, sources):
    """The exact excerpt text the model was shown, rebuilt from the index (same chunks, same order)."""
    return format_excerpts(asker.index.documents([(s["chunk_id"], s["retrieval_score"]) for s in sources]))


def generate(asker, questions, retrievers, fact_notes, out_path):
    rows = []
    with out_path.open("w") as f:
        for retriever in retrievers:
            for q in questions:
                a = asker.ask(q["question"], retriever)
                unanswerable = q["type"] == "unanswerable"
                paths = [s["path"] for s in a["sources"]]
                row = {
                    "id": q["id"], "type": q["type"], "split": q["split"], "retriever": retriever,
                    "unanswerable": unanswerable, "question": q["question"], "gold": q["answer"],
                    "fact_ids": q["fact_ids"], "answer": a["answer"], "abstained": a["abstained"],
                    "abstain_reason": a["abstain_reason"], "top_rerank_score": a["top_rerank_score"],
                    "retrieved_paths": paths, "chunk_ids": [s["chunk_id"] for s in a["sources"]],
                    "rerank_scores": [s["rerank_score"] for s in a["sources"]],
                    "citations": [c["n"] for c in a["citations"]], "invalid_citations": a["invalid_citations"],
                    "excerpts": excerpts_for(asker, a["sources"]),
                    "retrieval": None if unanswerable else retrieval_metrics(q["fact_ids"], paths, fact_notes),
                    "timings": a["timings"],
                }
                rows.append(row)
                f.write(json.dumps(row) + "\n")
                f.flush()
                status = f"abstained ({a['abstain_reason']})" if a["abstained"] else "answered"
                print(f"{retriever:14} {q['id']} {q['type']:12} {status}")
    return rows


def judge_row(judge, row):
    """Verdict fields for one answer, following the rules in the module docstring."""
    out = {"correct": None, "faithful": None, "judge": {}}
    if row["abstained"]:
        if not row["unanswerable"]:
            out["correct"] = False
        return out
    if row["unanswerable"]:
        out["correct"] = False
    else:
        v = judge.grade("correctness", question=row["question"], gold=row["gold"], answer=row["answer"])
        out["correct"] = v["verdict"] == "correct"
        out["judge"]["correctness"] = v
    v = judge.grade("faithfulness", excerpts=row["excerpts"], question=row["question"], answer=row["answer"])
    out["faithful"] = v["verdict"] == "faithful"
    out["judge"]["faithfulness"] = v
    return out


def judge_all(judge, rows, out_path):
    judged, errors = [], 0
    for row in rows:
        try:
            verdict = judge_row(judge, row)
        except JudgeError as e:  # recorded, not fatal: the summary counts these
            verdict = {"correct": None, "faithful": None, "judge": {}, "judge_error": str(e)}
            errors += 1
            print(f"judge error on {row['retriever']} {row['id']}: {e}")
        judged.append({**row, **verdict})
    out_path.write_text("".join(json.dumps(r) + "\n" for r in judged))
    calls = sum(not v.get("cached", True) for r in judged for v in r["judge"].values())
    print(f"judged {len(judged)} answers: {calls} new judge calls, {errors} judge errors")
    return judged


def load_kinds():
    return json.loads((EVAL_DATA / "unanswerable_kind.json").read_text())


def judge_and_report(judge, rows, out):
    judged = judge_all(judge, rows, out / "raw" / "per_question.jsonl")
    cfg = json.loads((out / "config.json").read_text())
    write_report(out, judged, cfg, load_kinds())
    print(f"-> {out.relative_to(config.ROOT)}/summary.md")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="notecabinet eval ask", description=__doc__.split("\n")[0])
    parser.add_argument("--split", default="test", choices=["test", "dev"])
    parser.add_argument("--retrievers", nargs="+", default=list(RETRIEVERS), choices=RETRIEVERS)
    parser.add_argument("--rejudge", type=Path, help="re-run only the judge pass on an existing run folder")
    args = parser.parse_args(argv)

    judge = Judge()  # fails fast if JUDGE_MODEL is missing, before any slow generation
    if args.rejudge:
        out = args.rejudge.resolve()
        rows = [json.loads(line) for line in (out / "raw" / "answers.jsonl").read_text().splitlines()]
        judge_and_report(judge, rows, out)
        return out

    require_benchmark_index()
    check_llm()
    questions = [q for q in load_qa() if q["split"] == args.split]
    fact_notes = notes_by_fact(json.loads((EVAL_DATA / "note_facts.json").read_text()))

    out = new_run_dir(f"eval-ask-{args.split}")
    cfg = run_config(
        task="eval ask", split=args.split, n_questions=len(questions),
        n_unanswerable=sum(q["type"] == "unanswerable" for q in questions), retrievers=args.retrievers,
        abstain_threshold=config.ABSTAIN_THRESHOLD, judge={"model": judge.model, "effort": "medium"},
        prompt_sha256={"ask_system": sha256_text(SYSTEM_PROMPT), "ask_user": sha256_text(USER_PROMPT),
                       **{f"judge_{k}": h for k, h in prompt_hashes().items()}},
        warmup_question=WARMUP_QUESTION,
    )
    (out / "config.json").write_text(json.dumps(cfg, indent=2) + "\n")

    asker = Asker()
    t = time.perf_counter()
    asker.ask(WARMUP_QUESTION)  # loads the embedder/reranker onto the GPU and warms llama-server; not timed
    print(f"warm-up {time.perf_counter() - t:.1f}s")

    rows = generate(asker, questions, args.retrievers, fact_notes, out / "raw" / "answers.jsonl")
    judge_and_report(judge, rows, out)
    return out


if __name__ == "__main__":
    main()
