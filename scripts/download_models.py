"""One-time model download. The only time the app's models touch the network.

- Embedder and reranker go into the Hugging Face cache (loaded later with HF_HUB_OFFLINE=1).
- The LLM GGUF goes into models/ for llama-server.

Revisions are pinned so every eval run uses the exact same weights.
"""

import os
import subprocess
import sys
from pathlib import Path

from huggingface_hub import hf_hub_download, snapshot_download

EMBEDDER = ("BAAI/bge-small-en-v1.5", "5c38ec7c405ec4b44b94cc5a9bb96e735b38267a")
RERANKER = ("BAAI/bge-reranker-base", "2cfc18c9415c912f9d8155881c133215df768a70")
LLM_REPO, LLM_REVISION = "unsloth/Qwen3-4B-Instruct-2507-GGUF", "a06e946bb6b655725eafa393f4a9745d460374c9"
LLM_FILE = "Qwen3-4B-Instruct-2507-Q4_K_M.gguf"

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"

# Both repos ship model.safetensors; skip the duplicate .bin and ONNX weights.
SKIP = ["*.bin", "onnx/*", "*.onnx"]

# Run in a fresh process so HF_HUB_OFFLINE is set before huggingface_hub is imported.
OFFLINE_CHECK = f"""
from sentence_transformers import CrossEncoder, SentenceTransformer
emb = SentenceTransformer({EMBEDDER[0]!r}, revision={EMBEDDER[1]!r}, device="cpu")
print("embedder dim:", emb.get_embedding_dimension())
rr = CrossEncoder({RERANKER[0]!r}, revision={RERANKER[1]!r}, device="cpu")
print("reranker score:", float(rr.predict([("what is bm25", "bm25 is a ranking function")])[0]))
"""


def main():
    for repo, rev in (EMBEDDER, RERANKER):
        print(f"downloading {repo}@{rev[:8]}")
        snapshot_download(repo, revision=rev, ignore_patterns=SKIP)

    print(f"downloading {LLM_REPO}/{LLM_FILE}@{LLM_REVISION[:8]} -> {MODELS_DIR}")
    path = hf_hub_download(LLM_REPO, LLM_FILE, revision=LLM_REVISION, local_dir=MODELS_DIR)
    print(f"  {path} ({Path(path).stat().st_size / 2**30:.2f} GiB)")

    print("verifying embedder + reranker load with HF_HUB_OFFLINE=1")
    env = {**os.environ, "HF_HUB_OFFLINE": "1"}
    subprocess.run([sys.executable, "-c", OFFLINE_CHECK], env=env, check=True)
    print("done")


if __name__ == "__main__":
    main()
