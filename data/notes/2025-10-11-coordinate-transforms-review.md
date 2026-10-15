---
title: "Robotic Coordinate Transformations Review"
date: 2025-10-11
tags: ["robotics", "autonav"]
---

sat morning -> spent it reviewing robotic coordinate transformatins mostly textbook-style review refreshing basics before they bite me in AutoNav.

## Key pts
- frames: world / body / camrea / sensor -> every measurement lives in *some* frame always write down which one
- rotation matrices: orthonormal, det = +1, inverse = transpose (cheap!)
- homogeneous transforms 4x4 combining R + t -> chain by multiplying
  - order matters!! T_world_cam = T_world_body * T_body_cam
  - naming convention T_a_b = "b expressed in a" -> stick w/ one or suffer
- Euler angles: intuitive but gimbal lock, also roll/pitch/yaw ordering differs across libs ??
- quaternions: no gimbal lock smooth interp (slerp) but harder to eyeball
- passive vs active rotation -> same matrix, opposite meaning. classic soucre of sign bugs

## Reactions
- relevant for ANAV b/c perception outputs (camera frame) need to get into body/world frame for nav -> if extrinsics off model looks wrong even when it isn't
- realizing half my past debugging pain was frame confsion not model issues lol
- ?? what convention does our drone stack use for camera frame — z forward or x forward
- ?? quaternion convention (w first vs w last) — check before trusting any logs

- [ ] sketch frame tree diagram for drnoe setup
- [ ] write tiny sanity-check script: transform known point verify by hand
