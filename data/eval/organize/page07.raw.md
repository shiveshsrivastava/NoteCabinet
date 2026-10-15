---
title: "ANAV C++ port"
date: 2025-10-25
tags: ["autonav", "research"]
---

- PFOX -> switch ANAV backend from Python to C++ (his call ok fine)
- core logic port to C++ = DONE!! finally
  - [x] port core ANAV logic -> C++
- sensor suite stuff:
  - new sensor suite integrated into ANAV sim, works
  - double check it still behaves w/ the C++ core?? prob fine but

## misc / env
- local env configured for perception module -> took forever b/c of deps, don't touch it now lol
- MW showed me how to profile PyTorch code efficiently on GCLU
  - write down his steps somewhere before I forget
  - profiler output was ... ?? half remember

- first LABM -> repo architecture for ANAV
  - where does C++ backend live vs perception module ??
  - Python side still needed for training?? or all C++ eventually
  - ask PFOX again re this, notes from LABM are thin

- [ ] clean up these notes Sunday
- [ ] re-read MW profiling tips -> apply to perception module

random thought: profiling on GCLU vs local env, compare?? 

- todo-ish: sim + sensor suite + C++ core all together -> sanity check
  - (sensor integration was before or after port? don't remember, whatever)

note to self: stop dumping everything on one page
