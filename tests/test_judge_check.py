"""Judge validation: sampling, the blind sheet round-trip, and agreement counts (synthetic rows)."""

import itertools

import pytest

from eval.judge_check import PER_TYPE, agreement, parse_sheet, render_sheet, sample


def make_rows():
    rows = []
    for n, (qtype, ret, correct, faithful) in enumerate(itertools.product(
            PER_TYPE, ["bm25", "dense", "hybrid", "hybrid+rerank"], [True, False], [True, False])):
        rows.append({"id": f"q{n:03d}", "type": qtype, "retriever": ret, "unanswerable": False, "abstained": False,
                     "correct": correct, "faithful": faithful, "question": f"Q{n}?", "gold": "G",
                     "answer": "A [1]", "excerpts": "[1] Note (Mon 2025-10-13)\ntext"})
    rows.append({**rows[0], "id": "q999", "abstained": True})  # never sampled: nothing to grade
    return rows


def test_sample_is_15_distinct_questions_with_the_planned_type_mix():
    picked = sample(make_rows())
    assert len(picked) == 15 and len({r["id"] for r in picked}) == 15
    assert {t: sum(r["type"] == t for r in picked) for t in PER_TYPE} == PER_TYPE
    assert all(not r["abstained"] for r in picked)


def test_sample_has_both_labels_and_several_retrievers():
    picked = sample(make_rows())
    assert {r["correct"] for r in picked} == {True, False}
    assert {r["faithful"] for r in picked} == {True, False}
    assert len({r["retriever"] for r in picked}) == 4


def test_sample_is_deterministic():
    assert [r["id"] for r in sample(make_rows())] == [r["id"] for r in sample(make_rows())]


def test_sheet_hides_the_judge_and_round_trips():
    items = sample(make_rows())[:2]
    sheet = render_sheet(items)
    assert "verdict" not in sheet.split("---", 1)[1] and "bm25" not in sheet  # blind: no verdicts, no retriever
    with pytest.raises(ValueError, match="G01 correct"):
        parse_sheet(sheet)  # not filled in yet
    filled = sheet.replace("correct:\nfaithful:\nnote:\n", "correct: yes\nfaithful: No\nnote: close call\n", 1)
    filled = filled.replace("correct:\nfaithful:\n", "correct: n\nfaithful: faithful\n", 1)
    grades = parse_sheet(filled)
    assert grades["G01"] == {"correct": True, "faithful": False, "note": "close call"}
    assert grades["G02"]["correct"] is False and grades["G02"]["faithful"] is True


def test_unclear_answers_are_rejected():
    sheet = render_sheet(sample(make_rows())[:1]).replace("correct:\n", "correct: maybe\n")
    with pytest.raises(ValueError, match="maybe"):
        parse_sheet(sheet.replace("faithful:\n", "faithful: yes\n"))


def test_agreement_counts():
    a = agreement([(True, True), (True, False), (False, False), (False, True), (True, True)])
    assert (a["n"], a["agree"], a["human_yes_judge_no"], a["human_no_judge_yes"]) == (5, 3, 1, 1)
    assert a["kappa"] == pytest.approx((0.6 - 0.52) / (1 - 0.52))


def test_note_headings_and_lines_inside_excerpts_do_not_confuse_the_parser():
    item = {**sample(make_rows())[0],
            "excerpts": "[1] Lecture (Mon 2025-10-13)\n## Gradient descent basics\nnote: not a grade\ncorrect: no"}
    sheet = render_sheet([item]).replace("correct:\nfaithful:\nnote:\n", "correct: yes\nfaithful: yes\nnote:\n")
    assert parse_sheet(sheet) == {"G01": {"correct": True, "faithful": True, "note": ""}}
