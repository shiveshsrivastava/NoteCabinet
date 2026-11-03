"""Validate the LLM judge against hand grades on a small sample of one Ask eval run.

  sample RUN_DIR   pick 15 judged answers and write a blind grading sheet (no judge verdicts on it):
                   RUN_DIR/judge_check/sheet.md (you fill it in) + key.json (which answer each item is)
  score RUN_DIR    read your grades, compare with the judge: % agreement and Cohen's kappa per judge
                   -> RUN_DIR/judge_check/agreement.md + agreement.json (self-contained: verdicts included)

The sample is 15 answers to 15 different questions, spread over question types and retrievers, and
balanced over the judge's correct/faithful verdicts so both labels occur (kappa needs that). Because
of that balancing, agreement is measured on a sample richer in "incorrect"/"unfaithful" verdicts than
the full run; agreement.md says so.

Usage: uv run python -m eval.judge_check sample results/<run>
       uv run python -m eval.judge_check score results/<run>
"""

import argparse
import json
import random
import re
from pathlib import Path

from eval.metrics import cohens_kappa, pct

SEED = 1234
PER_TYPE = {"single": 5, "multi": 4, "temporal": 4, "shorthand": 2}  # 15 items
CELLS = [(True, True), (False, False), (True, False), (False, True)]  # (correct, faithful), cycled for balance
YES = {"yes", "y", "correct", "faithful", "1", "true"}
NO = {"no", "n", "incorrect", "unfaithful", "0", "false"}

INSTRUCTIONS = """# Judge check: hand grading sheet

Grade each answer yourself, **without** looking at the judge's verdicts (they are not on this sheet),
using the same rules the judge was given (`eval/prompts/judge_correctness.md`, `judge_faithfulness.md`):

- **correct** (`yes`/`no`): compared with the gold answer, the system answer gives everything the
  question asks for and contradicts nothing in the gold. Background in the gold that the question
  doesn't ask for may be left out, but must not be stated wrongly. Extra details are fine unless they
  contradict the gold. Wording and citation markers like [2] don't matter.
- **faithful** (`yes`/`no`): every factual claim in the answer (names, dates, times, numbers, places,
  decisions, events) is stated in the excerpts or follows directly from them. Expanding an abbreviation
  counts as supported only if the excerpts show what it means. Ignore correctness and which excerpt a
  citation number points to.

Fill in the `correct:` and `faithful:` lines under each item (`yes` or `no`). `note:` is optional.
Then run `uv run python -m eval.judge_check score <run folder>`.
"""


def load_rows(run):
    return [json.loads(line) for line in (run / "raw" / "per_question.jsonl").read_text().splitlines()]


def sample(rows, seed=SEED):
    """15 judged answers (answerable, answered, judged by both judges), one per question."""
    pool = [r for r in rows if not r["unanswerable"] and not r["abstained"]
            and r["correct"] is not None and r["faithful"] is not None]
    random.Random(seed).shuffle(pool)
    picked, used_q, per_retriever = [], set(), {}
    for qtype, n in PER_TYPE.items():
        for i in range(n):
            for cell in CELLS[i % 4:] + CELLS[:i % 4]:  # preferred cell first, then the others
                cands = [r for r in pool if r["type"] == qtype and r["id"] not in used_q
                         and (r["correct"], r["faithful"]) == cell]
                if cands:
                    best = min(cands, key=lambda r: per_retriever.get(r["retriever"], 0))  # spread retrievers
                    picked.append(best)
                    used_q.add(best["id"])
                    per_retriever[best["retriever"]] = per_retriever.get(best["retriever"], 0) + 1
                    break
    random.Random(seed + 1).shuffle(picked)  # so items aren't grouped by type
    return picked


def render_sheet(items):
    parts = [INSTRUCTIONS]
    for i, r in enumerate(items, 1):
        parts.append(f"""---

## G{i:02d}

**Question:** {r['question']}

**Gold answer:** {r['gold']}

**System answer:** {r['answer']}

**Excerpts the system saw:**

```text
{r['excerpts']}
```

correct:
faithful:
note:
""")
    return "\n".join(parts)


def parse_sheet(text):
    """{item: {"correct": bool, "faithful": bool, "note": str}}; raises listing every unfilled/unclear line.

    The excerpts are real notes with their own "## ..." headings and lines, so items are split only on
    exact "## G01" headings, and grade lines are read only after the excerpts' closing fence."""
    grades, problems = {}, []
    parts = re.split(r"^## (G\d{2})[ \t]*$", text, flags=re.M)
    for item, block in zip(parts[1::2], parts[2::2]):
        block = block.rsplit("```", 1)[-1]
        g = {}
        for field in ("correct", "faithful"):
            m = re.search(rf"^{field}:[ \t]*(\S*)[ \t]*$", block, flags=re.M)
            value = m.group(1).lower() if m else ""
            if value in YES:
                g[field] = True
            elif value in NO:
                g[field] = False
            else:
                problems.append(f"{item} {field}: {value or '(empty)'}")
        note = re.search(r"^note:[ \t]*(.*)$", block, flags=re.M)
        g["note"] = note.group(1).strip() if note else ""
        grades[item] = g
    if problems:
        raise ValueError("fill in yes/no for: " + "; ".join(problems))
    return grades


def agreement(pairs):
    """pairs: [(human, judge)] booleans -> counts, % agreement, kappa."""
    human, judge = [h for h, _ in pairs], [j for _, j in pairs]
    k = cohens_kappa(human, judge)
    return {"n": len(pairs), "agree": sum(h == j for h, j in pairs), "kappa": k,
            "human_yes": sum(human), "judge_yes": sum(judge),
            "human_yes_judge_no": sum(h and not j for h, j in pairs),
            "human_no_judge_yes": sum(j and not h for h, j in pairs)}


def cmd_sample(run, force):
    out = run / "judge_check"
    sheet = out / "sheet.md"
    if sheet.exists() and not force:  # it may hold hand grades: never overwrite silently
        raise SystemExit(f"{sheet} already exists (it may contain your grades); pass --force to replace it")
    items = sample(load_rows(run))
    out.mkdir(exist_ok=True)
    sheet.write_text(render_sheet(items))
    key = [{"item": f"G{i:02d}", "retriever": r["retriever"], "id": r["id"], "type": r["type"]}
           for i, r in enumerate(items, 1)]
    (out / "key.json").write_text(json.dumps({"seed": SEED, "per_type": PER_TYPE, "items": key}, indent=2) + "\n")
    print(f"{len(items)} items -> {sheet}")


def cmd_score(run):
    out = run / "judge_check"
    grades = parse_sheet((out / "sheet.md").read_text())
    key = json.loads((out / "key.json").read_text())["items"]
    rows = {(r["retriever"], r["id"]): r for r in load_rows(run)}
    items = []
    for k in key:
        r, g = rows[(k["retriever"], k["id"])], grades[k["item"]]
        items.append({**k, "human_correct": g["correct"], "judge_correct": r["correct"],
                      "human_faithful": g["faithful"], "judge_faithful": r["faithful"], "note": g["note"],
                      "judge_reasons": {j: v["reason"] for j, v in r["judge"].items()}})
    result = {kind: agreement([(i[f"human_{kind}"], i[f"judge_{kind}"]) for i in items])
              for kind in ("correct", "faithful")}
    (out / "agreement.json").write_text(json.dumps({"agreement": result, "items": items}, indent=2) + "\n")

    def kappa(x):
        return "undefined (one label only)" if x is None else f"{x:.2f}"

    lines = ["# Judge check: hand grades vs. LLM judge", "",
             f"{len(items)} answers from this run, graded by hand without seeing the judge's verdicts. "
             "The sample is balanced over the judge's verdicts (so both labels occur), which makes it richer in "
             "incorrect/unfaithful answers than the full run.", "",
             "| judge | agreement | Cohen's kappa | yes: human / judge | human yes, judge no | human no, judge yes |",
             "|---|---|---|---|---|---|"]
    for kind, a in result.items():
        lines.append(f"| {kind}ness | {pct(a['agree'], a['n'])} | {kappa(a['kappa'])} | {a['human_yes']} / "
                     f"{a['judge_yes']} | {a['human_yes_judge_no']} | {a['human_no_judge_yes']} |")
    lines += ["", "## Disagreements", ""]
    dis = [(i, kind) for i in items for kind in ("correct", "faithful") if i[f"human_{kind}"] != i[f"judge_{kind}"]]
    if not dis:
        lines.append("None.")
    for i, kind in dis:
        reason = i["judge_reasons"].get("correctness" if kind == "correct" else "faithfulness", "")
        lines += [f"- **{i['item']}** ({i['id']}, {i['type']}, {i['retriever']}), {kind}ness: "
                  f"you {'yes' if i[f'human_{kind}'] else 'no'}, judge {'yes' if i[f'judge_{kind}'] else 'no'}. "
                  f"Judge: {reason}" + (f" Your note: {i['note']}" if i["note"] else "")]
    (out / "agreement.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[5:9]))


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m eval.judge_check", description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_sample = sub.add_parser("sample")
    p_sample.add_argument("run", type=Path)
    p_sample.add_argument("--force", action="store_true", help="replace an existing sheet (and its grades)")
    sub.add_parser("score").add_argument("run", type=Path)
    args = parser.parse_args(argv)
    if args.cmd == "sample":
        cmd_sample(args.run, args.force)
    else:
        cmd_score(args.run)


if __name__ == "__main__":
    main()
