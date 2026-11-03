"""LLM judge for the evals: Claude ($JUDGE_MODEL) grades answers. Only evals call this; the app never does.

The prompts are plain files in eval/prompts/ so they can be read and audited; prompt_hashes() goes into
each run's config.json. The verdict is a JSON object constrained by a schema (output_config.format), so
the label is always one of the allowed values.

The judge model takes no temperature setting, so for repeatable numbers every verdict is cached on disk,
keyed by a hash of everything that could change it (model, effort, filled-in prompt, schema). Re-running
an eval reuses the cached verdicts and never pays twice for the same judgment.
"""

import hashlib
import json
import os
from pathlib import Path

from notecabinet import config

PROMPTS = Path(__file__).resolve().parent / "prompts"
CACHE_DIR = config.ROOT / "results" / ".judge_cache"  # gitignored
EFFORT = "medium"     # set explicitly: the default differs between Claude models
MAX_TOKENS = 16000    # thinking is always on and counts toward this

JUDGES = {
    "correctness": {"prompt": "judge_correctness.md", "labels": ["correct", "incorrect"], "fields": {}},
    "faithfulness": {"prompt": "judge_faithfulness.md", "labels": ["faithful", "unfaithful"],
                     "fields": {"unsupported_claims": {"type": "array", "items": {"type": "string"}}}},
}


class JudgeError(RuntimeError):
    """The judge returned no usable verdict (refusal, or output cut off)."""


def prompt_template(kind):
    return (PROMPTS / JUDGES[kind]["prompt"]).read_text()


def schema(kind):
    spec = JUDGES[kind]
    props = {**spec["fields"], "reason": {"type": "string"}, "verdict": {"type": "string", "enum": spec["labels"]}}
    return {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}


def prompt_hashes():
    """{kind: sha256 of prompt template + schema}, for config.json."""
    return {k: hashlib.sha256((prompt_template(k) + json.dumps(schema(k), sort_keys=True)).encode()).hexdigest()
            for k in JUDGES}


class Judge:
    def __init__(self, model=None, client=None, cache_dir=CACHE_DIR):
        self.model = model or os.environ.get("JUDGE_MODEL")
        if not self.model:
            raise SystemExit("JUDGE_MODEL is not set; run with `uv run --env-file .env ...`")
        self._client = client
        self.cache_dir = Path(cache_dir)

    @property
    def client(self):
        if self._client is None:
            import anthropic  # local dataset/eval tooling only, not an app dependency

            self._client = anthropic.Anthropic(max_retries=5)  # retries 429s, 5xx and connection errors
        return self._client

    def grade(self, kind, **inputs):
        """Verdict dict: the schema's fields plus judge, model, usage and cached (True if from disk)."""
        prompt = prompt_template(kind).format(**inputs)
        fmt = {"type": "json_schema", "schema": schema(kind)}
        key = hashlib.sha256(json.dumps({"model": self.model, "effort": EFFORT, "prompt": prompt, "format": fmt},
                                        sort_keys=True).encode()).hexdigest()
        path = self.cache_dir / f"{kind}-{key}.json"
        if path.exists():
            return {**json.loads(path.read_text()), "cached": True}

        response = self.client.messages.create(
            model=self.model, max_tokens=MAX_TOKENS,
            output_config={"effort": EFFORT, "format": fmt},
            messages=[{"role": "user", "content": prompt}],
        )
        if response.stop_reason != "end_turn":  # refusal or max_tokens: no trustworthy verdict, never cache it
            raise JudgeError(f"{kind} judge stopped with {response.stop_reason!r} (request {response._request_id})")
        text = next(b.text for b in response.content if b.type == "text")
        record = {**json.loads(text), "judge": kind, "model": response.model,
                  "usage": {"input_tokens": response.usage.input_tokens, "output_tokens": response.usage.output_tokens}}

        self.cache_dir.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(record, indent=2) + "\n")
        tmp.replace(path)  # atomic: an interrupted run never leaves a half-written verdict
        return {**record, "cached": False}
