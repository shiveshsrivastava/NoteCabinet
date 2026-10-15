---
title: "Cluster storage crunch"
date: 2025-11-08
tags: ["cluster", "data"]
---

- KITTI download onto GCLU -> started it took forever
- update KITTI download finally finished!! on GCLU, all there (I think?? spot check)

**storage**
- MW warned whole lab: cluster storage almost completely full
  - -> does my KITTI copy count as part of the problem?? prob yes lol
  - who decides what gets cleaned up?? ask
- [ ] check my own usage on GCLU b/c don't want to be the one hogging space
- [ ] ask MW if there's a scratch vs home dir thing I'm missing

- GCLU was offline four hours, scheduled network maintenance -> couldn't do anything, just waited
  - note to self: check maintenance announcements before planning long jobs

### profiling
- MW showed me how to profile PyTorch code efficiently on the cluster
  - didn't write down all the steps... half remember
  - -> redo it myself while still fresh
- [ ] write up profiiling steps properly here
- does profiling output also eat storage?? (given the full disk thing careful)

### library path mess
- tricky library path issue on GCLU -> MW helped resolve it
  - fix was something w/ env / path setup?? forgot exact detail
  - [ ] write down what actually fixed it so I don't have to bug him again

- misc
  - owe MW a thank you helped w/ like three things
  - storage crunch + maintenance = annoying combo
  - ??
