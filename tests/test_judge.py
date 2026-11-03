"""The eval judge with a fake Claude client: prompt filling, schema, caching, refusals. No network."""

import json
import string
from types import SimpleNamespace

import pytest

from eval.judge import JUDGES, Judge, JudgeError, prompt_hashes, prompt_template, schema


class FakeClient:
    """Stands in for anthropic.Anthropic(): records requests, returns a canned verdict."""

    def __init__(self, verdict, stop_reason="end_turn"):
        self.calls = []
        self.messages = SimpleNamespace(create=self._create)
        self.verdict, self.stop_reason = verdict, stop_reason

    def _create(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(
            stop_reason=self.stop_reason, model=kwargs["model"], _request_id="req_test",
            content=[SimpleNamespace(type="thinking", thinking=""),
                     SimpleNamespace(type="text", text=json.dumps(self.verdict))],
            usage=SimpleNamespace(input_tokens=100, output_tokens=20),
        )


CORRECT = {"reason": "Matches the gold answer.", "verdict": "correct"}
INPUTS = {"question": "When is the 1:1?", "gold": "Wednesdays at 2pm.", "answer": "Wednesdays at 2pm [1]."}


def test_prompt_placeholders_are_exactly_the_inputs_we_fill():
    fields = {k: {f for _, f, _, _ in string.Formatter().parse(prompt_template(k)) if f} for k in JUDGES}
    assert fields == {"correctness": {"question", "gold", "answer"},
                      "faithfulness": {"excerpts", "question", "answer"}}


def test_schema_restricts_the_verdict_and_requires_every_field():
    s = schema("faithfulness")
    assert s["properties"]["verdict"]["enum"] == ["faithful", "unfaithful"]
    assert set(s["required"]) == {"unsupported_claims", "reason", "verdict"}
    assert s["additionalProperties"] is False


def test_grade_sends_filled_prompt_and_schema(tmp_path):
    client = FakeClient(CORRECT)
    v = Judge(model="judge-model", client=client, cache_dir=tmp_path).grade("correctness", **INPUTS)
    assert v["verdict"] == "correct" and v["model"] == "judge-model" and v["cached"] is False
    call = client.calls[0]
    assert "Gold answer: Wednesdays at 2pm." in call["messages"][0]["content"]
    assert call["output_config"]["format"]["schema"] == schema("correctness")
    assert "temperature" not in call  # rejected by the judge model


def test_second_identical_grade_comes_from_the_cache(tmp_path):
    client = FakeClient(CORRECT)
    judge = Judge(model="judge-model", client=client, cache_dir=tmp_path)
    judge.grade("correctness", **INPUTS)
    again = judge.grade("correctness", **INPUTS)
    assert again["cached"] is True and again["verdict"] == "correct"
    assert len(client.calls) == 1


def test_cache_key_changes_with_inputs_and_model(tmp_path):
    client = FakeClient(CORRECT)
    Judge(model="judge-model", client=client, cache_dir=tmp_path).grade("correctness", **INPUTS)
    Judge(model="judge-model", client=client, cache_dir=tmp_path).grade("correctness", **{**INPUTS, "answer": "x"})
    Judge(model="other-model", client=client, cache_dir=tmp_path).grade("correctness", **INPUTS)
    assert len(client.calls) == 3


def test_refusal_raises_and_is_not_cached(tmp_path):
    client = FakeClient(CORRECT, stop_reason="refusal")
    judge = Judge(model="judge-model", client=client, cache_dir=tmp_path)
    with pytest.raises(JudgeError):
        judge.grade("correctness", **INPUTS)
    assert not list(tmp_path.iterdir())


def test_missing_input_is_an_error(tmp_path):
    with pytest.raises(KeyError):
        Judge(model="m", client=FakeClient(CORRECT), cache_dir=tmp_path).grade("correctness", question="q")


def test_prompt_hashes_cover_every_judge():
    assert set(prompt_hashes()) == set(JUDGES)


def test_no_model_configured(monkeypatch):
    monkeypatch.delenv("JUDGE_MODEL", raising=False)
    with pytest.raises(SystemExit):
        Judge()
