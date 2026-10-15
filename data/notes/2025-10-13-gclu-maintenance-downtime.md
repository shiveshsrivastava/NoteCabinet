---
title: "GCLU Maintenance Downtime"
date: 2025-10-13
tags: ["gpu-cluster"]
---

## What happened
- tried to kick off training runs on the GPU cluster this aft -> jobs just hung, couldn't even ssh in reliably
- turns out GCLU was offline for four hours for scheduled network maintenance
  - totally missed the notice?? need to actually read cluster emails lol
- used downtime to clean up configs + reread my data loader code locally so not a total loss

## After it came back
- relaunched -> new problem: import errors, lib not found at runtime
- spent way too long poking at env vars myself, going in circles
- pinged Marcus Webb -> he spotted it fast tricky library path issue, my env was picking up wrong paths
- MW walked me through fixing it, jobs actually start now
  - write down eaxctly what he changed before I forget!!

## Next
- [ ] doc the library path fix in vault so I don't redo this mess
- [ ] check cluster status page before blaming my own code next time
- [ ] watch relaunched jobs make sure they don't silently die
- not sure if maintenance affects queued jobs too?? ask around
- owe Marcus coffee fr
