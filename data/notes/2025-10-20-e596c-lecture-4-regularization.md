---
title: "E596C Lecture 4 - Regularization"
date: 2025-10-20
tags: ["deep-learning", "lecture"]
---

## Admin
- Prof. Lindqvist: **midterm exam is week 5** -> next week basically?? need to plan review
- covers everything up through today's regularization stuff I think confirm on course page
- finished first set of EE P 596 C problem sets (gradient descent) -> relief remaining HWKS will probably lean on today's material

## Why regularize
- overfitting = low train loss, bad val loss -> model memorizing noise
- bias/variance tradeoff, regularization pushes toward simpler fns
- more data is best fix but not always possible

## L2 / weight decay
- add penalty on squared weights to loss
- graient view: each step shrinks weigths toward zero
- weight decay vs L2 not identical w/ adam -> AdamW decouples them. PLIN said this trips ppl up
- ?? why exactly does coupling break w/ adaptive lr, reread slides

## L1
- abs value penalty -> sparse weights
- not differentiable at zero subgradient handles it
- less common in deep nets more in linear models

## Dropout
- randomly zero activations during training
- interpretation: implicit ensemble of subnetworks
- scale at test time (or inverted dropout scales during train) -> remember which one PyTorch does
- don't really use in conv layers as much, BN kinda replaced it??

## early stopping
- watch val loss stop when it goes up
- acts like implicit regularization, related to L2 in simple cases (proof sketch on board, misssed half)

## Data augmentation
- flips crops coolor jitter -> encode invariances
- ties into CV course too, useful for AutoNav drone imagery maybe

## other
- label smoothing, mixup mentioned briefly
- BN has mild regularizing effect b/c batch noise

## to do
- [ ] start MIDT review for E596C, go back thru lectures 1-4
- [ ] rederive weight decay update by hand
- [ ] check AdamW paper section on decoupling
