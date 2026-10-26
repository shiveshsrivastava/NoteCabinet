"""Ask: retrieve -> rerank/score -> (abstain?) -> generate with citations.

Abstention returns NOT_FOUND when either
  - the best reranker score among the final chunks is below config.ABSTAIN_THRESHOLD
    (tuned on the dev split only), or
  - the model itself answers exactly NOT_FOUND (the prompt tells it to).
Every [n] in the answer is mapped to the cited chunk's note path and raw-file span.
"""

import re
import time

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from notecabinet import config
from notecabinet.index import context_text
from notecabinet.retrieve import RETRIEVERS, Index, Reranker, make_retriever

NOT_FOUND = "NOT_FOUND"

SYSTEM_PROMPT = """You answer questions about the user's own notes, using ONLY the numbered excerpts provided.

Rules:
- After each statement, cite the excerpt(s) it comes from as [n], e.g. "It moved to Wednesdays at 4pm [2]."
- Every fact in your answer must be written in an excerpt. Never infer or invent names, titles, numbers or dates.
- The excerpts are only a few retrieved pieces of the notes, not all of them. Never claim something is absent from the notes; if the excerpts show only part of the answer, give that part.
- Each excerpt starts with its note's title and date. If excerpts disagree, the later note usually replaces the earlier one; if the question names a time, use what was true at that time.
- The notes use personal shorthand. Only expand an abbreviation if an excerpt shows what it means.
- Never use outside knowledge or guess. If the excerpts do not contain the answer, reply with exactly: NOT_FOUND
- Answer only what was asked, in one to three sentences. Address the user as "you"."""

USER_PROMPT = "Excerpts:\n\n{excerpts}\n\nQuestion: {question}"

PROMPT = ChatPromptTemplate.from_messages([("system", SYSTEM_PROMPT), ("human", USER_PROMPT)])
CITATION_RE = re.compile(r"\[(\d+(?:\s*,\s*\d+)*)\]")


def make_llm():
    """ChatOpenAI pointed at the local llama-server (its OpenAI-compatible API). No other network calls."""
    return ChatOpenAI(
        base_url=f"{config.LLM_URL}/v1", api_key="local", model="local",
        temperature=0, seed=config.SEED, max_tokens=config.LLM_MAX_TOKENS, timeout=120, max_retries=1,
        # Reusing llama-server's cached prompt state changes the arithmetic slightly, so the same
        # question could get a different answer (2 distinct answers in 3 identical runs). Off = repeatable.
        extra_body={"cache_prompt": False},
    )


def format_excerpts(docs):
    return "\n\n".join(f"[{i}] {context_text(d)}" for i, d in enumerate(docs, 1))


def parse_citations(answer, docs):
    """[(n, doc)] for every valid [n] in the answer (in order, no repeats), plus any invalid numbers."""
    cited, invalid = [], []
    for group in CITATION_RE.findall(answer):
        for n in (int(x) for x in group.split(",")):
            if not 1 <= n <= len(docs):
                invalid.append(n)
            elif n not in [c for c, _ in cited]:
                cited.append((n, docs[n - 1]))
    return cited, invalid


class Asker:
    """Holds the index, reranker and chain so repeated questions don't reload models."""

    def __init__(self, index=None, reranker=None, threshold=config.ABSTAIN_THRESHOLD):
        self.index = index or Index()
        self.reranker = reranker or Reranker()
        self.threshold = threshold
        self.retrievers = {n: make_retriever(n, self.index, self.reranker) for n in ("bm25", "dense", "hybrid")}
        self.chain = PROMPT | make_llm() | StrOutputParser()

    def retrieve(self, question, retriever):
        """Final chunks, each with a rerank_score, plus per-stage timings (ms)."""
        if retriever not in RETRIEVERS:
            raise ValueError(f"unknown retriever {retriever!r}; choose from {', '.join(RETRIEVERS)}")
        t0 = time.perf_counter()
        if retriever == "hybrid+rerank":
            docs = self.index.documents(self.index.hybrid(question, config.RERANK_CANDIDATES))
        else:
            docs = self.retrievers[retriever].invoke(question)
        t1 = time.perf_counter()
        if retriever == "hybrid+rerank":
            docs = self.reranker.rerank(question, docs, config.FINAL_K)  # reorder + keep 5
        else:
            self.reranker.score(question, docs)  # score only, so one threshold fits every retriever
        t2 = time.perf_counter()
        return docs, {"retrieval_ms": (t1 - t0) * 1000, "rerank_ms": (t2 - t1) * 1000}

    def ask(self, question, retriever="hybrid+rerank"):
        docs, timings = self.retrieve(question, retriever)
        top = max((d.metadata["rerank_score"] for d in docs), default=0.0)
        result = {"question": question, "retriever": retriever, "top_rerank_score": top,
                  "threshold": self.threshold, "sources": [dict(d.metadata) for d in docs]}

        if self.threshold is not None and top < self.threshold:
            return {**result, "answer": NOT_FOUND, "abstained": True, "abstain_reason": "low_rerank_score",
                    "citations": [], "invalid_citations": [], "timings": {**timings, "generation_ms": 0.0}}

        t = time.perf_counter()
        answer = self.chain.invoke({"excerpts": format_excerpts(docs), "question": question}).strip()
        timings["generation_ms"] = (time.perf_counter() - t) * 1000

        if answer.rstrip(".").strip() == NOT_FOUND:
            return {**result, "answer": NOT_FOUND, "abstained": True, "abstain_reason": "model",
                    "citations": [], "invalid_citations": [], "timings": timings}
        cited, invalid = parse_citations(answer, docs)
        citations = [{"n": n, "path": d.metadata["path"], "start": d.metadata["start"], "end": d.metadata["end"],
                      "text": d.page_content} for n, d in cited]
        return {**result, "answer": answer, "abstained": False, "abstain_reason": None,
                "citations": citations, "invalid_citations": invalid, "timings": timings}
