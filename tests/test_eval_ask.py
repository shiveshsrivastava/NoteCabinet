"""Which answers the Ask eval sends to which judge, and how the rest are scored (fake judge, no network)."""

import pytest

from eval.eval_ask import judge_all, judge_row
from eval.judge import JudgeError


class FakeJudge:
    def __init__(self, verdicts=None, fail=False):
        self.calls = []
        self.verdicts = verdicts or {"correctness": "correct", "faithfulness": "faithful"}
        self.fail = fail

    def grade(self, kind, **inputs):
        self.calls.append(kind)
        if self.fail:
            raise JudgeError("refusal")
        return {"verdict": self.verdicts[kind], "cached": False}


def row(unanswerable, abstained, **extra):
    return {"id": "q1", "retriever": "bm25", "unanswerable": unanswerable, "abstained": abstained,
            "question": "Q?", "gold": "G", "answer": "NOT_FOUND" if abstained else "A [1]", "excerpts": "[1] E",
            **extra}


def test_answered_answerable_gets_both_judges():
    judge = FakeJudge()
    v = judge_row(judge, row(False, False))
    assert judge.calls == ["correctness", "faithfulness"]
    assert v["correct"] is True and v["faithful"] is True


def test_abstaining_on_an_answerable_question_is_incorrect_without_a_judge_call():
    judge = FakeJudge()
    v = judge_row(judge, row(False, True))
    assert judge.calls == [] and v["correct"] is False and v["faithful"] is None


def test_answering_an_unanswerable_question_is_incorrect_but_still_checked_for_faithfulness():
    judge = FakeJudge(verdicts={"faithfulness": "unfaithful"})
    v = judge_row(judge, row(True, False))
    assert judge.calls == ["faithfulness"]
    assert v["correct"] is False and v["faithful"] is False


def test_abstaining_on_an_unanswerable_question_needs_no_judge():
    judge = FakeJudge()
    v = judge_row(judge, row(True, True))
    assert judge.calls == [] and v["correct"] is None and v["faithful"] is None


@pytest.mark.parametrize("label, expected", [("incorrect", False), ("correct", True)])
def test_verdict_labels_map_to_booleans(label, expected):
    v = judge_row(FakeJudge(verdicts={"correctness": label, "faithfulness": "faithful"}), row(False, False))
    assert v["correct"] is expected


def test_judge_errors_are_recorded_not_fatal(tmp_path):
    out = tmp_path / "per_question.jsonl"
    judged = judge_all(FakeJudge(fail=True), [row(False, False), row(False, True)], out)
    assert "judge_error" in judged[0] and judged[0]["correct"] is None
    assert judged[1]["correct"] is False  # abstained: scored without the judge, unaffected
    assert len(out.read_text().splitlines()) == 2
