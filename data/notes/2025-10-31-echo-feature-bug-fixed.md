---
title: "ECHO Feature Extraction Bug Fixed"
date: 2025-10-31
tags: ["echosense", "debugging"]
---

## context
- RP flagged critical bug in ECHO feature extraction step -> whole downstream pipeline basically garbage until fixed
- been chasing this way too long, ugh

## what I tried
- first guess: input audio loading wrong?? -> checked, looked fine
- then suspected windowing / framing logic -> stepped through w/ debugger, compared intermediate arrays by hand
- printed shapes at every stage b/c something felt off w/ dims
- tried isolating extraction fn on its own w/ tiny dummy clip -> bug reproduced good, at least not falky

## what happened
- found it. finally fixed feature extraction bug in ECHO pipeline
- features now look sane when plotted, no more weird flat/blown-up regions
- honestly kind of embarrassing how small the actual mistake was once found lol
- relief tbh

## next / open qs
- does this change anything we concluded earlier from bad features?? prob need to recheck
- why didn't anything catch this sooner -> need some sanity checks on extraction output??
- tell RP it's fixed + ask him to pull and confirm on his end
- [ ] write down root cause somewhere so I don't repeat it
- [ ] look over rest of pipeline for similar sient issues?? paranoid now

note to self shape asserts are cheap, just add them
