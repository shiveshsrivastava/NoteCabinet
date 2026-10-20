"""Command line: `notecabinet index ...` (ask / eval arrive in later milestones)."""

import argparse

from notecabinet import config


def main(argv=None):
    parser = argparse.ArgumentParser(prog="notecabinet", description="Local-first AI over your markdown notes.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_index = sub.add_parser("index", help="build or update the index from a notes folder")
    p_index.add_argument("notes_dir", nargs="?", default=str(config.NOTES_DIR),
                         help=f"folder of .md notes (default: {config.NOTES_DIR.relative_to(config.ROOT)})")

    args = parser.parse_args(argv)
    if args.command == "index":
        parser.exit(1, "index: not implemented yet (M1 tasks 3-11)\n")


if __name__ == "__main__":
    main()
