# CLAUDE.md

Read `SPEC.md` before doing anything. It defines the goal, the design decisions, and the milestones.

## How we work
- Work on **one milestone per session**, in order (M0 → M5). Stop at the milestone's definition of done and summarize what was built and how to verify it.
- The design decisions in SPEC.md are fixed. If one blocks you, stop and ask instead of working around it.
- Prefer simple, readable code over abstraction. This is a 2-day build.
- Every eval run writes a timestamped folder under `results/` with a `config.json` (retriever, models, thresholds, git commit) so every number is reproducible.

## Hard rules
- **Never overwrite hand-checked data** in `data/eval/`. `gen_*` scripts need `--force` to overwrite.
- **Never invent, estimate, or hand-type results.** Numbers come only from eval scripts writing to `results/`.
- **Never modify files in `data/notes/`** from app code. Notes are read-only to the app.
- **Never tune on the full eval set.** Use a small dev split (~10 questions) for thresholds; report on the rest.
- The app itself must make **no network calls except to the local llama-server**. Only `scripts/gen_*` and the eval judge may call the Claude API.
- **LangSmith tracing is always off.** The app forces `LANGCHAIN_TRACING_V2=false` / `LANGSMITH_TRACING=false` at startup; the smoke test checks it.
- **Evals are our own scripts in `eval/`**, never LangSmith or LangChain evaluators. They call each retriever, the reranker and the chain directly so every stage can be swapped and timed.
- Keep the judge prompts in `eval/prompts/` so they can be read and audited.
- **Report honestly.** Every percentage in results tables is shown with raw counts, e.g. "80% (8/10)". The README's Limitations section states the test-set sizes, that the abstention threshold was tuned on a dev split with few unanswerable questions, and that judge agreement was measured on a small hand-graded sample.

## Commands
- Smoke test (run first; nothing else in M0 starts until it passes): `uv run python scripts/smoke_test.py`
- Setup: `uv sync`, then `uv run python scripts/download_models.py` (one-time model download)
- LLM server: `llama-server -m models/<qwen3-4b-instruct-q4_k_m>.gguf -ngl 99 -c 8192 --port 8080`
- Index: `uv run notecabinet index data/notes`
- Ask: `uv run notecabinet ask "question"`
- API + UI: `uv run uvicorn notecabinet.api:app --reload`
- Evals: `uv run notecabinet eval ask` / `uv run notecabinet eval organize`
- Tests: `uv run pytest`

## Environment
- `ANTHROPIC_API_KEY` and `JUDGE_MODEL` for dataset generation and judging only. They live in `.env` (gitignored) and are loaded per command with `uv run --env-file .env ...` — never for the app itself.
- `LLM_URL` (default `http://localhost:8080`).
- `HF_HUB_OFFLINE=1` when running the app, so models load from the local cache only.
- Fedora Linux, RTX 4060 (8 GB VRAM). Keep the LLM + embedder + reranker within that budget.

## Layout
```
notecabinet/   # package: index.py, retrieve.py, ask.py, organize.py, api.py, cli.py
scripts/       # smoke_test.py, download_models.py (committed); gen_*.py, common.py, review_qa.py (local only, gitignored)
eval/          # eval_ask.py, eval_organize.py, prompts/ (packaged in pyproject so `notecabinet eval` can import it)
data/          # bible.md, notes/, eval/
results/       # eval outputs (committed: the summary tables; gitignored: raw logs)
static/        # index.html
tests/
```
