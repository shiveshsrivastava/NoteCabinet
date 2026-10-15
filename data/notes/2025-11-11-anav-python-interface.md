---
title: "ANAV Python Interface Finalized"
date: 2025-11-11
tags: ["autonav", "python"]
---

## What happened
- spent the afternoon finalizing the Python interface for ANAV
- context: we decided to switch the ANAV backend back to Python -> faster iteration was the whole point
  - previous setup felt too slow to tweak, every small change = long loop before seeing anything
  - Python = quick edit, rerun, look at output, repeat

## tried
- went through the interface fn by fn, cleaned up the entry points so the perception side calls in w/ one consistent pattern
- renamed a bunch of stuff that was confusing me, prob confusing everyone else too
- tidied arg handling so it doesn't silently swallow bad inputs
- sanity-ran it end to end locally no crashes on the paths I checked

## Observations
- way nicer to poke at interactively now honestly should've stayed in Python from the start lol
- some old glue code from the previous backend still lying around -> messy, but not blocking
- ?? perf hit from going back to Python, is it gonna matter for edge deployment later or nah
- ?? are the interface boundaries in the right place or will I regret this in a week

## next
- [ ] clean out the leftover glue code
- [ ] write down how the interface is supposed to be used b/c future me will forget
- [ ] keep an eye on speed, don't optimize prematurely
- remind self iterate fast, that's the whole reason for the switch, don't overengineer it again
