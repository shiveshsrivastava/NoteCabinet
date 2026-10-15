---
title: "LABM - On-Device Model Optimization"
date: 2025-10-30
tags: ["lab", "edge-ai"]
---

**Who:** me, PFOX (+ rest of lab)

## Context
- lab meeting today -> topic was on-device model optimization techniques
- general discussion of how to squeeze models down for running on-device
- lots of ground covered need to go back over my scribbles

## Re ANAV
- PFOX told me to **switch ANAV backend from Python -> C++**
- reasoning seemed to be about on-device constraints, overhead etc. (didn't catch everything, should ask again??)
- honestly kind of expected this eventually but still... big change
- not sure how much of current pipeline carries over ??
- which parts to port first?? inference path vs everything??

## Open qs / my thoughts
- how painful is porting going to be w/ my current C++ skill level lol
- bindings vs full rewrite?? -> ask PFOX to clarify what "switch" means exactly
- does this change anything for how I'm profiling stuff right now ??

## next steps
- [ ] reread notes from LABM while still fresh
- [ ] figure out scope of C++ switch for ANAV before starting anything
- [ ] brush up on C++ build tooling b/c rusty
- [ ] write down clarifying qs for PFOX

-> fold into Sunday task list
