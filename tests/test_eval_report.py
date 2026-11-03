"""The Ask eval report on a few synthetic rows: what is counted where, and the rendered tables."""

from eval.report import render, summarize


def row(id, type, *, abstained=False, reason=None, correct=None, faithful=None, covered=True, gen_ms=1000.0):
    unanswerable = type == "unanswerable"
    return {
        "id": id, "type": type, "retriever": "bm25", "unanswerable": unanswerable, "abstained": abstained,
        "abstain_reason": reason, "correct": correct, "faithful": faithful, "invalid_citations": [],
        "retrieval": None if unanswerable else {"all_covered": covered, "coverage": 1.0 if covered else 0.5,
                                                "reciprocal_rank": 1.0 if covered else 0.5},
        "timings": {"retrieval_ms": 5.0, "rerank_ms": 20.0, "generation_ms": gen_ms},
    }


ROWS = [
    row("q1", "single", correct=True, faithful=True),
    row("q2", "multi", correct=False, faithful=False, covered=False),
    row("q3", "temporal", abstained=True, reason="low_rerank_score", correct=False, gen_ms=0.0),
    row("q4", "unanswerable", abstained=True, reason="model"),
    row("q5", "unanswerable", correct=False, faithful=True),
]
KINDS = {"q4": "near_miss", "q5": "near_miss"}
CFG = {"split": "dev", "n_questions": 5, "n_unanswerable": 2, "judge": {"model": "judge-model"},
       "abstain_threshold": 0.01, "retrieval": {"final_k": 5}, "git": {"commit": "abcdef0123", "dirty": False}}


def test_summary_counts():
    m = summarize(ROWS, KINDS)["bm25"]
    assert m["retrieval"]["n"] == 3 and m["retrieval"]["all_covered"] == (2, 3)
    assert m["retrieval"]["by_type"]["multi"]["all_covered"] == (0, 1)
    assert m["answers"]["correct"] == (1, 3)          # answerable only; the abstention counts as incorrect
    assert m["answers"]["faithful"] == (2, 3)         # answers actually given, incl. the unanswerable one
    a = m["abstention"]
    assert a["precision"] == (1, 2) and a["recall"] == (1, 2)
    assert (a["answerable_by_gate"], a["unanswerable_by_model"]) == (1, 1)
    assert a["by_kind"]["near_miss"] == {"n": 2, "gate": 0, "model": 1, "answered": 1}
    assert a["by_kind"]["off_topic"]["n"] == 0


def test_gated_answers_are_left_out_of_generation_latency():
    lat = summarize(ROWS, KINDS)["bm25"]["latency_ms"]
    assert lat["generation"]["n"] == 4 and lat["generation"]["p50"] == 1000.0
    assert lat["retrieval"]["n"] == 5


def test_unlabelled_unanswerable_questions_are_flagged():
    m = summarize(ROWS, {"q4": "near_miss"})
    assert m["bm25"]["abstention"]["unlabelled"] == ["q5"]
    assert "Unlabelled unanswerable questions" in render(m, CFG)


def test_render_shows_counts_and_empty_kinds():
    md = render(summarize(ROWS, KINDS), CFG)
    assert "| bm25 | 67% (2/3) | 0.83 (n=3) | 0.83 (n=3) |" in md
    assert "| bm25 | off_topic | 0 | n/a (0/0) | n/a (0/0) | n/a (0/0) |" in md
    assert "judge-model" in md and "abcdef0" in md
