---
title: "GCLU Library Path Fix (thanks MW)"
date: 2025-10-08
tags: ["gpu-cluster", "debugging"]
---

## context
- requested access to the GPU cluster for the E596C programming assignments -> wanted it working before actually needing it
- access came through logged in fine but env was broken

## what I tried
- loaded modules, activated env -> import kept failing, complaining it couldn't find shared lib
- reinstalled packages in env -> same error ??
- fiddled w/ LD_LIBRARY_PATH by hand -> made it worse lol, different error now
- googled forever, half the answers are for other clusters, not helpful

## what fixed it
- pinged Marcus Webb b/c he knows GCLU setup way better than me
- MW looked at my shell config + module list for like a few min -> spotted the path was pointing at wrong lib dir (something stale from my own edits + module ordering)
- cleaned it up the way he suggested -> imports work, GPU visible from inside env
- tricky one would not have found this alone owe him coffee

## notes to self
- don't hand-edit library paths blindly -> check what modules already set first
- order of module loads matters?? still don't fully get why, ask next time it comes up
- keep shell config minimal on cluster

## next
- [ ] write the fix down properly in vault so future me doesn't redo this
- [ ] sanity-check a tiny training run on cluster before real assignment work
- [ ] figure out how job submission works vs interactive session ??
