"""Tune the abstention threshold on the DEV split only (never the test split).

For each dev question: retrieve with hybrid+rerank, record the top reranker score, and ask the
model with no threshold (so we know when it abstains on its own). Then try every threshold that
falls between two observed scores; final behaviour = abstain if score < t OR the model said
NOT_FOUND. Pick the threshold with the most correct abstain/answer decisions; ties go to the
midpoint of the widest tied interval (the most margin on both sides).

Writes results/<timestamp>-tune-threshold/: config.json, summary.md, raw/per_question.jsonl.
Usage: uv run python eval/tune_threshold.py
"""

import hashlib
import json
import subprocess
from datetime import datetime
from pathlib import Path

from notecabinet import config
from notecabinet.ask import SYSTEM_PROMPT, USER_PROMPT, Asker
from notecabinet.index import stored_notes_dir

RETRIEVER = "hybrid+rerank"
RESULTS = config.ROOT / "results"


def sha256_files(paths):
    h = hashlib.sha256()
    for p in sorted(paths):
        h.update(str(p.relative_to(config.ROOT)).encode() + p.read_bytes())
    return h.hexdigest()


def git_state():
    run = lambda *a: subprocess.run(["git", *a], cwd=config.ROOT, capture_output=True, text=True).stdout.strip()
    return {"commit": run("rev-parse", "HEAD"), "dirty": bool(run("status", "--porcelain", "--untracked-files=no"))}


def decisions(rows, t):
    """Correct decisions at threshold t: abstain on unanswerable, answer on answerable."""
    correct = 0
    for r in rows:
        abstain = r["top_rerank_score"] < t or r["model_abstained"]
        correct += abstain == r["unanswerable"]
    return correct


def main():
    qa = [json.loads(l) for l in (config.ROOT / "data/eval/qa.jsonl").read_text().splitlines() if l.strip()]
    dev = [q for q in qa if q["split"] == "dev"]
    built_from = stored_notes_dir(config.INDEX_PATH)
    if built_from is None or built_from.resolve() != config.BENCHMARK_NOTES_DIR.resolve():
        raise SystemExit(f"the index at {config.INDEX_PATH} must be built from the benchmark notes first:\n"
                         f"  notecabinet index {config.BENCHMARK_NOTES_DIR.relative_to(config.ROOT)}")
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

    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    out = RESULTS / f"{stamp}-tune-threshold"
    (out / "raw").mkdir(parents=True)
    (out / "raw" / "per_question.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))

    eval_files = [p for p in (config.ROOT / "data/eval").rglob("*") if p.is_file() and ".gen_cache" not in p.parts]
    cfg = {
        "task": "tune abstention threshold", "split": "dev", "n_questions": len(rows),
        "n_unanswerable": sum(r["unanswerable"] for r in rows), "retriever": RETRIEVER,
        "models": {"llm": "models/Qwen3-4B-Instruct-2507-Q4_K_M.gguf", "embedder": config.EMBEDDER,
                   "embedder_revision": config.EMBEDDER_REVISION, "reranker": config.RERANKER,
                   "reranker_revision": config.RERANKER_REVISION},
        "sampling": {"temperature": 0, "seed": config.SEED, "max_tokens": config.LLM_MAX_TOKENS,
                     "cache_prompt": False, "llama_server_parallel": 1},
        "retrieval": {"final_k": config.FINAL_K, "rerank_candidates": config.RERANK_CANDIDATES, "rrf_k": config.RRF_K},
        "chosen_threshold": threshold, "best_correct": best_correct, "tied_interval": [lo, hi],
        "git": git_state(), "data_eval_sha256": sha256_files(eval_files),
        "notes_sha256": sha256_files(list(config.BENCHMARK_NOTES_DIR.rglob("*.md"))),
        "prompt_sha256": {"system": hashlib.sha256(SYSTEM_PROMPT.encode()).hexdigest(),
                          "user": hashlib.sha256(USER_PROMPT.encode()).hexdigest()},
    }
    (out / "config.json").write_text(json.dumps(cfg, indent=2) + "\n")

    lines = [f"# Abstention threshold tuning (dev split, {len(rows)} questions, "
             f"{cfg['n_unanswerable']} unanswerable)", "",
             f"Retriever: `{RETRIEVER}`. Chosen threshold: **{threshold}** "
             f"({best_correct}/{len(rows)} correct abstain/answer decisions; any value in "
             f"[{lo:.4f}, {hi:.4f}) behaves the same on dev).", "",
             "| threshold interval | correct decisions |", "|---|---|"]
    lines += [f"| [{l:.4f}, {h:.4f}) | {c}/{len(rows)} ({c / len(rows):.0%}) |" for c, _, l, h in graded]
    lines += ["", "| id | type | top rerank score | model abstained | source note in top 5 |", "|---|---|---|---|---|"]
    lines += [f"| {r['id']} | {r['type']} | {r['top_rerank_score']:.3f} | {r['model_abstained']} | "
              f"{'n/a' if r['unanswerable'] else r['source_in_top5']} |" for r in rows]
    (out / "summary.md").write_text("\n".join(lines) + "\n")
    print(f"\nchosen threshold {threshold} ({best_correct}/{len(rows)} correct) -> {out.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
