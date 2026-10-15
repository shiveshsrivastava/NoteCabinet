---
title: "LABM - Back to Python"
date: 2025-11-10
tags: ["autonav", "lab"]
---

**who:** me, Prof. Fox (+ rest of lab, didn't track everyone)

## context
- came into lab meeting w/ update: finished porting core ANAV logic to C++ -> finally done
- was kind of proud of this tbh, lots of evenings on it

## Discussion
- Prof. Fox asked how fast we can try new ideas w/ C++ setup -> honest answer: slow
  - every small change = rebuild debug, rebuild
  - perception experiments need quick turnaround, C++ fights that
- general feeling in room: speed of iteration > raw runtime speed right now
- **Decision:** switch ANAV backend back to Python for faster iteration
  - yes right after C++ port finished. oof
- C++ work not totally wasted?? -> maybe useful later for deployment side didn't really settle that

## My take
- anonying but makes sense b/c project still in exploring phase
- lesson -> ask about iteration needs *before* big port next time
- keep C++ bracnh around, don't delete

## Next steps
- [ ] get Python backend running again
- [ ] note which bits of C++ logic differ from old Python version -> don't lose fixes made during port
- [ ] bring progress to next LABM
- ?? how much of port logic carries over cleanly
- ?? should I ask Prof. Fox if C++ version matters for edge deployment eventually
