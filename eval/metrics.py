"""Metric functions for the evals. Plain Python, no models, so they can be unit-tested on hand-made examples.

Retrieval metrics work on notes, not chunks: the top-5 chunks are reduced to the distinct notes they come
from, in rank order, and a note "contains" a fact if data/eval/note_facts.json says so.
"""

import numpy as np


def pct(k, n):
    """A rate with its raw counts, e.g. "80% (8/10)". Every percentage in a results table uses this."""
    return f"{k / n:.0%} ({k}/{n})" if n else "n/a (0/0)"


def count(values):
    """(true, total) over booleans, skipping None (not applicable, or a judge error)."""
    known = [v for v in values if v is not None]
    return sum(known), len(known)


def mean(values):
    return float(np.mean(values)) if values else None


def percentile(values, p):
    """p-th percentile with linear interpolation (numpy's default); None for no values."""
    return float(np.percentile(values, p)) if values else None


def abstention_counts(rows):
    """Abstaining is the positive class: precision penalizes abstaining on answerable questions,
    recall penalizes answering unanswerable ones. rows need "abstained" and "unanswerable"."""
    tp = sum(r["abstained"] and r["unanswerable"] for r in rows)
    fp = sum(r["abstained"] and not r["unanswerable"] for r in rows)
    fn = sum(not r["abstained"] and r["unanswerable"] for r in rows)
    return {"tp": tp, "fp": fp, "fn": fn, "precision": (tp, tp + fp), "recall": (tp, tp + fn)}


def ranked_notes(paths):
    """Distinct note paths in order of first appearance (the top-5 chunks can share a note)."""
    return list(dict.fromkeys(paths))


def notes_by_fact(note_facts):
    """{fact_id: {note_path, ...}} from note_facts.json's {note_path: [fact_id, ...]}."""
    out = {}
    for path, facts in note_facts.items():
        for f in facts:
            out.setdefault(f, set()).add(path)
    return out


def retrieval_metrics(fact_ids, retrieved_paths, fact_notes):
    """Fact-level recall@k and note-level reciprocal rank for one answerable question.

    fact_ids: the question's facts. retrieved_paths: note paths of the top-k chunks, best first.
    fact_notes: notes_by_fact(note_facts).

    - all_covered: every fact is in at least one retrieved note.
    - coverage: fraction of the question's facts that are covered.
    - reciprocal_rank: 1/rank of the first retrieved note (ranked among distinct notes) containing
      any of the question's facts; 0 if none does.
    """
    if not fact_ids:
        raise ValueError("retrieval metrics are for answerable questions, which always have fact_ids")
    notes = ranked_notes(retrieved_paths)
    covered = [f for f in fact_ids if fact_notes.get(f, set()) & set(notes)]
    relevant = set().union(*(fact_notes.get(f, set()) for f in fact_ids))
    rank = next((i for i, n in enumerate(notes, 1) if n in relevant), None)
    return {
        "n_facts": len(fact_ids),
        "n_covered": len(covered),
        "all_covered": len(covered) == len(fact_ids),
        "coverage": len(covered) / len(fact_ids),
        "first_relevant_rank": rank,
        "reciprocal_rank": 1 / rank if rank else 0.0,
    }
