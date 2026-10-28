"""M2 tests: fusion, retrievers, citation mapping, abstention paths and the API path guard.

No llama-server needed: the LLM chain is replaced by a fake. Indexes are built in temp folders.
"""

import shutil

import pytest
from fastapi.testclient import TestClient
from langchain_core.runnables import RunnableLambda

from notecabinet import config
from notecabinet.ask import NOT_FOUND, Asker, parse_citations
from notecabinet.index import build_index, find_notes
from notecabinet.retrieve import RETRIEVERS, Index, Reranker, make_retriever, rrf


@pytest.fixture(scope="module")
def small_index(tmp_path_factory):
    folder = tmp_path_factory.mktemp("notes")
    for p in find_notes(config.BENCHMARK_NOTES_DIR)[:12]:
        shutil.copy(p, folder / p.name)
    db_path = folder.parent / "small.db"
    build_index(folder, db_path)
    return folder, Index(db_path)


@pytest.fixture(scope="module")
def reranker():
    return Reranker()


def fake_asker(index, reranker, reply, threshold=0.0):
    asker = Asker(index=index, reranker=reranker, threshold=threshold)
    calls = []
    asker.chain = RunnableLambda(lambda inp: calls.append(inp) or reply)
    return asker, calls


# ---------------------------------------------------------------- fusion + retrievers

def test_rrf_rewards_agreement_and_uses_ranks_only():
    a = [(1, 99.0), (2, 50.0), (3, 1.0)]       # wildly different score scales...
    b = [(3, 0.9), (1, 0.8), (4, 0.1)]
    fused = dict(rrf([a, b], k=10, rrf_k=60))
    assert fused[1] == pytest.approx(1 / 61 + 1 / 62)  # ...only ranks matter
    assert next(iter(fused)) == 1  # near the top of both lists -> ranked first
    assert 4 in fused and len(rrf([a, b], k=2)) == 2


@pytest.mark.parametrize("name", RETRIEVERS)
def test_retrievers_return_k_documents_with_exact_spans(small_index, reranker, name):
    folder, index = small_index
    docs = make_retriever(name, index, reranker).invoke("what did PFOX say in our 1:1?")
    assert len(docs) == config.FINAL_K
    for d in docs:
        raw = (folder / d.metadata["path"]).read_bytes().decode("utf-8")
        assert raw[d.metadata["start"]:d.metadata["end"]] == d.page_content


def test_rerank_retriever_orders_by_rerank_score(small_index, reranker):
    _, index = small_index
    docs = make_retriever("hybrid+rerank", index, reranker).invoke("office hours schedule")
    scores = [d.metadata["rerank_score"] for d in docs]
    assert scores == sorted(scores, reverse=True)


@pytest.mark.parametrize("question", ['what "is" this?', "a OR b AND NOT c", "(*)", "-- ; DROP TABLE chunks", "???"])
def test_bm25_survives_fts_syntax_in_questions(small_index, question):
    _, index = small_index
    index.bm25(question, 5)  # must not raise an FTS5 syntax error


# ---------------------------------------------------------------- citations + abstention

def test_parse_citations_maps_valid_numbers_and_flags_invalid_ones():
    docs = ["d1", "d2", "d3"]
    cited, invalid = parse_citations("A [2]. B [1, 3]. Again [2]. Bad [7] [0].", docs)
    assert [n for n, _ in cited] == [2, 1, 3]
    assert [d for _, d in cited] == ["d2", "d1", "d3"]
    assert invalid == [7, 0]


def test_answer_citations_carry_path_and_exact_span(small_index, reranker):
    folder, index = small_index
    asker, calls = fake_asker(index, reranker, "It was discussed [1] and later [2].")
    r = asker.ask("what happened at the lab meeting?", "hybrid")
    assert not r["abstained"] and len(calls) == 1
    assert [c["n"] for c in r["citations"]] == [1, 2]
    for c in r["citations"]:
        raw = (folder / c["path"]).read_bytes().decode("utf-8")
        assert raw[c["start"]:c["end"]] == c["text"]
    assert set(r["timings"]) == {"retrieval_ms", "rerank_ms", "generation_ms"}


def test_model_not_found_abstains(small_index, reranker):
    _, index = small_index
    asker, _ = fake_asker(index, reranker, "NOT_FOUND")
    r = asker.ask("what is my favourite colour?", "bm25")
    assert (r["answer"], r["abstained"], r["abstain_reason"]) == (NOT_FOUND, True, "model")


def test_low_rerank_score_abstains_without_calling_the_llm(small_index, reranker):
    _, index = small_index
    asker, calls = fake_asker(index, reranker, "should not be used", threshold=1.01)  # above any possible score
    r = asker.ask("anything", "dense")
    assert (r["abstained"], r["abstain_reason"], calls) == (True, "low_rerank_score", [])


def test_every_retriever_gets_rerank_scores_for_the_threshold(small_index, reranker):
    _, index = small_index
    asker, _ = fake_asker(index, reranker, "x [1]")
    for name in RETRIEVERS:
        docs, _ = asker.retrieve("deadline", name)
        assert all("rerank_score" in d.metadata for d in docs)


# ---------------------------------------------------------------- API

@pytest.fixture
def api_client(monkeypatch, tmp_path):
    from notecabinet import api
    monkeypatch.setattr(config, "INDEX_PATH", tmp_path / "none.db")    # no index: /ask must say so
    monkeypatch.setattr(api, "notes_dir", lambda: config.BENCHMARK_NOTES_DIR)  # serve the repo's notes read-only
    return TestClient(api.app)


def test_api_lists_and_returns_notes(api_client):
    notes = api_client.get("/notes").json()
    assert len(notes) == len(find_notes(config.BENCHMARK_NOTES_DIR))
    first = notes[0]["path"]
    raw = api_client.get(f"/notes/{first}").json()["raw"]
    assert raw == (config.BENCHMARK_NOTES_DIR / first).read_bytes().decode("utf-8")


@pytest.mark.parametrize("path", ["../CLAUDE.md", "..%2F..%2F.env", "%2e%2e/%2e%2e/.env", "/etc/passwd",
                                  "../../pyproject.toml", "nope.md", "../data/bible.md"])
def test_api_refuses_paths_outside_the_notes_folder(api_client, path):
    assert api_client.get(f"/notes/{path}").status_code == 404


def test_api_notes_without_index_is_503(monkeypatch, tmp_path):
    from notecabinet import api
    monkeypatch.setattr(config, "INDEX_PATH", tmp_path / "none.db")
    assert TestClient(api.app).get("/notes").status_code == 503


def test_api_ask_without_index_is_503(api_client):
    assert api_client.post("/ask", json={"question": "hello"}).status_code == 503


def test_api_rejects_unknown_retriever(api_client):
    assert api_client.post("/ask", json={"question": "x", "retriever": "magic"}).status_code == 422
