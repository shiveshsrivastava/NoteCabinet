---
title: "ANAV Env Setup + GCLU Access Request"
date: 2025-10-03
tags: ["autonav", "setup"]
---

## what I tried
- set up local env for AutoNav perception module
  - fresh conda env, pulled repo, installed deps from requirements file
  - some pkg conflicts at first -> pinned stuff until imports stopped yelling
  - ran the basic import check + tiny forward pass on CPU -> works, slow but whatever just sanity
- submitted request for access to the GPU cluster for E596C programming assignments
  - filled out the form listed course as reason
  - no reply yet ??

## what happened
- local ANAV env = functional at least for dev / debugging
- not touching real training locally, laptop would melt
- cluster access pending -> can't test anything on GPU nodes yet
- unclear how long approval takes ?? hopefully not forever b/c I'd rather not be scrambling once assignments ramp up

## Next
- [ ] keep an eye on inbox for GCLU approval
- [ ] once in -> figure out job submission basics, storage quotas, etc. (no idea how any of it works yet ??)
- [ ] write down env setup steps somewhere so I don't redo this from scratch latter
- [ ] double check ANAV deps don't clash w/ whatever couurse env ends up looking like

notes to self setup always takes longer than expected. annoying but done-ish
