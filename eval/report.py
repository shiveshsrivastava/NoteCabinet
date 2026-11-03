"""Ask eval report: turn raw/per_question.jsonl rows into metrics.json and summary.md.

metrics.json holds every number (rates as [k, n] pairs) so the README can quote them without retyping;
summary.md renders the same numbers as tables, every percentage with its raw counts.
"""

import json

from eval.metrics import abstention_counts, count, mean, pct, percentile

TYPES = ("single", "multi", "temporal", "shorthand")
KINDS = ("off_topic", "near_miss")  # both always shown, even when a split has none of a kind
STAGES = ("retrieval", "rerank", "generation")


def _retrieval(rows):
    m = [r["retrieval"] for r in rows]
    return {"n": len(m), "all_covered": count([x["all_covered"] for x in m]),
            "mean_coverage": mean([x["coverage"] for x in m]), "mrr": mean([x["reciprocal_rank"] for x in m])}


def _answers(rows):
    return {"correct": count([r["correct"] for r in rows]), "faithful": count([r["faithful"] for r in rows])}


def _latency(rows):
    out = {}
    for stage in STAGES:
        # Generation is timed only when it ran: the score gate skips it, and a 0 would flatter the percentiles.
        vals = [r["timings"][f"{stage}_ms"] for r in rows
                if stage != "generation" or r["abstain_reason"] != "low_rerank_score"]
        out[stage] = {"n": len(vals), "p50": percentile(vals, 50), "p95": percentile(vals, 95)}
    return out


def summarize(rows, kinds):
    """{retriever: metrics}. kinds: {question_id: "off_topic" | "near_miss"} (the hand labels)."""
    out = {}
    for ret in dict.fromkeys(r["retriever"] for r in rows):
        rs = [r for r in rows if r["retriever"] == ret]
        ans = [r for r in rs if not r["unanswerable"]]
        una = [r for r in rs if r["unanswerable"]]
        ab = abstention_counts(rs)
        out[ret] = {
            "retrieval": {**_retrieval(ans),
                          "by_type": {t: _retrieval([r for r in ans if r["type"] == t]) for t in TYPES}},
            "answers": {
                # correct: over answerable questions (abstaining = incorrect). faithful: over answers given.
                "correct": count([r["correct"] for r in ans]),
                "faithful": count([r["faithful"] for r in rs]),
                "judge_errors": sum("judge_error" in r for r in rs),
                "invalid_citations": sum(bool(r["invalid_citations"]) for r in rs if not r["abstained"]),
                "by_type": {t: _answers([r for r in ans if r["type"] == t]) for t in TYPES},
            },
            "abstention": {
                **ab,
                "unanswerable_by_gate": sum(r["abstain_reason"] == "low_rerank_score" for r in una),
                "unanswerable_by_model": sum(r["abstain_reason"] == "model" for r in una),
                "answerable_by_gate": sum(r["abstain_reason"] == "low_rerank_score" for r in ans),
                "answerable_by_model": sum(r["abstain_reason"] == "model" for r in ans),
                "by_kind": {k: {"n": len(g := [r for r in una if kinds.get(r["id"]) == k]),
                                "gate": sum(r["abstain_reason"] == "low_rerank_score" for r in g),
                                "model": sum(r["abstain_reason"] == "model" for r in g),
                                "answered": sum(not r["abstained"] for r in g)} for k in KINDS},
                "unlabelled": sorted({r["id"] for r in una if r["id"] not in kinds}),
            },
            "latency_ms": _latency(rs),
        }
    return out


def _table(headers, rows):
    return ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)] + \
           ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]


def _dec(x, n):
    return "n/a (n=0)" if x is None else f"{x:.2f} (n={n})"


def _ms(x):
    return "n/a" if x is None else f"{x:,.0f}"


def render(m, cfg):
    n_q, n_u = cfg["n_questions"], cfg["n_unanswerable"]
    first = next(iter(m.values()))
    n_ans = first["retrieval"]["n"]
    lines = [
        f"# Ask eval: {cfg['split']} split ({n_q} questions: {n_ans} answerable, {n_u} unanswerable)", "",
        f"Judge `{cfg['judge']['model']}`; abstention threshold {cfg['abstain_threshold']}; "
        f"top {cfg['retrieval']['final_k']} chunks; commit `{cfg['git']['commit'][:7]}`"
        f"{' (dirty)' if cfg['git']['dirty'] else ''}. Full settings in `config.json`, every number in `metrics.json`.",
        "", "## Retrieval (answerable questions; top-5 chunks reduced to distinct notes)", "",
        "**All facts covered** = every fact the question needs is in a retrieved note. "
        "**Mean per-fact coverage** and **MRR** are averages over questions.", "",
    ]
    lines += _table(["retriever", "all facts covered", "mean per-fact coverage", "MRR"],
                    [[r, pct(*s["all_covered"]), _dec(s["mean_coverage"], s["n"]), _dec(s["mrr"], s["n"])]
                     for r, s in ((r, x["retrieval"]) for r, x in m.items())])
    lines += ["", "All facts covered, by question type:", ""]
    lines += _table(["retriever", *TYPES],
                    [[r, *(pct(*x["retrieval"]["by_type"][t]["all_covered"]) for t in TYPES)] for r, x in m.items()])

    lines += ["", "## Answers (LLM judge)", "",
              "**Correct** is over answerable questions (abstaining counts as incorrect). "
              "**Faithful** is over the answers actually given, including answers to unanswerable questions.", ""]
    lines += _table(["retriever", "correct", "faithful", "answers citing a missing excerpt", "judge errors"],
                    [[r, pct(*x["answers"]["correct"]), pct(*x["answers"]["faithful"]),
                      x["answers"]["invalid_citations"], x["answers"]["judge_errors"]] for r, x in m.items()])
    lines += ["", "Correct, by question type:", ""]
    lines += _table(["retriever", *TYPES],
                    [[r, *(pct(*x["answers"]["by_type"][t]["correct"]) for t in TYPES)] for r, x in m.items()])

    lines += ["", "## Abstention (`NOT_FOUND`)", "",
              "Precision: of all abstentions, how many were on unanswerable questions. "
              "Recall: of the unanswerable questions, how many were abstained on.", ""]
    lines += _table(["retriever", "precision", "recall", "unanswerable caught: gate / model",
                     "answerable wrongly abstained: gate / model"],
                    [[r, pct(*a["precision"]), pct(*a["recall"]),
                      f"{a['unanswerable_by_gate']} / {a['unanswerable_by_model']}",
                      f"{a['answerable_by_gate']} / {a['answerable_by_model']}"]
                     for r, a in ((r, x["abstention"]) for r, x in m.items())])
    lines += ["", "Unanswerable questions by hand-labelled kind (`data/eval/unanswerable_kind.json`):", ""]
    lines += _table(["retriever", "kind", "questions", "abstained by gate", "abstained by model", "answered"],
                    [[r, k, b["n"], pct(b["gate"], b["n"]), pct(b["model"], b["n"]), pct(b["answered"], b["n"])]
                     for r, x in m.items() for k, b in x["abstention"]["by_kind"].items()])
    unlabelled = sorted({q for x in m.values() for q in x["abstention"]["unlabelled"]})
    if unlabelled:
        lines += ["", f"**Unlabelled unanswerable questions (not in either kind):** {', '.join(unlabelled)}"]

    lines += ["", "## Latency (ms, p50 / p95, after one warm-up query)", "",
              "Generation is counted only where it ran (the score gate skips it).", ""]
    lines += _table(["retriever", *STAGES],
                    [[r, *(f"{_ms(s['p50'])} / {_ms(s['p95'])} (n={s['n']})"
                           for s in (x["latency_ms"][st] for st in STAGES))] for r, x in m.items()])
    return "\n".join(lines) + "\n"


def write_report(out_dir, rows, cfg, kinds):
    m = summarize(rows, kinds)
    (out_dir / "metrics.json").write_text(json.dumps(m, indent=2) + "\n")
    (out_dir / "summary.md").write_text(render(m, cfg))
    return m
