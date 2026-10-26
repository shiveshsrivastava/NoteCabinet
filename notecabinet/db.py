"""The index: one SQLite file holding keyword search, vector search and chunk metadata.

Everything here can be rebuilt from the notes at any time; it holds nothing that isn't in them.
All three chunk tables share one id: chunks.id == chunks_fts.rowid == chunks_vec.rowid.
"""

import sqlite3
from pathlib import Path

import sqlite_vec

from notecabinet import config

SCHEMA_VERSION = 1

SCHEMA = f"""
-- one row per chunk; start/end are offsets into the raw note file
CREATE TABLE IF NOT EXISTS chunks (
    id          INTEGER PRIMARY KEY,
    path        TEXT NOT NULL,      -- relative to the notes folder
    chunk_index INTEGER NOT NULL,
    title       TEXT NOT NULL,
    date        TEXT NOT NULL,      -- ISO date of the note
    start       INTEGER NOT NULL,
    end         INTEGER NOT NULL,
    text        TEXT NOT NULL,      -- exactly raw[start:end]
    UNIQUE (path, chunk_index)
);
CREATE INDEX IF NOT EXISTS chunks_path ON chunks(path);

-- keyword search (BM25). Indexes the context text (title + date + chunk), the same text
-- that is embedded. porter: "meetings" matches "meeting".
CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(text, tokenize = 'porter unicode61');

-- vector search. Vectors are normalized, so L2 distance ranks exactly like cosine similarity.
CREATE VIRTUAL TABLE IF NOT EXISTS chunks_vec USING vec0(embedding float[{config.EMBEDDING_DIM}]);

-- one row per indexed note, for incremental re-indexing (unchanged hash = skip)
CREATE TABLE IF NOT EXISTS files (
    path       TEXT PRIMARY KEY,
    sha256     TEXT NOT NULL,
    n_chunks   INTEGER NOT NULL,
    indexed_at TEXT NOT NULL
);

-- what the index was built with; a mismatch forces a full rebuild
CREATE TABLE IF NOT EXISTS meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""


def connect(path=config.INDEX_PATH):
    """Open (creating if needed) the index and load the sqlite-vec extension."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.enable_load_extension(False)
    conn.execute("PRAGMA journal_mode = WAL")  # readers (the API) don't block the indexer
    return conn


def create_schema(conn):
    conn.executescript(SCHEMA)
    if get_meta(conn, "schema_version") is None:
        set_meta(conn, "schema_version", SCHEMA_VERSION)
    conn.commit()


def get_meta(conn, key):
    row = conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
    return row[0] if row else None


def set_meta(conn, key, value):
    conn.execute("INSERT INTO meta(key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                 (key, str(value)))
