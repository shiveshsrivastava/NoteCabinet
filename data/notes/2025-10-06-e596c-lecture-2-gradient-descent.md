---
title: "E596C Lecture 2 - Gradient Descent"
date: 2025-10-06
tags: ["deep-learning", "lecture"]
---

## Admin
- Prof. Lindqvist: midterm exam for EE P 596 C happening during week 5 -> start reviewing early, don't cram
- ?? what's covered on MIDT - everything up to then or just optimization stuff
- side note: already finished first set of E596C problem sets on gradient descent -> nice timing lecture lined up w/ what I did

## Gradient descent basics
- goal minimize loss L(θ) by stepping opposite gradient
- update: θ <- θ - η ∇L(θ)
- η = learning rate -> too big = overshoot / diverge too sall = crawls forever
- PLIN drew the classic bowl picture -> gradient points uphill so negate
- convex case = guaranteed to raech global min (w/ reasonable η)
- non-convex (aka basically every neural net) -> local mins, saddle pts, plateaus

## Batch vs stochastic vs mini-batch
- full batch: exact gradient, expensive per step
- SGD single sample, noisy but cheap
- mini-batch: middle ground, what everyone actually uses b/c GPU parallelism
- noise in SGD can help escape saddle pts?? -> he said yes-ish, intuition not proof

## Momentum etc
- momentum: accumulate velocity, smooths zig-zag in narrow valleys
- Nesterov = look-ahead version slightly better in practice
- teaser for adaptive methods (adam, RMSProp) next time

## LR schedules
- step decay cosine, warmup
- warmup matters for big models -> early grads unstable

## My takeaways / qs
- when I did the HWKS, my LR tuning was basically trial + error -> any principled way?? ask in OH maybe
- connect to AutoNav training -> small models, maybe try cosine schedule
- saddle pt vs local min distinction still fuzzy reread slides

- [ ] redo derivation of momentum update by hand
- [ ] make running list of topics for MIDT
- [ ] check if solutions for HWKS get posted
