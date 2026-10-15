---
title: "E500D Lecture - Tool-Augmented LLMs"
date: 2025-11-18
tags: ["agentic-ai", "lecture"]
---

## Why tools at all
- LLMs bad at: exact arithmetic, fresh info anything needing real state -> offload to tools
- tool = any callable w/ defined interface (calculator search, code interpreter, APIs)
- framing: model as controller, tools as actuators -> kind of like perception + planning split in robotics??

## How models learn to call tools
- prompting only: describe tools in context, model emits structured call harness executes, result fed back
- fine-tuning on tool traces -> self-supervised variant where model inserts calls & keeps ones that lower loss on next tokens (Toolformer-style idea)
- function calling = JSON schema in, JSON args out -> brittle when schema large
- ReAct loop: thought -> action -> observtaion -> repeat
  - interleaving reasoning w/ actions helps gounding, but loops can spiral / repeat same call

## Failure modes discussed
- hallucinated tool names / args
- over-calling (search for stuff it already knows) vs under-calling
- error propagation: bad observation poisons rest of trajectory
- tool output injection -> security issue untrusted text treated as instructions
- latency + cost stack up w/ every call

## Eval
- task success vs. call accuracy vs. efficiency -> no single metric everyone agrees on
- benchmarks mostly synthetic APIs?? how well does that transfer to messy real APIs

## My takeaways
- **decided E500D paper topic = LLM tool use** -> finally been going back & forth
- angle ideas (not settled):
  - tool selection when tool library is huge -> retrieval over tool descriptions?
  - small/edge models calling tools vs big models -> ties into edge deployment interest
  - robustness to noisy tool outputs
- open q survey-ish vs small experiment?? need to scope

- [ ] pull refs from today's slides for paper
- [ ] jot reflection thoughts on ReAct failure looops while fresh
