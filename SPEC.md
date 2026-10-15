# NoteCabinet — Mini Version Spec

App name: **NoteCabinet**. CLI command and Python package: `notecabinet`.

## Goal

A local-first AI layer over a folder of personal markdown notes, built in **2 days** as a resume-ready mini version of a larger app (cross-platform notes with LAN sync and on-device AI).

Two features, both measured:

1. **Ask** — answer questions about your notes with citations, and say "not in your notes" when the answer isn't there.
2. **Organize page** — turn one messy, shorthand-heavy page into a structured view, without dropping or inventing facts, using retrieval over other notes to resolve personal shorthand.

What makes it resume-worthy is the **evaluation**, not the UI: a benchmark, an ablation table, and faithfulness metrics.

## Non-negotiable design decisions

These carry forward to the full app. Do not change them without asking.

1. **Raw markdown files are the source of truth.** The app never modifies them.
2. **AI output is a derived view.** "Organize" produces a separate view; it never overwrites the note. Organize output is **computed on request and not stored** anywhere (not in the index, not on disk).
3. **One SQLite file holds the whole index** (FTS5 for keywords + sqlite-vec for vectors). It is rebuildable from the notes at any time, and holds nothing that isn't.
4. **All inference at app runtime is local** (llama.cpp + local embedding/reranker models). A cloud API is used only offline, for generating the synthetic dataset and as the eval judge — never by the app itself. Model weights are downloaded once by a script; the app runs with `HF_HUB_OFFLINE=1` and the UI loads nothing from a CDN.
5. **Every answer and every organized line links back to its source** (note path + character span).

## Stack

| Piece | Choice |
|---|---|
| Language / env | Python 3.11+, `uv` |
| API + minimal UI | FastAPI, one static HTML page |
| Index | SQLite: FTS5 (BM25) + `sqlite-vec` |
| Embeddings | `BAAI/bge-small-en-v1.5` (sentence-transformers, GPU) |
| Word list (shorthand detection) | `wordfreq` English word list (offline after install) |
| Reranker | `BAAI/bge-reranker-base` (cross-encoder, fp16) |
| LLM | `llama-server` (llama.cpp, CUDA), **Qwen3-4B-Instruct-2507** (non-thinking), Q4_K_M GGUF, on the RTX 4060 |
| Structured output | llama-server JSON-schema constrained decoding |
| Generation settings | temperature 0, fixed seed, for the app and all evals |
| Dataset generation + eval judge | Claude API (different model family from the app's LLM, to avoid circular eval). Model set via `JUDGE_MODEL` env var |

## Data layout

```
data/
  bible.md                 # hand-written world bible (ground truth), every fact has an ID
  notes/                   # ~100 generated messy notes, YYYY-MM-DD-slug.md with frontmatter
  eval/
    note_facts.json        # {note_path: [fact_id, ...]}, written by gen_notes.py
    note_shorthand.json    # {note_path: [{glossary_id, abbrev, original}]}, written by gen_notes.py
    qa.jsonl               # ~60 questions: {id, question, answer, fact_ids, source_notes, type, split}
    organize/              # ~20 pages: {id}.raw.md + {id}.facts.json + {id}.shorthand.json
index/notes.db             # generated, gitignored
results/                   # eval outputs, one timestamped folder per run + config.json
```

Note frontmatter: `title`, `date`, `tags`.

### Bible format
- Every fact is one bullet with a stable ID and a date: `- [F012] (wk3, 2025-10-14) Midterm for CS229 moved to Oct 20.`
- A fact that changes over time is a new fact that names the one it replaces: `- [F031] (wk5) p2 switched from PyTorch to JAX. supersedes F009`
- The shorthand glossary is a table: `abbrev | meaning`. Glossary entries also get IDs (`G01`…).

### Organize ground truth
- `{id}.facts.json`: `[{fact_id, text}]` — the clean facts the page was degraded from.
- `{id}.shorthand.json`: `{abbrev: meaning}` for every glossary abbreviation used on the page.

## Milestones (definition of done for each)

### M0 — Synthetic dataset (Day 1, ~2.5h)
- **First step: environment smoke test.** `scripts/smoke_test.py` checks that:
  - Python's `sqlite3` supports `enable_load_extension`, and `sqlite-vec` loads and runs a vector query;
  - FTS5 is available;
  - CUDA is visible to torch;
  - llama-server responds at `LLM_URL` (warn, don't fail, if it isn't running).
  - It prints a clear PASS/FAIL per check. **Nothing else in M0 starts until it passes.**
- **Shivesh writes `data/bible.md` by hand (~45 min):** a fictional grad student over a 10-week quarter — 3 courses, 2 projects, a TA job, ~8 recurring people, a personal shorthand glossary (≥15 abbreviations), and a dated timeline of facts and decisions, including at least 3 facts that change over time. Use the format above.
- `scripts/download_models.py`: fetches the embedder and reranker into the local Hugging Face cache (the only time the app's models touch the network).
- `scripts/gen_notes.py`: generates ~100 notes from the bible across types (lecture, meeting, project log, todo, reading, idea), each drawing on facts valid at its date. Prompt for shorthand, fragments, arrows, "??"; then a programmatic messiness pass (typos, dropped punctuation, glossary abbreviations).
  - Each note's generation request names the fact IDs it must include; the script writes them to `data/eval/note_facts.json`.
  - Every glossary abbreviation must appear in at least 3 notes in a context that makes its meaning recoverable (so Organize retrieval has something to find).
  - Random noise in the messiness pass (typos, dropped punctuation, casing) must never touch dates, numbers, or names, so facts stay recoverable.
  - Glossary substitutions **are** allowed, including names → abbreviations (e.g. the advisor's name → "R"), and must only use entries from the bible's glossary.
  - Every substitution is recorded per note in `data/eval/note_shorthand.json` as `{note_path: [{glossary_id, abbrev, original}]}`.
- `scripts/gen_qa.py`: generates ~60 questions **from the bible**, typed: `single` (~20), `multi` (~15), `temporal` (~10), `shorthand` (~5), `unanswerable` (~12, ≈20%).
  - Each question records the `fact_ids` it depends on; `source_notes` is derived from `note_facts.json`, never guessed by the LLM.
  - Temporal questions carry an explicit time anchor ("as of week 6", "at the end of the quarter").
  - Unanswerable questions must be plausible for this person but about facts absent from the bible.
  - Assigns `split`: a **dev split of 10 questions, stratified by type** (includes ≥2 `unanswerable`); the rest are `test`.
- `scripts/gen_organize.py`: ~20 pages built clean-then-degraded — pick a clean fact list from the bible first, then degrade it into a messy page. Store the clean facts and the abbreviations used as ground truth.
- All `gen_*` scripts **refuse to overwrite existing output** unless passed `--force`, so hand-checked data is never lost.
- **Shivesh hand-checks every QA pair (~45 min)** and fixes or drops bad ones. For answerable questions, confirm the answer is actually in the listed source notes. For `unanswerable` questions, grep the notes to confirm the generator didn't invent the answer.
- Done when: files exist, a sample of notes looks genuinely messy, all QA pairs are verified.

### M1 — Indexing (Day 1, ~2h)
- Parse frontmatter; chunk by heading/paragraph to ~300 tokens (counted with the bge tokenizer) with small overlap; keep char spans.
- Text embedded and shown to the LLM is prefixed with the note's title and date; spans refer to the raw note body only.
- Write chunks to SQLite: FTS5 table + sqlite-vec table + metadata (path, date, span).
- `notecabinet index data/notes` rebuilds the DB; re-indexing skips unchanged files by content hash, removes chunks of deleted files, and does a full rebuild if the chunker or embedding model changes (stored in a `meta` table).
- Done when: indexing all notes works and a test confirms spans map back to the exact source text.

### M2 — Retrieval + Ask (Day 1, ~3h)
- Retrievers: `bm25`, `dense`, `hybrid` (Reciprocal Rank Fusion, k=60), `hybrid+rerank` (rerank top 30 → keep 5). Non-rerank retrievers keep their top 5. Selectable by config.
- Ask: retrieved chunks → prompt → llama-server → answer with inline citations `[n]` mapped to note path + span.
- Abstention: return `NOT_FOUND` if either
  - the top **reranker score** over the final 5 chunks is below a threshold tuned on the dev split. The reranker scores the final chunks for **every** retriever (for non-rerank retrievers it only scores, it does not reorder), so one threshold applies across the ablation; or
  - the model's answer is exactly `NOT_FOUND` (the prompt instructs this).
- Endpoints: `POST /ask`, `POST /organize` (M4), `GET /notes` (list), `GET /notes/{path}` (raw text, for highlighting cited spans). CLI `notecabinet ask "..."`.
- Done when: answers carry valid citations and unanswerable questions abstain on manual spot checks.

### M3 — Ask evaluation (Day 2, ~3h)
- All metrics are reported on the `test` split only.
- Retrieval metrics (answerable questions only), computed over the deduplicated notes from the top-5 chunks:
  - **Primary — fact-level recall@5:** a fact is covered if at least one note containing it (per `data/eval/note_facts.json`) is among the retrieved notes. Report both:
    - **all facts covered:** fraction of questions where every one of its `fact_ids` is covered;
    - **mean per-fact coverage:** fraction of a question's facts covered, averaged over questions.
  - **Secondary — note-level MRR:** reciprocal rank of the first retrieved note that contains any of the question's facts.
- Answer metrics (LLM judge, prompt in `eval/prompts/`): correctness vs. gold answer, faithfulness to retrieved chunks.
- Abstention: precision and recall of `NOT_FOUND` against `unanswerable` (precision penalizes abstaining on answerable questions).
- **Ablation table:** bm25 / dense / hybrid / hybrid+rerank, broken down by question type.
- Latency: p50/p95 for retrieval, rerank, and generation separately (after one warm-up query).
- Validate the judge: Shivesh hand-grades 15 answers and reports agreement with the judge (% agreement and Cohen's κ).
- Done when: `notecabinet eval ask` writes a results folder with tables and config.

### M4 — Organize page + evaluation (Day 2, ~3h)
- Prompt input: the raw page with each line numbered `[L1]`, `[L2]`…, plus retrieved shorthand context with each chunk numbered `[C1]`, `[C2]`….
- Output JSON schema (enforced by constrained decoding): `title`, `sections[{heading, items[{text, sources, uncertain}]}]`, `action_items[{text, sources}]`, `open_questions[{text, sources}]`. `sources` is a list restricted by the schema to the valid `L*`/`C*` IDs for that request; code maps each ID to note path + character span.
- Shorthand resolution: detect likely abbreviations on the page (tokens of 2–5 characters that are all-caps, contain a digit, or are not dictionary words — "not a dictionary word" means below a frequency cutoff in the `wordfreq` English word list), retrieve chunks from **other** notes containing them, pass as "possible meanings" context. Unclear items must be marked `uncertain`, never guessed.
- Render JSON → markdown; UI shows raw and organized side by side.
- Eval on the ~20 pages (LLM judge, prompts in `eval/prompts/`):
  - **Coverage:** % of ground-truth clean facts the judge finds expressed in the output.
  - **Hallucination rate:** % of output items the judge finds unsupported by the raw page plus retrieved context.
  - **Shorthand accuracy:** % of abbreviations in `{id}.shorthand.json` expanded correctly in the output.
  - Compare **with vs. without retrieval**.
- No thresholds or prompts are tuned on these 20 pages; prompt iteration uses 3 extra pages generated separately as a dev set.
- Validate the judge: Shivesh hand-grades 3 pages' outputs and reports agreement.
- Done when: `notecabinet eval organize` writes results; the with/without-retrieval comparison exists.

### M5 — Demo + README (Day 2, ~2h)
- Single HTML page: notes list, Ask box with clickable citations, Organize button with side-by-side view.
- README: problem, architecture diagram, design decisions, **results tables from M3/M4**, limitations, roadmap (sync, Android, tiered inference across devices), how to reproduce.
- Record a demo GIF.

## Reproducibility
Each eval run's `config.json` records: retriever, models (LLM file, embedder, reranker, `JUDGE_MODEL`), thresholds, sampling settings, git commit, a hash of `data/eval/`, and hashes of every prompt used.

## Reporting (applies to M3 and M4)
- Every percentage in results tables is shown with raw counts, e.g. "80% (8/10)".
- The README has a Limitations section that states the test-set sizes, that the abstention threshold was tuned on a dev split with few unanswerable questions, and that judge agreement was measured on a small hand-graded sample.

## Cut list if behind schedule
Cut in this order:
1. **Incremental indexing:** keep the `meta`-table model/chunker check, but always do a full rebuild instead of hash-based skipping/deletion.
2. **Organize judge validation** on 3 hand-graded pages: defer to after Day 2.
3. **Cohen's κ:** report % agreement only.

**Never cut:** the dev/test split, the hand-checking of QA pairs, and the with/without-retrieval comparison for Organize.

## Out of scope for the mini version
Summarization, sync/CRDTs, Android/Windows clients, encryption, auth, multiple chunking strategies, fine-tuning.

## Resume bullet templates (fill only with real numbers from `results/`)
- Built a local-first RAG system over personal notes with hybrid BM25 + vector retrieval in SQLite, cross-encoder reranking, and cited answers; reranked hybrid retrieval raised fact-level recall@5 from [X]% (dense) to [Y]% on a [N]-question benchmark, with [P]% / [R]% abstention precision/recall on unanswerable queries.
- Built context-aware page restructuring with schema-constrained decoding and retrieval over the user's other notes to resolve personal shorthand, preserving [A]% of source facts at a [B]% hallucination rate; retrieval improved shorthand resolution from [C]% to [D]%.
