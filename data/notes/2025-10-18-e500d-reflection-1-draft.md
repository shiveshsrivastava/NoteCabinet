---
title: "E500D Reflection 1 Draft - ReAct"
date: 2025-10-18
tags: ["agentic-ai", "reflection"]
---

Started drafting first reading reflection for EE P 500 D -> ReAct (reasoning + acting). Rough notes below clean up later

## key points
- core idea: interleave reasoning trces ("thoughts") w/ actions (tool calls, env steps) instead of doing only one
- CoT alone -> hallucinates facts, no grounding in external info
- act-only -> no plan, gets lost can't recover from bad obs
- ReAct loop: thought -> action -> observation -> thought ...
- evals on knowledge tasks (HotpotQA FEVER w/ Wikipedia API) + decision-making (ALFWorld, WebShop)
- few-shot prompting only, no finetuning needed for main results
- traces = interpretable, humans can inspect/edit thoughts mid-run

## My reactions
- feels obvious in hindsight but framing matters b/c basically template for most agent frameworks now
- failure mode: loops / repeated actions when search returns junk -> how do modern agents detect this??
- thoughts are prompted, not verified -> is reasoning actually causal for actions or just narration??
- curious re: latency cost of extra thought tokens on edge devices -> connects to my drone stuff maybe
- want angle for reflection: grounding vs. faithfulness of traces

## Misc
- finally bought rquired textbook for E500D, check if it has a chapter on tool use to cite

- [ ] tighten draft, pick one argument not five
- [ ] reread experiments section, I skimmed it
