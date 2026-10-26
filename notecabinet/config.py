"""NoteCabinet settings, in one place.

Importing this module also applies the offline guards, so it must be imported
before anything that loads Hugging Face models or LangChain (notecabinet/__init__.py
does this for you).
"""

import os
from pathlib import Path

# ---- offline guards (read by the libraries at import time) ----
# Models load from the local cache only. setdefault: can still be overridden from the shell.
os.environ.setdefault("HF_HUB_OFFLINE", "1")
# LangSmith tracing would send notes to the cloud. Always off, not overridable.
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGSMITH_TRACING"] = "false"

# ---- paths ----
ROOT = Path(__file__).resolve().parent.parent
NOTES_DIR = ROOT / "data" / "notes"
INDEX_PATH = ROOT / "index" / "notes.db"

# ---- models (revisions pinned to what scripts/download_models.py fetched) ----
EMBEDDER = "BAAI/bge-small-en-v1.5"
EMBEDDER_REVISION = "5c38ec7c405ec4b44b94cc5a9bb96e735b38267a"
EMBEDDING_DIM = 384
RERANKER = "BAAI/bge-reranker-base"
RERANKER_REVISION = "2cfc18c9415c912f9d8155881c133215df768a70"

# ---- chunking ----
CHUNK_TOKENS = 300   # counted with the embedder's tokenizer
CHUNK_OVERLAP = 40
CHUNKER_VERSION = 1  # bump when chunking or context_text() changes; forces a full re-index

# ---- retrieval ----
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "  # bge: queries only, not chunks
FINAL_K = 5             # chunks handed to the LLM
RERANK_CANDIDATES = 30  # hybrid+rerank: candidates the cross-encoder chooses from
RRF_K = 60              # Reciprocal Rank Fusion constant

# ---- local LLM ----
LLM_URL = os.environ.get("LLM_URL", "http://localhost:8080")
SEED = 42             # with temperature 0 and llama-server --parallel 1: repeatable answers
LLM_MAX_TOKENS = 400

# ---- abstention ----
# Answer NOT_FOUND when the best reranker score among the final chunks is below this.
# Tuned on the dev split only (10 questions, 2 unanswerable) by eval/tune_threshold.py:
# results/2026-10-25_224256-tune-threshold/ (9/10 correct decisions; any value in [0, 0.0202) is equivalent).
# Low on purpose: on dev, unanswerable questions score mid-range, so a higher gate only rejects answerable ones.
ABSTAIN_THRESHOLD = 0.0101
