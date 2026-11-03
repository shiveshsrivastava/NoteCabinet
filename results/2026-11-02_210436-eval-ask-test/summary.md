# Ask eval: test split (51 questions: 41 answerable, 10 unanswerable)

Judge `claude-haiku-5-5`; abstention threshold 0.0101; top 5 chunks; commit `e58e735`. Full settings in `config.json`, every number in `metrics.json`.

## Retrieval (answerable questions; top-5 chunks reduced to distinct notes)

**All facts covered** = every fact the question needs is in a retrieved note. **Mean per-fact coverage** and **MRR** are averages over questions.

| retriever | all facts covered | mean per-fact coverage | MRR |
|---|---|---|---|
| bm25 | 73% (30/41) | 0.85 (n=41) | 0.74 (n=41) |
| dense | 61% (25/41) | 0.69 (n=41) | 0.64 (n=41) |
| hybrid | 73% (30/41) | 0.78 (n=41) | 0.70 (n=41) |
| hybrid+rerank | 80% (33/41) | 0.89 (n=41) | 0.82 (n=41) |

All facts covered, by question type:

| retriever | single | multi | temporal | shorthand |
|---|---|---|---|---|
| bm25 | 94% (16/17) | 50% (6/12) | 50% (4/8) | 100% (4/4) |
| dense | 71% (12/17) | 58% (7/12) | 50% (4/8) | 50% (2/4) |
| hybrid | 82% (14/17) | 75% (9/12) | 62% (5/8) | 50% (2/4) |
| hybrid+rerank | 94% (16/17) | 58% (7/12) | 75% (6/8) | 100% (4/4) |

## Answers (LLM judge)

**Correct** is over answerable questions (abstaining counts as incorrect). **Faithful** is over the answers actually given, including answers to unanswerable questions.

| retriever | correct | faithful | answers citing a missing excerpt | judge errors |
|---|---|---|---|---|
| bm25 | 61% (25/41) | 67% (24/36) | 0 | 0 |
| dense | 39% (16/41) | 62% (18/29) | 0 | 0 |
| hybrid | 51% (21/41) | 72% (23/32) | 0 | 0 |
| hybrid+rerank | 66% (27/41) | 61% (23/38) | 0 | 0 |

Correct, by question type:

| retriever | single | multi | temporal | shorthand |
|---|---|---|---|---|
| bm25 | 94% (16/17) | 17% (2/12) | 38% (3/8) | 100% (4/4) |
| dense | 71% (12/17) | 0% (0/12) | 38% (3/8) | 25% (1/4) |
| hybrid | 76% (13/17) | 25% (3/12) | 38% (3/8) | 50% (2/4) |
| hybrid+rerank | 82% (14/17) | 25% (3/12) | 75% (6/8) | 100% (4/4) |

## Abstention (`NOT_FOUND`)

Precision: of all abstentions, how many were on unanswerable questions. Recall: of the unanswerable questions, how many were abstained on.

| retriever | precision | recall | unanswerable caught: gate / model | answerable wrongly abstained: gate / model |
|---|---|---|---|---|
| bm25 | 67% (10/15) | 100% (10/10) | 0 / 10 | 1 / 4 |
| dense | 45% (10/22) | 100% (10/10) | 0 / 10 | 4 / 8 |
| hybrid | 53% (10/19) | 100% (10/10) | 0 / 10 | 3 / 6 |
| hybrid+rerank | 77% (10/13) | 100% (10/10) | 0 / 10 | 1 / 2 |

Unanswerable questions by hand-labelled kind (`data/eval/unanswerable_kind.json`):

| retriever | kind | questions | abstained by gate | abstained by model | answered |
|---|---|---|---|---|---|
| bm25 | off_topic | 0 | n/a (0/0) | n/a (0/0) | n/a (0/0) |
| bm25 | near_miss | 10 | 0% (0/10) | 100% (10/10) | 0% (0/10) |
| dense | off_topic | 0 | n/a (0/0) | n/a (0/0) | n/a (0/0) |
| dense | near_miss | 10 | 0% (0/10) | 100% (10/10) | 0% (0/10) |
| hybrid | off_topic | 0 | n/a (0/0) | n/a (0/0) | n/a (0/0) |
| hybrid | near_miss | 10 | 0% (0/10) | 100% (10/10) | 0% (0/10) |
| hybrid+rerank | off_topic | 0 | n/a (0/0) | n/a (0/0) | n/a (0/0) |
| hybrid+rerank | near_miss | 10 | 0% (0/10) | 100% (10/10) | 0% (0/10) |

## Latency (ms, p50 / p95, after one warm-up query)

Generation is counted only where it ran (the score gate skips it).

| retriever | retrieval | rerank | generation |
|---|---|---|---|
| bm25 | 0 / 1 (n=51) | 26 / 29 (n=51) | 900 / 2,144 (n=50) |
| dense | 8 / 11 (n=51) | 25 / 26 (n=51) | 907 / 1,976 (n=47) |
| hybrid | 8 / 11 (n=51) | 24 / 27 (n=51) | 903 / 1,892 (n=48) |
| hybrid+rerank | 8 / 10 (n=51) | 116 / 127 (n=51) | 1,048 / 2,116 (n=50) |
