---
title: "Midterm Review Notes - CNNs"
date: 2025-11-08
tags: ["deep-learning", "exam-prep"]
---

Started review notes for **E596C** MIDT -> PLIN announced it's delayed *again*, now week 8. More time, but also feels like moving tagret lol

just finished second set of problem sets on CNNs, so good moment to consolidate while it's fresh.

## key points (lecture slides + HWKS)
- conv layer = shared weights over spatial locations -> way fewer params than fully connected
- receptive field grows w/ depth -> deeper layers see more context
- stride + padding control output size -> keep formula on cheat sheet, kept messing this up in HWKS
- pooling = cheap downsampling + some translation invariance (but not full invariance!!)
- batch norm -> stabilizes training, interacts weirdly w/ small batches??
- residual connections -> gradient flows thru skip path, why super deep nets train at all

## Reactions / conusions
- still fuzzy on backprop thru conv layer by hand -> it's basically conv w/ flipped kernel?? redo derivation
- dilated conv vs. just biggger kernel: tradeoff unclear to me
- connets nicely to AutoNav stuff, lightweight backbones = all about cutting conv cost (depthwise separable)
- invariance vs. equivariance distinction -> likely exam question imo

## to review
- [ ] rederive output-size formula from scratch
- [ ] backprop thru conv + pooling
- [ ] skim my mistakes in both HWKS
- [ ] make one-page summary sheet
