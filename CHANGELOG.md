# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-10-28

First packaged release (not published to PyPI; install from GitHub).

### Added
- `notecabinet index [NOTES_DIR] [--full]`: chunk, embed and index a folder of markdown notes into one
  SQLite file (FTS5 keyword search + sqlite-vec vectors). Incremental by content hash; rebuilds
  automatically when the chunker or embedding model changes. Every chunk stores an exact
  `(start, end)` span into the raw note file.
- `notecabinet ask "..."`: hybrid retrieval (BM25 + vectors, Reciprocal Rank Fusion), cross-encoder
  reranking, and an answer from a local LLM (llama-server) with `[n]` citations mapped to note path and
  span, or "Not in your notes". `--retriever` selects `bm25`, `dense`, `hybrid` or `hybrid+rerank`.
- `notecabinet serve`: HTTP API (`POST /ask`, `GET /notes`, `GET /notes/{path}`) on 127.0.0.1:8000.
- `notecabinet download-models [--with-llm]`: one-time download of the pinned embedder, reranker and
  (optionally) LLM weights.
- `notecabinet --version`, `python -m notecabinet`.
- Synthetic benchmark dataset: 100 notes, 61 hand-checked questions (10 dev / 51 test), 20 Organize pages.
- Test suite (pytest) and GitHub Actions CI (ruff + pytest on Python 3.10-3.13).

### Notes
- The index lives at `$NOTECABINET_INDEX`, else `$XDG_DATA_HOME/notecabinet/notes.db`
  (`~/.local/share/notecabinet/notes.db`). The notes folder is given on the first `index` run and
  remembered.
- Notes are only ever read, never modified.
