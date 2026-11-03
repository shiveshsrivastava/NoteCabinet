# Judge check: review after grading

The official result is the blind one in `agreement.md`: correctness 87% (13/15), kappa 0.71;
faithfulness 53% (8/15), kappa 0.00. The hand grades in `sheet.md` were not changed after the
judge's verdicts were seen. This file only records what a review of the disagreements found.

## Correctness: both disagreements look like grading slips

Every gold answer in the sample was checked against the bible facts it cites (`fact_ids`) and the
notes those facts appear in; all 15 hold up. In both disagreements the judge's "incorrect" matches
the notes:

- **G12 (q024)**: the question asks why the open-source plan was dropped. Gold: the target went back
  to the workshop because its deadline was extended, as `2025-10-24-echo-feature-extraction-bug.md`
  says ("deadline got extended -> switched ECHO target back to the workshop"). The system answer gives
  the reasons for going open source in the first place, which answers a different question.
- **G13 (q023)**: gold says the original paper topic was LLM tool use, as three notes say
  (`2025-11-18-e500d-paper-llm-tool-use.md`: "E500D paper = LLM tool use"). The system answer calls
  the original plan "LLM agent coordination", a phrase from the later MARL note.

## Faithfulness: the judge is stricter than the hand grades

All 15 answers were graded faithful by hand; the judge marked 7 unfaithful. On review:

- **Judge arguably right (3)**: G06 claims the week-7 date held "as of Oct 25" from an Oct 27 note;
  G13 states "LLM agent coordination" as the original plan; G04 attributes the discussion
  section's Laplace review topic to office hours.
- **Judge stricter than a reader would be (4)**: G08 counts "AutoNav" as an unsupported expansion
  although the question itself names AutoNav; G10 and G14 because the excerpts never say which week a
  date falls in; G15 because a later note mentions the fix differently, although the cited note
  supports the claimed date.

So the run's faithfulness rates (61-72%) are best read as lower bounds. These categories are a
reviewer's judgement on 7 items, not a measured number.
