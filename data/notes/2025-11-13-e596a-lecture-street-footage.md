---
title: "E596A Lecture - Real-World Evaluation"
date: 2025-11-13
tags: ["computer-vision", "lecture"]
---

## Benchmark vs real world
- PSTE opened w/ main point: benchmark scores != deployment performance
- datasets curated -> clean lighting, centered objects limited clutter
- real scenes motion blur, weird angles, crodws rain/glare -> mdoels fall apart
- "distribution shift" everywhere, even subtle stuff like camera sensor differences
- leaderboard chasing -> overfitting to test set quirks?? he seemed pretty annoyed about this lol

## Eval beyond accuracy
- look at failure cases, not just avg metric
- slice data by conndition (night, occlusion small objects) -> find where model actually breaks
- latency + memory matter for deployment -> relevant for edge stuff, think about this more
- qualitative review still important, watch the videos, don't just trust numbers

## Tracking specifically
- occlusion = classic failure mode -> ID switches when object reappears
- re-identification helps but adds cost
- long sequences expose drift that short clips hide

## Our tracking project (E596A)
- LO and I tested our tracking algorithm on real street footage -> very different from the clean sample clips
- lots of pedestrians crossing behind cars/poles -> exactly the occlusion problem from lecture
- LO fixed the occlusion bug in our tacking code -> tracks hold up way better now when objects get blocked
- still some jitter in crowded parts?? not sure if detector or association step
- lecture basically validated what we saw, nice timing

## open qs
- how to build a fair "real world" test set w/o it becoming another curated benchmark??
- how much failure-slicing is enough for final project writeup??
- does metric choice hide occlusion errors? ask PSTE maybe

- [ ] rewatch slides on failure analyis
- [ ] jot down our street footage observations before I forget
