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

# ---- local LLM ----
LLM_URL = os.environ.get("LLM_URL", "http://localhost:8080")
