---
title: "ECHO Architecture Doc Kickoff"
date: 2025-11-13
tags: ["echosense", "docs"]
---

## what happened
- kicked off system architecture doc for ECHO w/ RP today
  - mostly just skeleton so far -> section headeers, rough block diagram sketch
  - talked through how pieces connect mic input -> feature extraction -> model -> alert path
  - lots of hand-waving still, but good to finally have something written down instead of in our heads
- RP got first acoustic model prototype running on Raspberry Pi!!
  - first time ECHO actually lives on real hardware not just laptop
  - he showed me it running, seemed to work end to end
  - haven't dug into perf numbers yet, didn't want to guess

## thoughts
- doc + prototype same day = nice timing b/c can describe what actually eixsts vs imaagined design
- prob should write doc around what's on the Pi rather than ideal version
- power budget section feels most important for low-power angle -> no real data for it yet

## open qs
- how much detail in architecture doc vs keeping it high level ??
- what's the bottleneck on Pi side - inference or audio preprocessing ??
- how to diagram the anomaly loggic cleanly ??
- does prototype need retraining for different rooms / noise floors ??

## next
- [ ] reread draft w/ fresh eyes, fill in gaps
- [ ] ask RP about his Pi setup steps so doc captures them
- [ ] note down questions as they come up instead of losing them

feels like ECHO went from idea to real thing today, kinda hyped
