"""Shared test setup.

Tests that use a fixture which loads the bge embedder/reranker are marked `models` automatically and
skipped, with a clear reason, if the weights aren't downloaded (`notecabinet download-models`).
No test needs llama-server: LLM calls are replaced by a fake chain (see test_retrieve_ask.py).
"""

from pathlib import Path

import pytest

from notecabinet import config as nc

# The repo's benchmark notes, located from the tests folder (not from the package, which may be an
# installed wheel in site-packages). Tests only ever read these.
BENCHMARK_NOTES = Path(__file__).resolve().parent.parent / "data" / "notes"

# Fixtures whose setup loads model weights (tokenizer, embedder or reranker).
MODEL_FIXTURES = {"splitter", "full_index", "small_index", "reranker", "small_notes"}


def _weights_cached():
    from huggingface_hub import try_to_load_from_cache

    for repo, rev in ((nc.EMBEDDER, nc.EMBEDDER_REVISION), (nc.RERANKER, nc.RERANKER_REVISION)):
        if not isinstance(try_to_load_from_cache(repo, "config.json", revision=rev), str):
            return False
    return True


def pytest_collection_modifyitems(config, items):
    have_weights = _weights_cached()
    skip = pytest.mark.skip(reason="model weights not downloaded; run `notecabinet download-models`")
    for item in items:
        if MODEL_FIXTURES & set(getattr(item, "fixturenames", ())):
            item.add_marker(pytest.mark.models)
            if not have_weights:
                item.add_marker(skip)
