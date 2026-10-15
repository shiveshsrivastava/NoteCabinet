---
title: "ANAV Core Logic Ported to C++"
date: 2025-10-23
tags: ["autonav", "cpp"]
---

## context
- PFOX said to switch ANAV backend from Python -> C++
- reasoning made sense to me, Python side always felt like wrong fit for drone stuff anyway

## what I tried
- went module by module, core logic first, left everything else alone for now
- kept structure close to Python version so diffing behavior is less painful
- lots of fighting w/ types + memory ownership, way more boilerplate than expected
- some Python idioms just don't translate cleanly -> had to rethink a few spoots instead of line-by-line copy

## What happened
- **core ANAV logic now fully prted to C++** :)
- compiles, runs, no obvious crashes so far
- haven't rigorously checked outputs match old Python path yet so "done" w/ asterisk
- honestly C++ version reads cleaner in places b/c forced to be explicit about everything

## Open qs
- are outputs actuaally equivalent to Python version?? need some way to confirm
- edge cases / nuumerical differences b/w the two ??
- does rest of pipeline still talk to new backend properly or is glue broken somewhere ??
- worth showwing PFOX now or wait until verified ??

## Next
- [ ] side-by-side sanity check old vs new
- [ ] clean up leftover TODO comments scattered thru port
- [ ] write down gotchas from porting before I forget them

note to self don't touch perf tuning until correctness is nailed down
