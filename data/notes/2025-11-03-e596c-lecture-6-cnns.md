---
title: "E596C Lecture 6 - CNNs, Midterm Moved to Wk8"
date: 2025-11-03
tags: ["deep-learning", "lecture"]
---

## Admin
- PLIN: MIDT delayed *again* -> now week 8
  - second time it's moved?? starting to lose track
  - honestly fine, more buffer for conv stuff
- finished second set of E596C problem sets on CNNs before leture -> felt good walking in for once
  - backprop through conv layer part took forever, glad it's done

## Conv nets - core idea
- fully connected on images = way too many params ignores spatial structure
- conv layer -> small learned filter slides over input, same weights everywhere
  - **weight sharing** + **local connectivity** = the whole point
  - translation equivariance (not invariance! he stressed this)
- output = feature map, one per filter
- stride / padding control output size
  - "same" padding keeps spatial dims "valid" shrinks
  - need to re-derive output size formula myself, wrote it too fast

## Pooling
- max pool -> downsample, some small-shift invariance
- avg pool more common at end (gloabl avg pool before classifier)
- he mentioned some modern archs just use strided conv instead of pooling -> why exactly?? ask / look up

## Receptive field
- stacking small filters -> recetive field grows w/ depth
- deeper + small kernels > shallow + big kernels (fweer params, more nonlinearity)
- dilated conv = grow RF w/o extra params -> relevant for AutoNav maybe?? segmentation-ish stuff

## Channels / 1x1 conv
- filters span all input channels
- 1x1 conv = per-pixel linear mixing across channels -> cheap channel reduction
- depthwise separable conv mentioned briefly -> mobile/edge archs, def want to read more on this b/c edge deployment

## Misc
- batchnorm after conv, before activation (he said order debated)
- visualizing early filters -> edge/color detectors, later layers more abstract

## To self
- [ ] redo output-size derivation by hand
- [ ] skim depthwise separable section in readings
- [ ] look back over HWKS mistakes before midterm review
- slides went fast near end, rewatch recording if posted
