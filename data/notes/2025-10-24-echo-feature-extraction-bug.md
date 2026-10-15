---
title: "ECHO Feature Extraction Bug"
date: 2025-10-24
tags: ["echosense", "debugging"]
---

## What happened
- Ryan Park pinged re **critical bug** in EchoSense feature extraction step
  - his words: "critical" -> taking seriously, everything downstream depends on features
  - haven't seen exact failure myself yet -> need his repro / logs
- open qs:
  - is it the extraction code itself or upstream audio loding?? 
  - silent bad output vs crash?? silent = way worse means anything tained on these features is suspect
  - when did it get introduced?? check reccent commits

## target change
- deadline got extended -> switched ECHO target **back to the workshop**
  - honestly relief, bug would've been painful otherwise
  - extra time should go to fixing this properly, not hacking around it

## tried so far
- nothing concrete yet on my end, only read RP's report
- skimmed extraction code nothing obvious jumped out -> prob need actual failing input to see it

## next
- [ ] get repro case + logs from RP
- [ ] run extraction on known-good sample, compare outputs
- [ ] diff recent changes to feature extraction step
- [ ] once fixed -> sanity check features before any more training
- [ ] upadte shared task list w/ new workshop target

note to self don't let this eat into coursework time, timebox debugging b/c it can spiral
