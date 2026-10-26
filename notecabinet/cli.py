"""Command line: `notecabinet index ...` (ask / eval arrive in later milestones)."""

import argparse
from pathlib import Path

from notecabinet import config


def main(argv=None):
    parser = argparse.ArgumentParser(prog="notecabinet", description="Local-first AI over your markdown notes.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_index = sub.add_parser("index", help="build or update the index from a notes folder")
    p_index.add_argument("notes_dir", nargs="?", default=str(config.NOTES_DIR),
                         help=f"folder of .md notes (default: {config.NOTES_DIR.relative_to(config.ROOT)})")
    p_index.add_argument("--full", action="store_true", help="ignore what's indexed and rebuild from scratch")
    p_index.add_argument("--db", default=str(config.INDEX_PATH), help=argparse.SUPPRESS)  # for tests

    args = parser.parse_args(argv)
    if args.command == "index":
        cmd_index(p_index, args)


def cmd_index(parser, args):
    from notecabinet.index import rebuild_index, update_index  # heavy imports only when needed

    notes_dir = Path(args.notes_dir)
    if not notes_dir.is_dir():
        parser.error(f"not a folder: {notes_dir}")
    if args.full:
        s = {**rebuild_index(notes_dir, args.db), "mode": "full (--full)"}
    else:
        s = update_index(notes_dir, args.db)

    if s["mode"] == "incremental":
        detail = (f"{s['notes']} notes ({s['new']} new, {s['changed']} changed, {s['deleted']} deleted, "
                  f"{s['unchanged']} unchanged), {s['chunks_embedded']} chunks embedded")
    else:
        detail = f"{s['notes']} notes, {s['chunks']} chunks"
    print(f"{s['mode']}: {detail} in {s['seconds']:.1f}s -> {_short(args.db)}")


def _short(path):
    """Path relative to the current folder when possible, for readable output."""
    path = Path(path).resolve()
    try:
        return path.relative_to(Path.cwd())
    except ValueError:
        return path


if __name__ == "__main__":
    main()
