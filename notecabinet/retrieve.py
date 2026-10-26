"""Retrieval over the SQLite index: bm25, dense, hybrid (RRF) and hybrid+rerank.

Each retriever is a LangChain BaseRetriever returning Documents whose metadata carries the
chunk's path and raw-file span. The cross-encoder reranker is a separate step so evals can
time it on its own; for the non-rerank retrievers it only *scores* the final chunks (so one
abstention threshold works across all four), for hybrid+rerank it also reorders them.
"""

import re
import threading

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from pydantic import ConfigDict

from notecabinet import config, db
from notecabinet.index import context_text

RETRIEVERS = ("bm25", "dense", "hybrid", "hybrid+rerank")


class Index:
    """Read access to the index, plus the embedder for queries. Safe to share across threads."""

    def __init__(self, db_path=config.INDEX_PATH):
        self.conn = db.connect(db_path, check_same_thread=False)
        self._lock = threading.Lock()
        self._embedder = None

    def _query(self, sql, params=()):
        with self._lock:
            return self.conn.execute(sql, params).fetchall()

    @property
    def embedder(self):
        if self._embedder is None:
            from notecabinet.index import load_embedder
            self._embedder = load_embedder()
        return self._embedder

    def bm25(self, question, k):
        """[(chunk_id, score)], best first. Score = -bm25(), so higher is better."""
        words = re.findall(r"\w+", question)
        if not words:
            return []
        match = " OR ".join(f'"{w}"' for w in words)  # quoted terms: '?', ':' etc. can't break FTS syntax
        return self._query(
            "SELECT rowid, -bm25(chunks_fts) FROM chunks_fts WHERE chunks_fts MATCH ? "
            "ORDER BY bm25(chunks_fts) LIMIT ?", (match, k))

    def dense(self, question, k):
        """[(chunk_id, cosine similarity)], best first."""
        vec = self.embedder.encode(config.QUERY_PREFIX + question, normalize_embeddings=True).astype("float32")
        rows = self._query(
            "SELECT rowid, distance FROM chunks_vec WHERE embedding MATCH ? AND k = ? ORDER BY distance",
            (vec.tobytes(), k))
        return [(cid, 1 - d * d / 2) for cid, d in rows]  # unit vectors: L2 distance -> cosine

    def hybrid(self, question, k):
        """Reciprocal Rank Fusion of bm25 and dense candidate lists."""
        n = config.RERANK_CANDIDATES
        return rrf([self.bm25(question, n), self.dense(question, n)], k)

    def documents(self, scored):
        """Turn [(chunk_id, score)] into Documents, keeping the order."""
        if not scored:
            return []
        ids = [cid for cid, _ in scored]
        rows = self._query(
            f"SELECT id, path, chunk_index, title, date, start, end, text FROM chunks "
            f"WHERE id IN ({','.join('?' * len(ids))})", ids)
        by_id = {r[0]: r for r in rows}
        docs = []
        for rank, (cid, score) in enumerate(scored, 1):
            _, path, chunk_index, title, date, start, end, text = by_id[cid]
            docs.append(Document(page_content=text, metadata={
                "chunk_id": cid, "path": path, "chunk_index": chunk_index, "title": title, "date": date,
                "start": start, "end": end, "retrieval_score": float(score), "retrieval_rank": rank,
            }))
        return docs


def rrf(ranked_lists, k, rrf_k=config.RRF_K):
    """Reciprocal Rank Fusion: score(chunk) = sum over lists of 1 / (rrf_k + rank), rank from 1.
    Uses ranks only, so BM25 and cosine scores never have to be put on the same scale."""
    fused = {}
    for ranked in ranked_lists:
        for rank, (cid, _) in enumerate(ranked, 1):
            fused[cid] = fused.get(cid, 0.0) + 1.0 / (rrf_k + rank)
    return sorted(fused.items(), key=lambda kv: -kv[1])[:k]


class Reranker:
    """bge-reranker-base cross-encoder: reads question and chunk *together*, scores relevance 0..1."""

    def __init__(self):
        import torch
        from sentence_transformers import CrossEncoder

        cuda = torch.cuda.is_available()
        self.model = CrossEncoder(
            config.RERANKER, revision=config.RERANKER_REVISION, device="cuda" if cuda else "cpu",
            model_kwargs={"torch_dtype": torch.float16 if cuda else torch.float32},
        )

    def score(self, question, docs):
        """Set metadata["rerank_score"] on every doc (in place) and return them."""
        if docs:
            scores = self.model.predict([(question, context_text(d)) for d in docs], show_progress_bar=False)
            for d, s in zip(docs, scores):
                d.metadata["rerank_score"] = float(s)
        return docs

    def rerank(self, question, docs, k):
        return sorted(self.score(question, docs), key=lambda d: -d.metadata["rerank_score"])[:k]


class NoteRetriever(BaseRetriever):
    """bm25 / dense / hybrid: top-k chunks straight from the index."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    index: Index
    method: str
    k: int = config.FINAL_K

    def _get_relevant_documents(self, query, *, run_manager=None):
        return self.index.documents(getattr(self.index, self.method)(query, self.k))


class RerankRetriever(BaseRetriever):
    """hybrid+rerank: take the hybrid top-N candidates, let the cross-encoder pick the best k."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    index: Index
    reranker: Reranker
    candidates: int = config.RERANK_CANDIDATES
    k: int = config.FINAL_K

    def _get_relevant_documents(self, query, *, run_manager=None):
        docs = self.index.documents(self.index.hybrid(query, self.candidates))
        return self.reranker.rerank(query, docs, self.k)


def make_retriever(name, index, reranker=None):
    if name == "hybrid+rerank":
        return RerankRetriever(index=index, reranker=reranker or Reranker())
    if name in ("bm25", "dense", "hybrid"):
        return NoteRetriever(index=index, method=name)
    raise ValueError(f"unknown retriever {name!r}; choose from {', '.join(RETRIEVERS)}")
