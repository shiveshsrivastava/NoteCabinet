---
title: "MARL Survey Reading"
date: 2025-11-26
tags: ["agentic-ai", "reading"]
---

skimmed most of the MARL survey tonight, notes while fresh

## key pts
- core problem = non-stationarity -> each agent's env keeps shifting b/c other agents are learning at same time
- settings split: cooperative / competitive / mixed
- centralized training w/ decentralized execution (CTDE) seems like the dominant paradigm
  - critic sees global state during training, actors only use local obs at runtime
- cerdit assignment in shared-reward setups = still messy value decomposition approaches try to fix
- communication learning section -> agents learn what msgs to send, interesting but felt hand-wavy
- scalability joint acion space blows up w/ # agents, mean-field style approx as workaround

## reactions
- this connects way better to agentic AI stuff than my old topic did -> multiple LLM agents coordinating is basically a MARL problem w/o the RL formalism??
- CTDE framing might map onto planner + executor agent setups
- not sure how much of classic MARL theory traansfers to language aegnts tbh
- eval section weak lots of toy benchmarks

**decision: switching E500D paper topic to multi-agent RL.** feels like more to say + better fit w/ course readings

- [ ] dig up follow-up papers on credit assignment
- [ ] figure out angle -> survey-ish vs small experiment??
- [ ] reread comms section, missed stuff
