---
title: "E596C Lecture 1 - Backprop Fundamentals"
date: 2025-09-29
tags: ["deep-learning", "lecture"]
---

## Logistics
- first lecture of EE P 596 C tonight long block brought cofee -> good call
- Prof. Lindqvist: midterm exam is in week 5
  - scope?? prob everything up to then, didn't say exactly
  - MIDT format unclear -> closed book?? ask later
- programming assignments need real compute -> requested access to the GPU cluster after class
  - waiting on approval check email
- [ ] confirm GCLU login works once access goes through

## Backprop fundamentals
- core idea: chain rule applied over computational graph
  - forward pass -> compute + cache intermediate values
  - backward pass -> propagate grads from loss back to each param
- each node only needs local gradient * upstream gradient
  - modular -> why autograd frameworks work at all
- PLIN walked thru small MLP example by hand
  - sigmoid derivative reuses forward output, neat
  - ReLU grad = pass-through or zero, dead units issue mentioned
- vectorized form: Jacobians in theory, but never build them explicitly in practice b/c huge
  - use vector-Jacobian products instead
- gradient checking w/ finite differences -> sanity check own impl slow tho

## things that confused me
- why accumulate grads when node has multiple outgoing edges?? -> b/c total derivative sums over all paths makes sense now-ish
- shapes in matrix backprop -> keep messing up transposes
  - trick from lecture just match dims, transpose wherever needed
- memory cost of caching activations for big nets?? relevant later for edge stuff

## Takeaways
- re-derive linear layer + softmax/cross-entropy grads on paper this week
- E596C feels heavy on derivations -> good prep for MIDT
- once GCLU is sorted, try toy MLP from scratch, compare to autograd
