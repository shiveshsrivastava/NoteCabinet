"""Indexing: read notes, chunk them, embed them, and write the SQLite index.

Span convention: every span is a (start, end) offset into the note's *raw file text*,
so `note.raw[start:end]` is exactly the cited text. Spans never cover the frontmatter.
Notes are only ever read, never written.
"""

import hashlib
import re
import sys
import time
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path

import yaml
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from notecabinet import config, db

# Split on markdown structure first (headings, paragraphs, lines), words only as a last resort.
SEPARATORS = ["\n## ", "\n### ", "\n\n", "\n", " ", ""]

# Optional BOM, a '---' line, the YAML, a closing '---' line. Works with \n and \r\n.
FRONTMATTER_RE = re.compile(r"\A﻿?---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.S)
DATE_PREFIX_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")


@dataclass
class Note:
    path: str          # relative to the notes folder, e.g. "2025-10-22-dsec-laplace-review.md"
    title: str
    date: date
    tags: list[str]
    raw: str           # the whole file, exactly as on disk
    body_offset: int   # where the body starts in raw
    sha256: str        # of the file's bytes; unchanged hash = skip on re-index

    @property
    def body(self):
        return self.raw[self.body_offset:]


def read_note(path, notes_dir):
    """Parse one markdown note. Missing or broken frontmatter falls back to the filename."""
    path, notes_dir = Path(path), Path(notes_dir)
    data = path.read_bytes()  # bytes, not read_text(): keeps \r\n so offsets match the file on disk
    raw = data.decode("utf-8")

    meta, body_offset = {}, 0
    if m := FRONTMATTER_RE.match(raw):
        body_offset = m.end()
        try:
            meta = yaml.safe_load(m.group(1)) or {}
            if not isinstance(meta, dict):
                raise ValueError("not a key: value mapping")
        except (yaml.YAMLError, ValueError) as e:
            reason = getattr(e, "problem", None) or e  # YAML errors are multi-line; keep the gist
            print(f"warning: {path.name}: unreadable frontmatter ({reason}); using filename", file=sys.stderr)
            meta = {}
    while body_offset < len(raw) and raw[body_offset] in "\r\n":  # skip blank lines before the body
        body_offset += 1

    return Note(
        path=path.relative_to(notes_dir).as_posix(),
        title=str(meta.get("title") or _title_from_filename(path)),
        date=_as_date(meta.get("date")) or _date_from_filename(path) or date.fromtimestamp(path.stat().st_mtime),
        tags=_as_tags(meta.get("tags")),
        raw=raw,
        body_offset=body_offset,
        sha256=hashlib.sha256(data).hexdigest(),
    )


def find_notes(notes_dir):
    """All .md files under notes_dir (including subfolders), in a stable order."""
    return sorted(Path(notes_dir).rglob("*.md"))


# ---------------------------------------------------------------- chunking

def load_tokenizer():
    """The embedder's own tokenizer, so chunk sizes are measured the way the model sees text."""
    from transformers import AutoTokenizer

    return AutoTokenizer.from_pretrained(config.EMBEDDER, revision=config.EMBEDDER_REVISION)


def make_splitter(tokenizer):
    return RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
        tokenizer, chunk_size=config.CHUNK_TOKENS, chunk_overlap=config.CHUNK_OVERLAP, separators=SEPARATORS
    )


def chunk_note(note, splitter):
    """Split a note's body into Documents whose metadata carries an exact span into note.raw.

    We compute spans ourselves instead of using add_start_index=True: with a token-based
    overlap, LangChain backs up only CHUNK_OVERLAP *characters* before searching, which
    misses some chunks (start_index = -1 on 2 of 139 chunks in our notes). Each chunk is an
    exact substring of the body, so searching from just after the previous chunk's start
    always finds it.
    """
    docs, search_from = [], 0
    for i, text in enumerate(splitter.split_text(note.body)):
        pos = note.body.find(text, search_from)
        if pos < 0:
            raise ValueError(f"{note.path}: chunk {i} not found in body")
        start = note.body_offset + pos
        docs.append(Document(page_content=text, metadata={
            "path": note.path,
            "title": note.title,
            "date": note.date.isoformat(),
            "chunk_index": i,
            "start": start,
            "end": start + len(text),
        }))
        search_from = pos + 1
    return docs


def context_text(doc):
    """What the embedder (and later the LLM) sees: the chunk prefixed with its note's title and date.

    A chunk like "- moved to Wed 4pm" means little alone; "DSEC reschedule (Mon 2025-10-13)" above it
    tells the model what moved and when. The prefix is never part of the stored span: the span
    still points at doc.page_content in the raw file, so citations highlight only real note text.
    """
    m = doc.metadata
    weekday = date.fromisoformat(m["date"]).strftime("%a")  # "Mon": helps "what's on my Mondays?"
    return f"{m['title']} ({weekday} {m['date']})\n{doc.page_content}"


# ---------------------------------------------------------------- embedding

def load_embedder():
    """bge-small on the GPU if there is one (from the local cache only, see config)."""
    import torch
    from sentence_transformers import SentenceTransformer

    device = "cuda" if torch.cuda.is_available() else "cpu"
    return SentenceTransformer(config.EMBEDDER, revision=config.EMBEDDER_REVISION, device=device)


def embed_documents(docs, model, batch_size=32):
    """One float32 vector per chunk, shape (len(docs), EMBEDDING_DIM).

    Vectors are normalized to length 1, so cosine similarity is a plain dot product
    (and sqlite-vec's distances rank the same way).
    """
    return model.encode(
        [context_text(d) for d in docs],
        batch_size=batch_size,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=False,
    ).astype("float32")


# ---------------------------------------------------------------- writing the index

def index_signature():
    """Everything that, if it changes, makes stored chunks or vectors invalid."""
    return {
        "chunker_version": config.CHUNKER_VERSION,
        "chunk_tokens": config.CHUNK_TOKENS,
        "chunk_overlap": config.CHUNK_OVERLAP,
        "embedder": config.EMBEDDER,
        "embedder_revision": config.EMBEDDER_REVISION,
        "embedding_dim": config.EMBEDDING_DIM,
    }


def build_index(notes_dir=config.NOTES_DIR, db_path=config.INDEX_PATH):
    """Full rebuild: read, chunk and embed every note, then replace the whole index in one transaction."""
    t0 = time.perf_counter()
    notes_dir = Path(notes_dir).resolve()
    notes = [read_note(p, notes_dir) for p in find_notes(notes_dir)]
    splitter = make_splitter(load_tokenizer())
    chunked = [(note, chunk_note(note, splitter)) for note in notes]
    docs = [d for _, note_docs in chunked for d in note_docs]
    vectors = embed_documents(docs, load_embedder()) if docs else []  # one GPU pass for all chunks

    conn = db.connect(db_path)
    db.create_schema(conn)
    with conn:  # one transaction: a crash leaves the previous index intact
        for table in ("chunks", "chunks_fts", "chunks_vec", "files"):
            conn.execute(f"DELETE FROM {table}")
        i = 0
        for note, note_docs in chunked:
            _add_note(conn, note, note_docs, vectors[i:i + len(note_docs)])
            i += len(note_docs)
        for key, value in index_signature().items():
            db.set_meta(conn, key, value)
        db.set_meta(conn, "notes_dir", notes_dir)
    check_counts(conn)
    conn.close()
    return {"notes": len(notes), "chunks": len(docs), "seconds": time.perf_counter() - t0}


def update_index(notes_dir=config.NOTES_DIR, db_path=config.INDEX_PATH):
    """Incremental update: skip notes whose hash is unchanged, re-index changed or new ones,
    and remove notes that no longer exist. Only new/changed chunks are embedded."""
    t0 = time.perf_counter()
    notes_dir = Path(notes_dir).resolve()
    conn = db.connect(db_path)
    db.create_schema(conn)
    if db.get_meta(conn, "embedder") is None:  # never built: nothing to compare against
        conn.close()
        return {**build_index(notes_dir, db_path), "mode": "full (no index yet)"}

    indexed = dict(conn.execute("SELECT path, sha256 FROM files").fetchall())
    on_disk = {note.path: note for note in (read_note(p, notes_dir) for p in find_notes(notes_dir))}
    new = [n for path, n in on_disk.items() if path not in indexed]
    changed = [n for path, n in on_disk.items() if path in indexed and indexed[path] != n.sha256]
    deleted = [path for path in indexed if path not in on_disk]

    to_index = new + changed
    chunked, docs, vectors = [], [], []
    if to_index:  # load models only when there is something to embed
        splitter = make_splitter(load_tokenizer())
        chunked = [(note, chunk_note(note, splitter)) for note in to_index]
        docs = [d for _, note_docs in chunked for d in note_docs]
        vectors = embed_documents(docs, load_embedder()) if docs else []

    with conn:
        for path in deleted + [n.path for n in changed]:
            _remove_note(conn, path)
        i = 0
        for note, note_docs in chunked:
            _add_note(conn, note, note_docs, vectors[i:i + len(note_docs)])
            i += len(note_docs)
    check_counts(conn)
    conn.close()
    return {"mode": "incremental", "notes": len(on_disk), "new": len(new), "changed": len(changed),
            "deleted": len(deleted), "unchanged": len(on_disk) - len(to_index),
            "chunks_embedded": len(docs), "seconds": time.perf_counter() - t0}


def _remove_note(conn, path):
    """Delete one note's rows from every table."""
    ids = [(r[0],) for r in conn.execute("SELECT id FROM chunks WHERE path = ?", (path,))]
    conn.executemany("DELETE FROM chunks_fts WHERE rowid = ?", ids)
    conn.executemany("DELETE FROM chunks_vec WHERE rowid = ?", ids)
    conn.execute("DELETE FROM chunks WHERE path = ?", (path,))
    conn.execute("DELETE FROM files WHERE path = ?", (path,))


def _add_note(conn, note, docs, vectors):
    """Insert one note's chunks into chunks / chunks_fts / chunks_vec (same id) and record it in files."""
    for doc, vector in zip(docs, vectors):
        m = doc.metadata
        chunk_id = conn.execute(
            "INSERT INTO chunks(path, chunk_index, title, date, start, end, text) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (m["path"], m["chunk_index"], m["title"], m["date"], m["start"], m["end"], doc.page_content),
        ).lastrowid
        conn.execute("INSERT INTO chunks_fts(rowid, text) VALUES (?, ?)", (chunk_id, context_text(doc)))
        conn.execute("INSERT INTO chunks_vec(rowid, embedding) VALUES (?, ?)", (chunk_id, vector.tobytes()))
    conn.execute(
        "INSERT INTO files(path, sha256, n_chunks, indexed_at) VALUES (?, ?, ?, ?)",
        (note.path, note.sha256, len(docs), datetime.now(timezone.utc).isoformat(timespec="seconds")),
    )


def check_counts(conn):
    """The three chunk tables must hold the same rows, matching what files says was indexed."""
    n = {t: conn.execute(f"SELECT count(*) FROM {t}").fetchone()[0] for t in ("chunks", "chunks_fts", "chunks_vec")}
    expected = conn.execute("SELECT coalesce(sum(n_chunks), 0) FROM files").fetchone()[0]
    if len(set(n.values())) != 1 or n["chunks"] != expected:
        raise RuntimeError(f"index is inconsistent: {n}, files expects {expected}")
    return n["chunks"]


def _as_date(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value.strip()[:10])
        except ValueError:
            return None
    return None


def _date_from_filename(path):
    m = DATE_PREFIX_RE.match(path.stem)
    return _as_date(m.group(1)) if m else None


def _title_from_filename(path):
    stem = DATE_PREFIX_RE.sub("", path.stem).strip("-_ ")
    return stem.replace("-", " ").replace("_", " ") or path.stem


def _as_tags(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(t) for t in value]
    return []
