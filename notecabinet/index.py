"""Indexing: read notes, chunk them, embed them, and write the SQLite index.

Span convention: every span is a (start, end) offset into the note's *raw file text*,
so `note.raw[start:end]` is exactly the cited text. Spans never cover the frontmatter.
Notes are only ever read, never written.
"""

import hashlib
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

import yaml
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from notecabinet import config

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


def find_notes(notes_dir):
    """All .md files under notes_dir (including subfolders), in a stable order."""
    return sorted(Path(notes_dir).rglob("*.md"))


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
