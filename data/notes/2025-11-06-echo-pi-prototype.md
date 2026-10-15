---
title: "ECHO First Raspberry Pi Prototype"
date: 2025-11-06
tags: ["echosense", "edge-ai"]
---

## what happened
- RP got first ECHO acoustic model prototype running on Raspberry Pi -> actual hardware, not just laptop sim anymore!!
- me: FINALLY fixed feature extraction bug in ECHO pipeline
  - been staring at this way too long, felt good to kill it
  - features coming out of pipeline now look sane (at least by eye)

## tried / noes
- Ryan handled Pi side, I stayed on pipeline side -> split worked ok
- fix landed around same time as deploy -> unclear if Pi build has old or new feature code ??
- need to double check both sides compute features same way, otherwise model sees garbage on device
- haven't really looked at power draw yet ?? whole point of project is low-power so can't ignore

## open qs
- does model behave same on Pi as on laptop ?? no idea yet
- any other silent bugs in preprocessing that I'm missing ??
- how noisy is real room audio vs whatever we tested w/ ??

## next (rough nothing decided)
- [ ] sync w/ Ryan re: which pipeline version is on Pi
- [ ] write down what the bug actually was b/c I will forget
- [ ] sanity check outputs on device before getting excited

feels like real progress for once. don't jinx it
