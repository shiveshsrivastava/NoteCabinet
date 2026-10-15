---
title: "Handling Occlusion in Our Tracker"
date: 2025-10-28
tags: ["computer-vision", "tracking"]
---

- context LO suggested we build real-time object tracker for E596A -> sounded clean at first
- now: LO + me realized tracker has major occlussion flaw
  - obj goes behind something -> track just dies?? or worse, ID swaps to wrong obj

## half-baked ideas
- motion model to coast thru occlusion -> Kalman-ish predict step, keep track "alive" for a bit w/o detections??
- appearance embedding for re-ID when obj comes back out
  - cost?? real-time is the whole point can't bloat it
- treat occluded state explicitly vs just low confidence?
- partial occlusion vs full -> handle differently??

## questions
- how long to keep a lost track before killing it? no idea what's reasonable
- does detector even flag partially hidden objs reliably? maybe that's the real issue, not tracker
- worth checkng how standard trackers deal w/ this before reinventing

- [ ] talk thru w/ LO before we pick anything
