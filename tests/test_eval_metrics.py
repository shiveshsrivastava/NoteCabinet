"""Eval metric functions on small hand-made examples (no models, no index)."""

import pytest

from eval.metrics import abstention_counts, count, notes_by_fact, pct, percentile, ranked_notes, retrieval_metrics

NOTE_FACTS = {
    "a.md": ["F1", "F2"],
    "b.md": ["F2"],
    "c.md": ["F3"],
    "d.md": [],
}
FACT_NOTES = notes_by_fact(NOTE_FACTS)


def test_notes_by_fact_inverts_the_mapping():
    assert FACT_NOTES == {"F1": {"a.md"}, "F2": {"a.md", "b.md"}, "F3": {"c.md"}}


def test_ranked_notes_dedupes_and_keeps_first_rank():
    assert ranked_notes(["d.md", "a.md", "d.md", "c.md", "a.md"]) == ["d.md", "a.md", "c.md"]


def test_single_fact_found_at_rank_one():
    m = retrieval_metrics(["F3"], ["c.md", "d.md"], FACT_NOTES)
    assert m["all_covered"] and m["coverage"] == 1.0
    assert m["first_relevant_rank"] == 1 and m["reciprocal_rank"] == 1.0


def test_rank_counts_distinct_notes_not_chunks():
    # Three chunks of d.md come first, but they are one note: c.md is note rank 2, not chunk rank 4.
    m = retrieval_metrics(["F3"], ["d.md", "d.md", "d.md", "c.md"], FACT_NOTES)
    assert m["first_relevant_rank"] == 2 and m["reciprocal_rank"] == 0.5


def test_fact_covered_by_any_note_that_contains_it():
    # F2 is in both a.md and b.md; retrieving b.md alone covers it.
    m = retrieval_metrics(["F2"], ["d.md", "b.md"], FACT_NOTES)
    assert m["all_covered"] and m["first_relevant_rank"] == 2


def test_partial_coverage_of_a_multi_fact_question():
    m = retrieval_metrics(["F1", "F2", "F3"], ["b.md", "d.md"], FACT_NOTES)
    assert (m["n_facts"], m["n_covered"]) == (3, 1)
    assert not m["all_covered"]
    assert m["coverage"] == pytest.approx(1 / 3)
    assert m["reciprocal_rank"] == 1.0  # b.md has one of the question's facts


def test_one_note_can_cover_several_facts():
    m = retrieval_metrics(["F1", "F2"], ["d.md", "a.md"], FACT_NOTES)
    assert m["all_covered"] and m["n_covered"] == 2 and m["reciprocal_rank"] == 0.5


def test_nothing_relevant_retrieved():
    m = retrieval_metrics(["F1", "F3"], ["d.md"], FACT_NOTES)
    assert m["n_covered"] == 0 and not m["all_covered"] and m["coverage"] == 0.0
    assert m["first_relevant_rank"] is None and m["reciprocal_rank"] == 0.0


def test_empty_retrieval():
    m = retrieval_metrics(["F1"], [], FACT_NOTES)
    assert m["coverage"] == 0.0 and m["reciprocal_rank"] == 0.0


def test_unanswerable_questions_are_rejected():
    with pytest.raises(ValueError):
        retrieval_metrics([], ["a.md"], FACT_NOTES)


def test_pct_always_shows_raw_counts():
    assert pct(8, 10) == "80% (8/10)"
    assert pct(1, 3) == "33% (1/3)"
    assert pct(0, 0) == "n/a (0/0)"


def test_count_skips_not_applicable():
    assert count([True, False, None, True]) == (2, 3)
    assert count([None]) == (0, 0)


def test_percentile_interpolates_and_handles_empty():
    assert percentile([10, 20, 30, 40], 50) == 25
    assert percentile([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 95) == pytest.approx(9.55)
    assert percentile([], 50) is None


def test_abstention_precision_and_recall():
    rows = [{"abstained": True, "unanswerable": True},    # caught
            {"abstained": True, "unanswerable": False},   # wrongly abstained -> hurts precision
            {"abstained": False, "unanswerable": True},   # answered an unanswerable -> hurts recall
            {"abstained": False, "unanswerable": False}]
    a = abstention_counts(rows)
    assert (a["tp"], a["fp"], a["fn"]) == (1, 1, 1)
    assert a["precision"] == (1, 2) and a["recall"] == (1, 2)
