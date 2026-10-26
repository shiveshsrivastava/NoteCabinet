"""HTTP API: POST /ask, GET /notes, GET /notes/{path}. POST /organize arrives in M4.

Run: uv run uvicorn notecabinet.api:app --reload
The only outbound call is to the local llama-server (via /ask). Notes are only ever read.
"""

import threading
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from notecabinet import config, db
from notecabinet.index import find_notes, read_note
from notecabinet.retrieve import RETRIEVERS

app = FastAPI(title="NoteCabinet", description="Local-first AI over your markdown notes.")

_asker = None
_lock = threading.Lock()  # one question at a time: llama-server runs a single slot anyway


def notes_dir():
    """The folder the index was built from (falls back to the configured default)."""
    if config.INDEX_PATH.exists():
        conn = db.connect(config.INDEX_PATH)
        try:
            stored = db.get_meta(conn, "notes_dir")
        finally:
            conn.close()
        if stored:
            return Path(stored)
    return config.NOTES_DIR


def get_asker():
    global _asker
    if _asker is None:
        if not config.INDEX_PATH.exists():
            raise HTTPException(503, "no index yet; run `notecabinet index` first")
        from notecabinet.ask import Asker
        _asker = Asker()
    return _asker


def resolve_note(path):
    """Map a request path to a note file inside the notes folder, refusing anything outside it."""
    root = notes_dir().resolve()
    target = (root / path).resolve()
    if not target.is_relative_to(root) or target.suffix != ".md" or not target.is_file():
        raise HTTPException(404, "note not found")
    return root, target


class AskRequest(BaseModel):
    question: str
    retriever: str = "hybrid+rerank"


@app.post("/ask")
def ask(req: AskRequest):
    if req.retriever not in RETRIEVERS:
        raise HTTPException(422, f"retriever must be one of {', '.join(RETRIEVERS)}")
    if not req.question.strip():
        raise HTTPException(422, "question is empty")
    with _lock:
        try:
            return get_asker().ask(req.question, req.retriever)
        except HTTPException:
            raise
        except Exception as e:
            if "connect" in str(e).lower() or "Connection" in type(e).__name__:
                raise HTTPException(503, f"can't reach the local LLM at {config.LLM_URL}") from e
            raise


@app.get("/notes")
def list_notes():
    root = notes_dir()
    notes = [read_note(p, root) for p in find_notes(root)]
    return [{"path": n.path, "title": n.title, "date": n.date.isoformat(), "tags": n.tags} for n in notes]


@app.get("/notes/{path:path}")
def get_note(path: str):
    """The raw file text. Citation spans are (start, end) offsets into `raw` (Python characters)."""
    root, target = resolve_note(path)
    note = read_note(target, root)
    return {"path": note.path, "title": note.title, "date": note.date.isoformat(), "tags": note.tags,
            "body_offset": note.body_offset, "raw": note.raw}
