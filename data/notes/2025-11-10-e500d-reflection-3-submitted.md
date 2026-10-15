---
title: "E500D Reflection 3 Submitted"
date: 2025-11-10
tags: ["agentic-ai", "reflection"]
---

- submitted 3rd reading reflection for E500D online -> done, finally
- uploaded through course site double checked file actually attached (paranoid ater last time lol)

## key points from reading (as I understood them)
- agents = LLM + loop of plan -> act -> observe -> revise
- big theme: reasoning traces interleaved w/ actions help catch own mistakes
- tool use framed as extending what model can do vs. making model bigger
- failure modes discussed: getting stuck in loops, hallucinated tool outputs, drifting off goal over long hoorizons

## my reactions
- interleaving reasoning + acting feels obvious in hindsight but eval setup is what makes it convincing
- skepttical on how much is prompt engineering vs actual capability ??
- long-horizon drift part most interesting -> feels relevant to perception-driven agents, e.g. drone that has to keep re-grounding on what it sees
- cost/latency barely mentioned b/c everything assumes big cloud model. what about edge?? small models probably break the whole loop
- wrote most of reflection around that edge angle hope that's not too off-topic

## open qs
- how do you even benchmark "good planning" fairly across tasks ??
- is self-critique actuallly helping or just more tokens = more chances to get lucky?

- [ ] reread my reflection later, see if argument still holds
- [ ] jot down edge-agent idea somewhere so I don't lose it
