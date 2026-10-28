"""One-time model download: the only time the app's models touch the network.

The embedder and reranker go into the Hugging Face cache (the app then loads them with
HF_HUB_OFFLINE=1). Optionally the LLM GGUF is downloaded for llama-server. Revisions are pinned
in config, so every run uses exactly the same weights.

Importing notecabinet sets HF_HUB_OFFLINE=1, and huggingface_hub reads that once when it is first
imported. So the download runs in a child process started with HF_HUB_OFFLINE=0, and a second
child process checks that both models load offline.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

from notecabinet import config

SKIP = ["*.bin", "onnx/*", "*.onnx"]  # both repos ship model.safetensors; skip duplicate weights


def download_models(with_llm=False, llm_dir=None):
    """Download (online child process), then verify offline loading (offline child process)."""
    fetch = [sys.executable, "-m", "notecabinet.models", "--fetch"]
    if with_llm:
        fetch += ["--llm-dir", str(llm_dir or config.DATA_HOME / "models")]
    subprocess.run(fetch, env={**os.environ, "HF_HUB_OFFLINE": "0"}, check=True)
    subprocess.run([sys.executable, "-m", "notecabinet.models", "--verify"],
                   env={**os.environ, "HF_HUB_OFFLINE": "1"}, check=True)


def _fetch(llm_dir):
    from huggingface_hub import hf_hub_download, snapshot_download

    for repo, rev in ((config.EMBEDDER, config.EMBEDDER_REVISION), (config.RERANKER, config.RERANKER_REVISION)):
        print(f"downloading {repo}@{rev[:8]}", flush=True)
        snapshot_download(repo, revision=rev, ignore_patterns=SKIP)
    if llm_dir:
        print(f"downloading {config.LLM_REPO}/{config.LLM_FILE}@{config.LLM_REVISION[:8]} -> {llm_dir}", flush=True)
        path = Path(hf_hub_download(config.LLM_REPO, config.LLM_FILE, revision=config.LLM_REVISION, local_dir=llm_dir))
        print(f"  {path} ({path.stat().st_size / 2**30:.2f} GiB)", flush=True)


def _verify():
    from sentence_transformers import CrossEncoder, SentenceTransformer

    emb = SentenceTransformer(config.EMBEDDER, revision=config.EMBEDDER_REVISION, device="cpu")
    rr = CrossEncoder(config.RERANKER, revision=config.RERANKER_REVISION, device="cpu")
    score = float(rr.predict([("what is bm25", "bm25 is a ranking function")])[0])
    print(f"offline check ok: embedder dim {emb.get_embedding_dimension()}, reranker score {score:.3f}", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--llm-dir")
    a = ap.parse_args()
    if a.fetch:
        _fetch(a.llm_dir)
    if a.verify:
        _verify()
