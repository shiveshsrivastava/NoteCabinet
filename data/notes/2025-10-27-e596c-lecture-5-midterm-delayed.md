---
title: "E596C Lecture 5 - Midterm Delayed, CNN Intro"
date: 2025-10-27
tags: ["deep-learning", "lecture"]
---

## Admin
- Prof. Lindqvist opened w/ announcement -> E596C MIDT delayed to week 7
- ugh. studied all day Saturday for the MIDT thinking it was coming up soon
  - not wasted I guess -> gives more buffer to actually absorb backprop stuff instead of cramming
  - reminder to self: don't let notes go stale, review again before week 7
- no details on format change?? ask PLIN after next lecture if coverage expands to conv nets now that it's later

## Why convolutions
- fully connected layers on images = way too many params ignores spatial structure
- conv layers -> local receptive fields + weight sharing
  - same filter slid across whole image -> translation equivariance
- param count depends on filter size + cannels NOT image size (big deal)

## Conv mechanics
- filter/kernel slides over input dot product at each location -> feature map
- stride = step size, bigger stride -> smaller output
- padding -> keeps spatial dims avoids losing edge info
- multiple filters -> multiple output channels
- output size formula on slides -> copy into cheat sheet, kept messing it up in lecture

## Pooling
- max pool vs avg pool
- downsamples some invariance to small shifts
- PLIN mentioned trend toward strided convs instead of pooling?? -> look into why

## Hierarchy of features
- early layers -> edges simple textures
- deepper layers -> parts, objects
- receptive field grows w/ depth b/c stacking
- showed filter visualizations, pretty cool

## open qs / todo
- [ ] rework output size exampels by hand
- [ ] how does backprop thru conv layer actually work?? (flipped kernel thing, didn't fully follow)
- [ ] connect this to CV course stuff overlap seems big
- dilated convs mentioned briefly -> prob not on exam but curious
