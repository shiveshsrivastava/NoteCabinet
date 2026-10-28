"""Command line: `notecabinet index ...` and `notecabinet ask "..."` (eval arrives in M3)."""

import argparse
from pathlib import Path

from notecabinet import config


def main(argv=None):
    parser = argparse.ArgumentParser(prog="notecabinet", description="Local-first AI over your markdown notes.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_index = sub.add_parser("index", help="build or update the index from a notes folder")
    p_index.add_argument("notes_dir", nargs="?",
                         help="folder of .md notes (required the first time; then defaults to the folder indexed last)")
    p_index.add_argument("--full", action="store_true", help="ignore what's indexed and rebuild from scratch")
    p_index.add_argument("--db", help=argparse.SUPPRESS)  # for tests; users set $NOTECABINET_INDEX

    p_ask = sub.add_parser("ask", help="answer a question from your notes, with citations")
    p_ask.add_argument("question")
    p_ask.add_argument("--retriever", default="hybrid+rerank", choices=["bm25", "dense", "hybrid", "hybrid+rerank"])
    p_ask.add_argument("--json", action="store_true", help="print the full result as JSON")
    p_ask.add_argument("--db", help=argparse.SUPPRESS)

    p_models = sub.add_parser("download-models", help="one-time download of the embedder and reranker (and optionally the LLM)")
    p_models.add_argument("--with-llm", action="store_true", help=f"also download {config.LLM_FILE} for llama-server")
    p_models.add_argument("--llm-dir", help=f"where to put the GGUF (default: {config.DATA_HOME / 'models'})")

    args = parser.parse_args(argv)
    if args.command == "download-models":
        from notecabinet.models import download_models
        download_models(with_llm=args.with_llm, llm_dir=args.llm_dir)
    elif args.command == "index":
        cmd_index(p_index, args)
    elif args.command == "ask":
        cmd_ask(p_ask, args)


def cmd_index(parser, args):
    from notecabinet.index import rebuild_index, stored_notes_dir, update_index  # heavy imports only when needed

    args.db = Path(args.db or config.INDEX_PATH)
    if args.notes_dir is None:
        notes_dir = stored_notes_dir(args.db)
        if notes_dir is None:
            parser.error("which notes folder? The first time, run: notecabinet index PATH/TO/NOTES")
    else:
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

    args.db = Path(args.db or config.INDEX_PATH)
    if not args.db.exists():
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
