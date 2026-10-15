---
title: "E596A Lecture - Tracking Robustness"
date: 2025-11-06
tags: ["computer-vision", "lecture"]
---

## Why trackers break
- PSTE opened w/ failure gallery -> ID switches, drift lost tracks after crowd crossings
- main culprits: occlusion fast motion appearance change (lighting, pose), detector misses
- tracking-by-detection only as good as association step -> bad matching = cascading errors

## motion models
- constant velocity Kalman filter = baseline cheap, surprisingly decent
- predict step keeps track "alive" when detection missing -> but uncertainty grows fast
- nonlinear motion (drones, people turning) -> KF prediction drifts off ??
- gating on Mahalanobis dist to reject crazy matches

## Occlusion handling
- keep lost tracks in bufer instead of killing immediately
- re-ID features (appearance embeddings) to reconnect after object reappears
- combine IoU cost + appearance cost in Hungarian matchiing
- partial occlusion -> bbox shrinks IoU tanks even tho same object
- **this is exactly what bit us** -> LO and I realized during lecture our E596A tracker had major occlusion flaw: tracks deleted the moment detection dropped, then respawned w/ new ID
- LO fixed the occlusion bug in our E596A tracking code -> lost-track buffer instead of instant delete
  - still want to sanity check on harder clips

## Robustness tricks
- confidence-aware association (low-conf dets used in second pass, ByteTrack-style)
- camera motion compensation b/c ego-motion messes up predictions
- appearance memory bank w/ smoothing rather than single last-frame feature

## Open qs
- how to tune buffer length w/o just guessing ??
- re-ID embedding cost on edge hardware -> worth it or just better motion model?
- relevant to AutoNav drone perception too think about later

- [ ] reread slides on combined cost matrix
- [ ] look up ByteTrack paper PSTE mentioned
