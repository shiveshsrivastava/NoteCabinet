---
title: "ANAV Sim Demo for PFOX"
date: 2025-11-11
tags: ["autonav", "demo"]
---

**who:** me, PFOX

## demo
- walked thru ANAV sim demo -> drone in sim env, perception model running in loop
- PFOX was impressed w/ it!! honestly did not expect that reaction was bracing for a pile of critiques
- asked a few q's about how percetion output feeds into nav -> answered ok-ish prob should clean up my explanation for next time
- vibe overall v positive, relief

## backend discussion
- talked about current backend setup + how slow it's been to iterate on
- **decision:** switch ANAV backend back to Python -> faster itertaion
  - b/c every small change has been taking way too long to test
  - kind of funny we're going back, but iteration speed > everything rn
- perf concerns w/ Python?? -> didn't really dig in park for later

## next steps
- [ ] start porting backend pieces back to Python
- [ ] figure out which parts are worth keeping vs rewriting from scratch ??
- [ ] re-run sim demo after swtch to make sure nothing breaks
- [ ] write up short summary of demo for my own records

## random thoughts
- good momentum don't lose it
- remember to save demo recording somewhere I can actually find it
- what's the cleanest way to structure the Python side so I don't end up w/ spaghetti again ??
