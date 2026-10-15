---
title: "E596A Lecture 3 - Feature Tracking + Assignment 1"
date: 2025-10-16
tags: ["computer-vision", "lecture"]
---

## feature tracking recap
- Prof. Seitz started w/ why tracking != detection every frame -> cheaper, temporally consistent but drift is the enemy
- good features to track = corners, not edges/flat patches
  - aperture problem agian: edge only constrains motion perpendicular to it
  - look at eigenvlaues of structure tensor -> both large = corner, trackable
- brightness constancy assumption -> optical flow eq
  - one eq two unknowns per pixel -> need neighborhood constraint

## Lucas-Kanade
- assume flow constant in small window -> least squares solve
- breaks w/ large motion b/c linearization only valid for small displacements
  - fix: coarse-to-fine pyramid, estimate at low res, warp + refine going up
- KLT = LK + corner selection + iterative refinement
- failure modes: occlusion, lighting change features sliding off objeect boundary
  - forward-backward chcek to drop bad tracks?? PSTE mentioned briefly, need to reread slides

## Misc lecture notes
- template drift -> re-detect features periodically
- affine vs translation-only model for patch -> affine beter for longer tracks but more unknowns
- connection to deep flow nets hinted at, not covered yet

## Assignment 1
- PSTE released first maojr coding assignment for EE P 596 A today
- skimmed spec in class, looks substantial -> start early, don't repeat last-minute mess
- check starter code env actually runs before anything else

## project chat w/ Liam
- Liam Ortiz suggested after lecture we build real-time object tracker for E596A
  - pretty natural fit w/ today's material
  - "real-time" on what hardware?? laptop vs edge device
  - overlaps w/ drone perception stuff -> could be nice synergy, or scope creep ??
- need to think about whether tracker is too close to lecture content / novvel enough

## TODO
- [ ] reread LK derivation esp pyramid part
- [ ] read Assignment 1 spec fully
- [ ] reply to LO w/ thoughts on tarcker idea
