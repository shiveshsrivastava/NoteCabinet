"""Command line: `notecabinet index ...` and `notecabinet ask "..."` (eval arrives in M3)."""

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

    p_ask = sub.add_parser("ask", help="answer a question from your notes, with citations")
    p_ask.add_argument("question")
    p_ask.add_argument("--retriever", default="hybrid+rerank", choices=["bm25", "dense", "hybrid", "hybrid+rerank"])
    p_ask.add_argument("--json", action="store_true", help="print the full result as JSON")
    p_ask.add_argument("--db", default=str(config.INDEX_PATH), help=argparse.SUPPRESS)

    args = parser.parse_args(argv)
    if args.command == "index":
        cmd_index(p_index, args)
    elif args.command == "ask":
        cmd_ask(p_ask, args)


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


def cmd_ask(parser, args):
    import json

    if not Path(args.db).exists():
        parser.error(f"no index at {_short(args.db)}; run `notecabinet index` first")
    from notecabinet.ask import Asker
    from notecabinet.retrieve import Index

    try:
        result = Asker(index=Index(args.db)).ask(args.question, args.retriever)
    except Exception as e:  # most often: llama-server isn't running
        if "Connection" in type(e).__name__ or "connect" in str(e).lower():
            parser.exit(1, f"can't reach the local LLM at {config.LLM_URL}; is llama-server running?\n")
        raise
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return
    if result["abstained"]:
        why = "no relevant notes found" if result["abstain_reason"] == "low_rerank_score" else "the notes don't say"
        print(f"Not in your notes ({why}).")
        return
    print(result["answer"])
    if result["citations"]:
        print()
    for c in result["citations"]:
        snippet = " ".join(c["text"].split())[:90]
        print(f"[{c['n']}] {c['path']}:{c['start']}-{c['end']}  {snippet}...")
    if result["invalid_citations"]:
        print(f"(warning: answer cites excerpts that don't exist: {result['invalid_citations']})")


def _short(path):
    """Path relative to the current folder when possible, for readable output."""
    path = Path(path).resolve()
    try:
        return path.relative_to(Path.cwd())
    except ValueError:
        return path


if __name__ == "__main__":
    main()
