---
title: "ECHO Data Collection Script"
date: 2025-10-10
tags: ["echosense", "data"]
---

## What happened
- Ryan Park shared initial data collection script for EchoSense -> finally something concrete to poke at
- skimmed through it structure looks reasonable at first glance
- open qs while reading:
  - how is auudio chunked / windowed?? need to check before trusting any of it
  - is sample rate hardcoded or configurable??
  - where do labels come from -> manual tagging or some auto heuristic??
  - any metadata logged w/ each clip (room, device, time)?? would matter later for anomaly stuff
- feels like a good starting base, not trying to rewrite it, just understand it first

## Decision
- talked w/ RP -> we're submitting ECHO to a smart home workshop
- kinda exciting also kinda scary lol
- means data collection quality matters way more now b/c reviewers will ask about it

## next
- [ ] actually read script line by line, not just skim
- [ ] write down my questions + send to RP instead of guessing
- [ ] look up workshop page -> what format / scope do they want??
- [ ] think about what "low-power" claim needs for evidence?? don't want to overpromise

## notes to self
- don't let this eat into coursework time, side project = side project
- keep log updated so Sunday cleanup is less painful
