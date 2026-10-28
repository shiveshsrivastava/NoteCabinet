"""One-time model download for a source checkout: embedder + reranker into the Hugging Face cache,
and the Qwen GGUF into models/ for llama-server.

Same as `notecabinet download-models --with-llm --llm-dir models`; the logic lives in
notecabinet/models.py so installed users get it too.
"""

from notecabinet import config
from notecabinet.models import download_models

if __name__ == "__main__":
    download_models(with_llm=True, llm_dir=config.ROOT / "models")
