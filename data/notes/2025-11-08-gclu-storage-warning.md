---
title: "GCLU Storage Almost Full"
date: 2025-11-08
tags: ["gpu-cluster"]
---

## log

**tried / status**
- KITTI download on GCLU -> finally finished!! been babysitting this forever
- haven't sanity-checked the files yet, just saw it complete

**what happened**
- Marcus Webb posted warning to lab: storage on GCLU almost completely full
- timing is great lol, right as KITTI lands
- not sure how much of the full-ness is me vs everyone else ??
- is my KITTI copy part of the problem?? prob contributes it's not small

**thoughts**
- don't want to be the person who breaks shared storage for whole lab
- unclear what the actual policy is for big datasets -> scratch vs home vs shared dir ??
- maybe there's already a shared KITTI copy somewhere & I duplicatted it?? would be embarrassing
- careful w/ any checkpoints / intermediate outputs those pile up fast

**next**
- [ ] ask MW where datasets are supposed to live + whether I should move/trim anything
- [ ] check my own usage on GCLU before writing anything else
- [ ] verify KITTI download is actually intact (don't trust it yet)
- [ ] look for junk files of mine to clean up -> old logs stale stuff
- hold off on kicking off anything that writes lots of output until storage situation clearer

note to self: stop letting temp files accumulate b/c this will keep happening
