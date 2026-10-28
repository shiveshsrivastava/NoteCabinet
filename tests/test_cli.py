"""CLI smoke tests: the installed `notecabinet` command runs, and path defaults behave.

Every subprocess gets a temp XDG_DATA_HOME, so nothing touches the real ~/.local/share.
"""

import os
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
from importlib.metadata import version

import pytest


@pytest.fixture
def env(tmp_path):
    e = {**os.environ, "XDG_DATA_HOME": str(tmp_path / "data")}
    e.pop("NOTECABINET_INDEX", None)
    return e


def run(args, env, **kw):
    return subprocess.run([sys.executable, "-m", "notecabinet", *args], env=env, capture_output=True, text=True,
                          timeout=120, **kw)


def test_console_script_help_exits_0(env):
    exe = shutil.which("notecabinet")
    assert exe, "the `notecabinet` console script is not installed"
    r = subprocess.run([exe, "--help"], env=env, capture_output=True, text=True, timeout=60)
    assert r.returncode == 0
    assert "index" in r.stdout and "ask" in r.stdout and "serve" in r.stdout


def test_version_matches_package_metadata(env):
    r = run(["--version"], env)
    assert r.returncode == 0
    assert r.stdout.strip() == f"notecabinet {version('notecabinet')}"


@pytest.mark.parametrize("cmd", ["index", "ask", "serve", "download-models"])
def test_subcommand_help_exits_0(env, cmd):
    assert run([cmd, "--help"], env).returncode == 0


def test_first_index_needs_a_notes_folder(env):
    r = run(["index"], env)
    assert r.returncode == 2
    assert "notecabinet index PATH/TO/NOTES" in r.stderr


def test_index_rejects_missing_folder(env, tmp_path):
    r = run(["index", str(tmp_path / "nope")], env)
    assert r.returncode == 2 and "not a folder" in r.stderr


def test_ask_without_index_says_so(env):
    r = run(["ask", "anything?"], env)
    assert r.returncode == 2 and "run `notecabinet index` first" in r.stderr


def test_index_path_follows_env(env, tmp_path):
    code = "from notecabinet import config; print(config.INDEX_PATH)"
    default = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True).stdout.strip()
    assert default == str(tmp_path / "data" / "notecabinet" / "notes.db")
    custom = {**env, "NOTECABINET_INDEX": str(tmp_path / "x.db")}
    assert subprocess.run([sys.executable, "-c", code], env=custom, capture_output=True, text=True).stdout.strip() \
        == str(tmp_path / "x.db")


def test_serve_starts_and_answers(env):
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    proc = subprocess.Popen([sys.executable, "-m", "notecabinet", "serve", "--port", str(port)], env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        deadline = time.time() + 60
        while True:
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{port}/docs", timeout=2) as resp:
                    assert resp.status == 200
                    break
            except OSError:
                if time.time() > deadline or proc.poll() is not None:
                    raise
                time.sleep(0.5)
    finally:
        proc.terminate()
        proc.wait(timeout=10)
