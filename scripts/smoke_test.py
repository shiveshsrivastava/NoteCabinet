"""Environment smoke test. Run before anything else in M0.

Checks: sqlite extension loading + sqlite-vec, FTS5, CUDA in torch,
(warn-only) llama-server at LLM_URL, and that LangSmith tracing is off.
"""

import os
import sqlite3
import struct
import sys

LLM_URL = os.environ.get("LLM_URL", "http://localhost:8080")

results = []  # (name, status, detail) with status in PASS / FAIL / WARN


def check(name, fn, warn_only=False):
    try:
        detail = fn()
        results.append((name, "PASS", detail))
    except Exception as e:
        results.append((name, "WARN" if warn_only else "FAIL", f"{type(e).__name__}: {e}"))


def check_sqlite_vec():
    import sqlite_vec

    db = sqlite3.connect(":memory:")
    if not hasattr(db, "enable_load_extension"):
        raise RuntimeError("this Python's sqlite3 was built without extension loading")
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.enable_load_extension(False)

    db.execute("CREATE VIRTUAL TABLE v USING vec0(embedding float[3])")
    vecs = {1: [1.0, 0.0, 0.0], 2: [0.0, 1.0, 0.0], 3: [0.9, 0.1, 0.0]}
    for rowid, v in vecs.items():
        db.execute("INSERT INTO v(rowid, embedding) VALUES (?, ?)", (rowid, struct.pack("3f", *v)))
    rows = db.execute(
        "SELECT rowid FROM v WHERE embedding MATCH ? ORDER BY distance LIMIT 2",
        (struct.pack("3f", 1.0, 0.0, 0.0),),
    ).fetchall()
    if [r[0] for r in rows] != [1, 3]:
        raise RuntimeError(f"unexpected nearest neighbours: {rows}")
    version = db.execute("SELECT vec_version()").fetchone()[0]
    return f"sqlite {sqlite3.sqlite_version}, sqlite-vec {version}, KNN query ok"


def check_fts5():
    db = sqlite3.connect(":memory:")
    db.execute("CREATE VIRTUAL TABLE t USING fts5(body)")
    db.executemany("INSERT INTO t(body) VALUES (?)", [("midterm moved to friday",), ("lab meeting notes",)])
    rows = db.execute("SELECT body FROM t WHERE t MATCH 'midterm' ORDER BY bm25(t)").fetchall()
    if rows != [("midterm moved to friday",)]:
        raise RuntimeError(f"unexpected FTS5 result: {rows}")
    return "FTS5 + bm25() ok"


def check_cuda():
    import torch

    if not torch.cuda.is_available():
        raise RuntimeError(f"torch {torch.__version__} cannot see a CUDA device")
    x = torch.ones(2, device="cuda") * 2
    assert x.sum().item() == 4.0
    name = torch.cuda.get_device_name(0)
    total = torch.cuda.get_device_properties(0).total_memory / 2**30
    return f"torch {torch.__version__}, {name}, {total:.1f} GiB"


def check_llama_server():
    import httpx

    r = httpx.get(f"{LLM_URL}/health", timeout=3)
    r.raise_for_status()
    return f"{LLM_URL}/health -> {r.json()}"


def check_no_tracing():
    on = [k for k in ("LANGCHAIN_TRACING_V2", "LANGSMITH_TRACING")
          if os.environ.get(k, "").strip().lower() in ("1", "true", "yes")]
    if on:
        raise RuntimeError(f"LangSmith tracing enabled via {', '.join(on)}; the app must stay offline")
    return "LangSmith tracing off"


check("sqlite-vec", check_sqlite_vec)
check("fts5", check_fts5)
check("cuda", check_cuda)
check("llama-server", check_llama_server, warn_only=True)
check("no-tracing", check_no_tracing)

for name, status, detail in results:
    print(f"[{status}] {name:13} {detail}")

failed = [r for r in results if r[1] == "FAIL"]
print("\nSMOKE TEST", "FAILED" if failed else "PASSED")
sys.exit(1 if failed else 0)
