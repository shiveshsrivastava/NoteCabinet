---
title: "ANAV backend progress and advisor check-ins"
date: 2025-11-05
tags: ["autonav", "research"]
---

- C++ backend compiles w/ zero warnings!!! finally
- PFOX canceled 1ON1 this wk -> grant deadline. fine, more time to clean up

## backend stuff
- core ANAV logic -> ported to C++, done
  - b/c PFOX said switch backend off Python -> C++
  - ?? was the reasoning mainly speed or edge deployment? think it tied into the edge discussion, need to reread notes
- new sensor suite integrated into sim, works
  - ?? did that happen before or after port... python side or C++ side?? check commit log

- first LABM -> repo architecture for ANAV
  - half remember: where does C++ core live vs sim code
  - ?? anything actually decided or just discussion

## advisor check-ins
- great 1ON1 w/ PFOX re: scalable Edge AI architecture
  - really useful connects to why C++ backend
  - notes from it scattered somewhere, find + paste here
- this wk's 1ON1 = canceled (grant deadline, see above)

## todo / loose ends
- [ ] write up what changed in port for whenever next 1ON1 happens
- [ ] pull LABM repo architecture notes into one place
- [ ] confirm sensor suite still behaves w/ C++ backend ??
- [ ] organize this Sunday

random: compile clean but haven't really stress tested anything -> don't celebrate yet
?? should sensor sutie integration get its own section, it's kind of buried
-> messy fix later
