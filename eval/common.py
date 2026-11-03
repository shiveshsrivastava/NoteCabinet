"""What every eval run shares: loading the QA set, checking the index, and recording a reproducible config.

Each run writes results/<timestamp>-<name>/ with a config.json built from run_config(), so every number
can be traced back to the models, settings, prompts, data and git commit that produced it.
"""

import hashlib
import json
import subprocess
from datetime import datetime

from notecabinet import config
from notecabinet.index import stored_notes_dir

RESULTS = config.ROOT / "results"
EVAL_DATA = config.ROOT / "data" / "eval"


def load_qa():
    return [json.loads(line) for line in (EVAL_DATA / "qa.jsonl").read_text().splitlines() if line.strip()]


def require_benchmark_index():
    """Refuse to run on an index built from any folder other than the benchmark notes."""
    built_from = stored_notes_dir(config.INDEX_PATH)
    if built_from is None or built_from.resolve() != config.BENCHMARK_NOTES_DIR.resolve():
        raise SystemExit(f"the index at {config.INDEX_PATH} must be built from the benchmark notes first:\n"
                         f"  notecabinet index {config.BENCHMARK_NOTES_DIR.relative_to(config.ROOT)}")


def new_run_dir(name):
    """results/<timestamp>-<name>/ with an empty raw/ folder (raw/ is gitignored)."""
    out = RESULTS / f"{datetime.now().strftime('%Y-%m-%d_%H%M%S')}-{name}"
    (out / "raw").mkdir(parents=True)
    return out


def sha256_files(paths):
    h = hashlib.sha256()
    for p in sorted(paths):
        h.update(str(p.relative_to(config.ROOT)).encode() + p.read_bytes())
    return h.hexdigest()


def sha256_text(text):
    return hashlib.sha256(text.encode()).hexdigest()


def git_state():
    def run(*a):
        return subprocess.run(["git", *a], cwd=config.ROOT, capture_output=True, text=True).stdout.strip()

    return {"commit": run("rev-parse", "HEAD"), "dirty": bool(run("status", "--porcelain", "--untracked-files=no"))}


def run_config(**fields):
    """config.json contents: the caller's fields, then models, sampling, retrieval settings, git and data hashes."""
    eval_files = [p for p in EVAL_DATA.rglob("*") if p.is_file() and ".gen_cache" not in p.parts]
    return {
        **fields,
        "models": {"llm": f"models/{config.LLM_FILE}", "embedder": config.EMBEDDER,
                   "embedder_revision": config.EMBEDDER_REVISION, "reranker": config.RERANKER,
                   "reranker_revision": config.RERANKER_REVISION},
        "sampling": {"temperature": 0, "seed": config.SEED, "max_tokens": config.LLM_MAX_TOKENS,
                     "cache_prompt": False, "llama_server_parallel": 1},
        "retrieval": {"final_k": config.FINAL_K, "rerank_candidates": config.RERANK_CANDIDATES, "rrf_k": config.RRF_K},
        "git": git_state(), "data_eval_sha256": sha256_files(eval_files),
        "notes_sha256": sha256_files(list(config.BENCHMARK_NOTES_DIR.rglob("*.md"))),
    }
