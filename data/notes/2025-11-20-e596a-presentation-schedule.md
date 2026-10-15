---
title: "E596A - Presentation Schedule Announced"
date: 2025-11-20
tags: ["computer-vision", "lecture"]
---

## Presentation schedule
- PSTE announced final project presentation schedule for E596A at start of class
- didn't catch all of it -> need to double check where we land in the order
- ?? is order fixed or can ppl swap
- ?? format expectations, live demo vs recorded video -> ask after next lecture if not on course page
- feels way closer than it should

## Tracking algo -> real footage
- LO and I tested E596A tracking algorithm on real street footage
- big difference vs clean toy clips, real wrold = messy
- stuff to look at more closely
  - occlusions, ppl walking behind cars/poles -> does ID survive??
  - lighting changes, shadows
  - lots of small far-away objects, not sure detector even sees them
  - camera shake ?? maybe need stabilization step first
- ran pretty smooth for a first real try honestly, but hard to judge w/o proper metrics
- ?? do we have any ground truth labels for this kind of footage or do we just eyeball it
- should save a few good + bad clips for slides, failure cases make for good discussion

## Misc thoughts
- presentation timing + tracking results basically same problem now -> need something demo-able
- want visaulizations that are easy to read on projector (boxes + IDs + trails?)
- keep slides minimal show video instead of tables

## TODO
- [ ] check announced schedule again confirm our spot
- [ ] sync w/ LO on what to clean up first in tracker
- [ ] pick candidate street clips for demo
- [ ] list open failure cases from test run
- [ ] start rough slide outline

reminder to self: don't let this slide into Sunday-night panic again
