You are grading an answer produced by a question-answering system over a student's personal notes. Compare the system's answer with the gold answer.

Question: {question}

Gold answer: {gold}

System answer: {answer}

Grading rules:
- "correct": the system answer states the key information in the gold answer, and nothing it says contradicts the gold answer. Wording does not matter. Citation markers like [2] do not matter.
- "incorrect": it leaves out or gets wrong any key part of the gold answer, contradicts it, or does not answer the question.
- If the gold answer has several parts, all of them are needed for "correct".
- Extra details that are not in the gold answer do not make an answer incorrect unless they contradict it. (Whether the answer is supported by the notes is graded separately.)
- The question is written by the student ("I", "my") and the system replies to them as "you"; that is expected.
- Judge only against the gold answer. Do not use your own knowledge of the facts.

Give a one- or two-sentence reason, then the verdict.
