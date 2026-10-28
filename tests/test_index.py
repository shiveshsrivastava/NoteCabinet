"""M1 tests: exact spans (task 12) and incremental re-indexing (task 13).

Everything runs on temp copies and temp databases: data/notes/ and index/ are never touched.
"""

import hashlib
import shutil

import numpy as np
import pytest
from conftest import BENCHMARK_NOTES

from notecabinet import config, db
from notecabinet.index import (
    build_index,
    chunk_note,
    find_notes,
    load_tokenizer,
    make_splitter,
    read_note,
    update_index,
)


def notes_fingerprint():
    h = hashlib.sha256()
    for p in find_notes(BENCHMARK_NOTES):
        h.update(p.name.encode() + p.read_bytes())
    return h.hexdigest()


@pytest.fixture(scope="session", autouse=True)
def real_notes_untouched():
    before = notes_fingerprint()
    yield
    assert notes_fingerprint() == before, "a test modified data/notes/"


@pytest.fixture(scope="session")
def splitter():
    return make_splitter(load_tokenizer())


@pytest.fixture(scope="session")
def full_index(tmp_path_factory):
    """A fresh index of the real notes, built into a temp database."""
    path = tmp_path_factory.mktemp("full") / "notes.db"
    build_index(BENCHMARK_NOTES, path)
    return path


def rows(db_path, sql):
    conn = db.connect(db_path)
    try:
        return conn.execute(sql).fetchall()
    finally:
        conn.close()


def assert_spans_exact(db_path, notes_dir):
    chunks = rows(db_path, "SELECT path, start, end, text FROM chunks")
    assert chunks, "index has no chunks"
    for path, start, end, text in chunks:
        raw = (notes_dir / path).read_bytes().decode("utf-8")
        assert raw[start:end] == text, f"{path} [{start}:{end}] does not match the stored chunk"


# ---------------------------------------------------------------- task 12: spans

def test_every_span_maps_to_the_exact_source_text(full_index):
    assert_spans_exact(full_index, BENCHMARK_NOTES)


def test_every_note_is_indexed_and_tables_agree(full_index):
    n_notes = len(find_notes(BENCHMARK_NOTES))
    assert rows(full_index, "SELECT count(*) FROM files")[0][0] == n_notes
    counts = [rows(full_index, f"SELECT count(*) FROM {t}")[0][0] for t in ("chunks", "chunks_fts", "chunks_vec")]
    assert len(set(counts)) == 1


def test_spans_never_cover_frontmatter(full_index):
    for path, start in rows(full_index, "SELECT path, start FROM chunks"):
        assert start >= read_note(BENCHMARK_NOTES / path, BENCHMARK_NOTES).body_offset


def test_chunks_respect_the_token_limit(full_index):
    tok = load_tokenizer()
    for (text,) in rows(full_index, "SELECT text FROM chunks"):
        assert len(tok.tokenize(text)) <= config.CHUNK_TOKENS


EDGE_CASES = {
    "crlf.md": b'---\r\ntitle: "CRLF"\r\ndate: 2025-10-05\r\n---\r\n\r\n## A\r\nline one\r\n\r\n## B\r\nline two\r\n',
    "bom.md": "﻿---\ntitle: BOM\ndate: 2025-10-06\n---\nbody here\n".encode(),
    "2025-11-01-no-frontmatter.md": b"just a body\nsecond line\n",
    "2025-10-07-bad-yaml.md": b"---\ntitle: [unclosed\n---\nbody\n",
    "emoji.md": "---\ntitle: Emoji\ndate: 2025-10-08\n---\n- [x] done ✅ then text\n".encode(),
}


@pytest.mark.parametrize("name", EDGE_CASES)
def test_edge_case_spans_are_exact(tmp_path, splitter, name):
    (tmp_path / name).write_bytes(EDGE_CASES[name])
    note = read_note(tmp_path / name, tmp_path)
    docs = chunk_note(note, splitter)
    assert docs
    for d in docs:
        assert note.raw[d.metadata["start"]:d.metadata["end"]] == d.page_content
        assert d.metadata["start"] >= note.body_offset


def test_missing_frontmatter_falls_back_to_filename(tmp_path):
    for name in ("2025-11-01-no-frontmatter.md", "2025-10-07-bad-yaml.md"):
        (tmp_path / name).write_bytes(EDGE_CASES[name])
        note = read_note(tmp_path / name, tmp_path)
        assert note.date.isoformat() == name[:10]
        assert note.title == name[11:-3].replace("-", " ")


# ---------------------------------------------------------------- task 13: incremental

@pytest.fixture
def small_notes(tmp_path):
    """A temp folder with 6 real notes (one of them long enough to be split)."""
    src = find_notes(BENCHMARK_NOTES)
    picked = src[:5] + [BENCHMARK_NOTES / "2025-10-23-e596a-lecture-mot-deadline.md"]
    folder = tmp_path / "notes"
    folder.mkdir()
    for p in picked:
        shutil.copy(p, folder / p.name)
    return folder


def test_unchanged_notes_are_skipped(small_notes, tmp_path):
    dbp = tmp_path / "i.db"
    assert update_index(small_notes, dbp)["mode"].startswith("full")
    s = update_index(small_notes, dbp)
    assert (s["mode"], s["unchanged"], s["chunks_embedded"]) == ("incremental", 6, 0)


def test_edited_note_is_reindexed(small_notes, tmp_path):
    dbp = tmp_path / "i.db"
    update_index(small_notes, dbp)
    note = sorted(small_notes.iterdir())[0]
    note.write_text(note.read_text() + "\n- zebracorn meeting moved to Fri\n")
    s = update_index(small_notes, dbp)
    assert (s["changed"], s["unchanged"]) == (1, 5)
    assert rows(dbp, "SELECT count(*) FROM chunks_fts WHERE chunks_fts MATCH 'zebracorn'")[0][0] == 1
    assert_spans_exact(dbp, small_notes)


def test_deleted_note_is_removed_everywhere(small_notes, tmp_path):
    dbp = tmp_path / "i.db"
    update_index(small_notes, dbp)
    victim = sorted(small_notes.iterdir())[0]
    ids = [r[0] for r in rows(dbp, f"SELECT id FROM chunks WHERE path = '{victim.name}'")]
    victim.unlink()
    assert update_index(small_notes, dbp)["deleted"] == 1
    assert rows(dbp, f"SELECT count(*) FROM files WHERE path = '{victim.name}'")[0][0] == 0
    for table in ("chunks", "chunks_fts", "chunks_vec"):
        key = "id" if table == "chunks" else "rowid"
        assert rows(dbp, f"SELECT count(*) FROM {table} WHERE {key} IN ({','.join(map(str, ids))})")[0][0] == 0


def test_new_note_is_added(small_notes, tmp_path):
    dbp = tmp_path / "i.db"
    update_index(small_notes, dbp)
    (small_notes / "2025-12-08-new.md").write_text('---\ntitle: "New"\ndate: 2025-12-08\n---\n\n- brand new idea\n')
    s = update_index(small_notes, dbp)
    assert (s["new"], s["chunks_embedded"]) == (1, 1)


def test_incremental_matches_a_fresh_full_build(small_notes, tmp_path):
    dbp = tmp_path / "inc.db"
    update_index(small_notes, dbp)
    files = sorted(small_notes.iterdir())
    files[0].write_text(files[0].read_text() + "\n- edited\n")
    files[1].unlink()
    (small_notes / "2025-12-09-added.md").write_text("---\ntitle: Added\ndate: 2025-12-09\n---\n- added note\n")
    update_index(small_notes, dbp)
    build_index(small_notes, tmp_path / "full.db")

    q = ("SELECT c.path, c.chunk_index, c.start, c.end, c.text, f.text, v.embedding FROM chunks c "
         "JOIN chunks_fts f ON f.rowid = c.id JOIN chunks_vec v ON v.rowid = c.id ORDER BY c.path, c.chunk_index")
    inc, full = rows(dbp, q), rows(tmp_path / "full.db", q)
    assert [r[:6] for r in inc] == [r[:6] for r in full]
    for a, b in zip(inc, full):
        assert np.allclose(np.frombuffer(a[6], np.float32), np.frombuffer(b[6], np.float32), atol=1e-5)
    files_q = "SELECT path, sha256, n_chunks FROM files ORDER BY path"
    assert rows(dbp, files_q) == rows(tmp_path / "full.db", files_q)


def test_changed_settings_force_a_rebuild(small_notes, tmp_path, monkeypatch):
    dbp = tmp_path / "i.db"
    update_index(small_notes, dbp)
    monkeypatch.setattr(config, "CHUNK_TOKENS", 200)
    s = update_index(small_notes, dbp)
    assert "chunk_tokens changed: 300 -> 200" in s["mode"]
    assert update_index(small_notes, dbp)["mode"] == "incremental"  # new signature was saved
    monkeypatch.setattr(config, "CHUNKER_VERSION", config.CHUNKER_VERSION + 1)
    assert "chunker_version changed" in update_index(small_notes, dbp)["mode"]
