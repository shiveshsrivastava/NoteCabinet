---
title: "E596A Lecture - Multi-Object Tracking + Deadline Extension"
date: 2025-10-23
tags: ["computer-vision", "lecture"]
---

## Admin
- Prof. Seitz announced at start of class: assignment deadline extended by exacly two days
  - relief, was going to be tight w/ everything else this week
  - don't get lazy w/ it tho -> treat orginal date as real target
- Liam Ortiz and I submitted our E596A project proposal -> topic = multi-object tracking
  - good timing b/c today's lecture is literally our topic lol

## Multi-object tracking (MOT) overview
- goal: detect objects per frame + keep consistent IDs across frames
- tracking-by-detection = dominant paradigm
  - run detector each frame -> associate detections to existing tracks
  - association is the hard part not detection
- failure modes:
  - ID switches (two people cross paths -> labels swap)
  - fragmentation (trrack dies during occlusion, comes back w/ new ID)
  - false positives spawning junk tracks

## Motion model
- Kalman filter for predicting box position next frame
  - constant velocity assumption -> breaks on sudden trns
  - predict -> match -> update loop
- ?? how well does constant velocity hold for fast/erratic motion e.g. drone footage

## association
- cost matrix between predicted tracks and new detections
  - IoU-based cost = simple, cheap
  - appearance emeddings (re-ID features) help w/ occlusion + crossing
- Hungarian algorithm for optimal assignment
- gating ignore matches w/ cost too high -> avoids crazy jumps

## Track management
- new track needs a few consistent hits before confirmed
- unmatched tracks kept alive for a while before deletion -> handles short occlusions
- tradeoff: keep alive too long = ghost tracks, too short = fragmentation

## Metrics
- MOTA lumps FP FN ID swiitches together
- IDF1: focuses more on identity consistency
- PSTE said MOTA overweights detection quality -> look at both

## Thoughts / to-do
- [ ] send LO lecture slides on association + metrics, relevant for proposal scope
- ?? appearance features worth the extra compute or stick w/ IoU baseline first
- re-read Kalman update equations, got lost midway
