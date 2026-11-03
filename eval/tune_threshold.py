"""Tune the abstention threshold on the DEV split only (never the test split).

For each dev question: retrieve with hybrid+rerank, record the top reranker score, and ask the
model with no threshold (so we know when it abstains on its own). Then try every threshold that
falls between two observed scores; final behaviour = abstain if score < t OR the model said
NOT_FOUND. Pick the threshold with the most correct abstain/answer decisions; ties go to the
midpoint of the widest tied interval (the most margin on both sides).

Writes results/<timestamp>-tune-threshold/: config.json, summary.md, raw/per_question.jsonl.
Usage: uv run python eval/tune_threshold.py
"""

import json

from eval.common import load_qa, new_run_dir, require_benchmark_index, run_config, sha256_text
from notecabinet import config
from notecabinet.ask import SYSTEM_PROMPT, USER_PROMPT, Asker

RETRIEVER = "hybrid+rerank"


def decisions(rows, t):
    """Correct decisions at threshold t: abstain on unanswerable, answer on answerable."""
    correct = 0
    for r in rows:
        abstain = r["top_rerank_score"] < t or r["model_abstained"]
        correct += abstain == r["unanswerable"]
    return correct


def main():
    dev = [q for q in load_qa() if q["split"] == "dev"]
    require_benchmark_index()
    asker = Asker(threshold=None)
    asker.ask("warm-up question")

    rows = []
    for q in dev:
        a = asker.ask(q["question"], RETRIEVER)
        rows.append({"id": q["id"], "type": q["type"], "unanswerable": q["type"] == "unanswerable",
                     "top_rerank_score": a["top_rerank_score"], "model_abstained": a["abstained"],
                     "answer": a["answer"], "gold": q["answer"],
                     "source_in_top5": bool(set(q["source_notes"]) & {s["path"] for s in a["sources"]}),
                     "timings": a["timings"]})
        print(f"{q['id']} {q['type']:12} score {a['top_rerank_score']:.3f}  model abstained: {a['abstained']}")

    scores = sorted({0.0, 1.0, *(r["top_rerank_score"] for r in rows)})
    intervals = list(zip(scores, scores[1:]))            # every threshold inside one interval acts the same
    graded = [(decisions(rows, (lo + hi) / 2), hi - lo, lo, hi) for lo, hi in intervals]
    best_correct = max(g[0] for g in graded)
    _, width, lo, hi = max(g for g in graded if g[0] == best_correct)  # widest tied interval
    threshold = round((lo + hi) / 2, 4)

    out = new_run_dir("tune-threshold")
    (out / "raw" / "per_question.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))

    cfg = run_config(
        task="tune abstention threshold", split="dev", n_questions=len(rows),
        n_unanswerable=sum(r["unanswerable"] for r in rows), retriever=RETRIEVER,
        chosen_threshold=threshold, best_correct=best_correct, tied_interval=[lo, hi],
        prompt_sha256={"system": sha256_text(SYSTEM_PROMPT), "user": sha256_text(USER_PROMPT)},
    )
    (out / "config.json").write_text(json.dumps(cfg, indent=2) + "\n")

    lines = [f"# Abstention threshold tuning (dev split, {len(rows)} questions, "
             f"{cfg['n_unanswerable']} unanswerable)", "",
             f"Retriever: `{RETRIEVER}`. Chosen threshold: **{threshold}** "
             f"({best_correct}/{len(rows)} correct abstain/answer decisions; any value in "
             f"[{lo:.4f}, {hi:.4f}) behaves the same on dev).", "",
             "| threshold interval | correct decisions |", "|---|---|"]
    lines += [f"| [{low:.4f}, {high:.4f}) | {c}/{len(rows)} ({c / len(rows):.0%}) |" for c, _, low, high in graded]
    lines += ["", "| id | type | top rerank score | model abstained | source note in top 5 |", "|---|---|---|---|---|"]
    lines += [f"| {r['id']} | {r['type']} | {r['top_rerank_score']:.3f} | {r['model_abstained']} | "
              f"{'n/a' if r['unanswerable'] else r['source_in_top5']} |" for r in rows]
    (out / "summary.md").write_text("\n".join(lines) + "\n")
    print(f"\nchosen threshold {threshold} ({best_correct}/{len(rows)} correct) -> {out.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
