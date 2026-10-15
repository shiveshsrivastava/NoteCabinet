---
title: "PyTorch Profiling on GCLU"
date: 2025-10-21
tags: ["gpu-cluster", "pytorch"]
---

## what happened
- Marcus Webb sat down w/ me & showed how to profile PyTorch code efficiently on GCLU
- before this I was basically guessing where time goes -> sprinkling print timers everywhere lol
- his approach: wrap the region you care about in the built-in profiler instead of timing whole script
  - only profle a short window, not full run -> otherwise trace is huge & useless
  - look at CUDA time vs CPU time separately b/c they tell different stories
  - sort the op table, stare at the top few rows first
- also showed how to pull the trace into the viewer so you can actually *see* gaps between kernels
- big takeaway: idle GPU time is the thing to hunt, not just slow ops

## reactions
- way less painful than I expected
- the trace viewer is kind of addictive ngl
- feel dumb for not doing this sooner

## open qs
- is the dataloader the bottleneck or is that just how it loks on first glance ??
- does prrofiler overhead skew the numbers much on GCLU noodes ??
- waarmup stps -> how many to skip before recording ?? forgot to ask
- how to tell sync points apart from real compute in the trace ??

## notes to self
- write down MW's steps somewhere permanent before I forget them
- don't profile the whole training loop again, seriously
- ask MW follow-ups in batch, not one ping at a time
