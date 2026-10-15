---
title: "E500D Lecture - Tool Use in Agents"
date: 2025-10-21
tags: ["agentic-ai", "lecture"]
---

## why tolos at all
- LLM alone = frozen knowledge, bad at arithmetic, can't act on world
- tools -> extend model w/ search, calculator, code exec, APIs
- framing: model decides *when* + *which* tool + *what args*, env returns observation
- basically a policy over actions where some actions are function calls

## Patterns covered
- **ReAct-style loop**: thought -> action -> observation -> repeat
  - interleaving reasoning w/ calls helps grounding, fewer hallucinated facts
  - but loops can spiral, model keeps calling same tool ??
- **Toolformer idea**: self-supervised, model learns to insrt API calls where they reduce loss
  - cool b/c no big human labeled set needed
- **function calling / structured output**: JSON schema for args parser validates
  - most prod systems do this now
- planner vs executor split -> one model plans steps another (or same) executes

## Failure modes
- wrong tool selection when tool descriptions overlap
- bad args (type errors, made-up params)
- over-calling -> latency + cost blowup
- trusting tool output blindly -> prompt injection via retrieved content!!
- error recovery weak model often doesn't retry sensibly

## Eval
- hard to eval success rate on task vs per-step correctness
- trajectories matter, not just final answer
- sandboxing for code exec tools obviously

## own thoughts
- relevant for edge stuff -> tool calls to cloud vs on-device, when to offload ??
- how many tools before selection accuracy tanks?? lecture hand-waved this
- tool docs basically = prompt engineering, feels fragile

## Admin / misc
- staarted writing first E500D reading reflection -> tying it to tool-use failure modes prompt injection angle seems strongest
- [ ] reread ReAct section before finishing reflection
- [ ] look up how tool descriptions get ranked when list is long
