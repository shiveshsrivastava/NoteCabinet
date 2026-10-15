---
title: "Midterm Study Day - Backprop Review"
date: 2025-10-25
tags: ["deep-learning", "exam-prep"]
---

Spent all day Saturday studying for the upcoming EE P 596 C midterm exam -> ging back over backprop since it's the foundation for everything else.

Source: my notes from the first E596C lecture, which covered backpropagation fundamentals + re-derived stuff by hand

## key pts
- backprop = chain rule applied systematically over a computational graph
- forward pass: compute + **cache** intermediate values (needed later!!)
- backward pass: upstream grad x local grad -> pass downstream
- each node only needs to know its own local derivative -> modular, nice
- branching paths -> grads **add** at merge pts (kept forgetting this)
- matrix case: check shapes dL/dW must match shape of W -> good sanity check
- sigmoid local grad = s(1 - s) -> saturates at extremes -> vanishing grads ??

## Reactions
- scalar version clicks now, vectorized/Jacobian version still shaky
- why is reverse mode cheaper than forward mode for nets?? I think b/c one scalar loss, many params -> one backward sweep gets all grads. confirm
- drawing graph first, then gradients, helped a LOT vs. just pushing symbols
- ReLU grad at exactly zero -> just pick a convention?? 

## TODO
- [ ] redo a two-layer MLP backward pass from scratch, no notes
- [ ] practice softmax + cross-entropy grad (always messy)
- [ ] write a one-page cheat summary for the MIDT

feeling ok-ish. need more reps on matrix calculus befroe it's automatic
