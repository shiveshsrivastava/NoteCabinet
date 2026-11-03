# Judge check: hand grading sheet

Grade each answer yourself, **without** looking at the judge's verdicts (they are not on this sheet),
using the same rules the judge was given (`eval/prompts/judge_correctness.md`, `judge_faithfulness.md`):

- **correct** (`yes`/`no`): compared with the gold answer, the system answer gives everything the
  question asks for and contradicts nothing in the gold. Background in the gold that the question
  doesn't ask for may be left out, but must not be stated wrongly. Extra details are fine unless they
  contradict the gold. Wording and citation markers like [2] don't matter.
- **faithful** (`yes`/`no`): every factual claim in the answer (names, dates, times, numbers, places,
  decisions, events) is stated in the excerpts or follows directly from them. Expanding an abbreviation
  counts as supported only if the excerpts show what it means. Ignore correctness and which excerpt a
  citation number points to.

Fill in the `correct:` and `faithful:` lines under each item (`yes` or `no`). `note:` is optional.
Then run `uv run python -m eval.judge_check score <run folder>`.

---

## G01

**Question:** Why did Sarah Kim have to cover my EE 235 office hours?

**Gold answer:** I had a dentist appointment.

**System answer:** Sarah Kim had to cover your EE 235 office hours because you had a dentist appointment and couldn't attend your own office hours [1].

**Excerpts the system saw:**

```text
[1] DSEC Laplace Review + SK Covering OFHR (Wed 2025-10-22)
**Who:** me, Sarah Kim, PATL (msgs/quick chat not all at once)

## DSEC - Laplace review
- led review session on Laplace transforms for E235 during DSEC
- went thru basics -> transform pairs, properties, inverse via partial fractions
- students mostly ok w/ table lookups, shakier on ROC stuff + partial fractions w/ repeated roots
- maybe redo ROC w/ more pictures next time?? felt rsuhed

## Office hours coverage
- had dentist appt -> couldn't do my OFHR
- SK covered my E235 OFHR, huge help
- ask SK what ppl came in w/ -> prob same Laplace confusion

## Section time change
- PATL moved my DSEC to **Wednesdays at 4pm**, permanently
- so not a one-off -> fix everything around it
- does this clash w/ anything on my end?? double check

## next steps
- [ ] thank SK for covering OFHR
- [ ] update calendar for new Wednesdays at 4pm slot
- [ ] jot down which Laplace topics students struggled w/ while still fresh
- [ ] ping PATL if anything weird comes up w/ new time

[2] Friday TA Logistics + Coffee (Fri 2025-10-03)
- [ ] add EE 235 office hours to calendar -> Fridays at 3pm, official now
- [ ] update Canvas/syllabus page w/ OFHR time ?? check if Prof. Atlas wants to post it himself
- [ ] block Friday mornings for cofefe w/ Chloe Nguyen -> every Friday this quarter, agreed
- [ ] set recurring reminder so I don't double-book mornings
- [ ] prep something to do during E235 slots if nobody shows up (wk 1 prob quiet)

notes:
- coffee w/ CN = good anchor before the 3pm block, don't skip it b/c of work
- where do I hold OFHR?? room not confirmed yet

[3] Empty Office Hours (Wed 2025-10-15)
**Attendees:** just me. nobody else showed.

- E235 office hours this afternoon -> completely empty. zero students, the whole time
- context: had already moved OFHR to **Wednesdays at 3pm** b/c Friday attendance was so low
  - so the switch was supposed to fix this.. didn't, at least not today
- spent the slot sitting w/ laptop open half expecting someone to wander in. no one did

### thoughts / open qs
- did students actually nootice the time change?? not sure
- is it the time, or do people just not need help right now?? hard to tell from one empty session
- maybe they're using other channels instead of coming in person?? no idea
- don't want to overreact to a single afternoon

### decided
- nothing new. wednesday slot stays as is for now

### Next steps
- [ ] keep showing up for Wed OFHR, see if anyone comes
- [ ] think aobut why turnout is so low -> revisit when organizing notes Sunday
- [ ] use empty time productivly next time instead of just waiting aorund

mildly demoralizing ngl, but ok. one data point

[4] E235 TA Kickoff with PATL (Wed 2025-10-01)
**Who:** Prof. Atlas, Sarah Kim, me

quick kickoff for EE 235 TA stuff. Short mostly logistics

## Discussed
- PATL assigned me to teach the E235 discussion section on **Thursdays at 10am**
  - -> so I own the DSEC, not shared
  - first time leading a section solo.. slightly nervous lol
- SK + me split remaining TA duties details still fuzzy
  - autograding scripts = joint w/ SK, who does what?? not decided yet
- PATL wants section to reinforce lecture material, not introduce new stuff
  - format of worksheets?? didn't really get to it, ran out of time

## open qs
- do I prep my own materials or does PATL send something each week??
- attendance tracked or not??
- where are past section notes do they even exist??

## Next steps
- [ ] email PATL re: section materials question
- [ ] ping SK to sort out script spilt
- [ ] block Thursday mornings on calendar so nothing else lands there
- [ ] skim intro lecture slides before first DSEC

feels manageable as long as prep doesn't eat into my own coursework -> watch that

[5] Schedule Conflict - DSEC vs LABM (Mon 2025-10-06)
- PATL put me on the EE 235 discussion section -> Thursdays 10am
- just realized: Thursday 10am = my lab meeting slot. direct conflict ugh
- how did I not catch this earlier??

half-formed options:
- swap DSEC time w/ someone?? not sure if that's even allowed for E235
- ask if LABM can shift?? prob not, whole group's schedule
- join LABM remotely / late?? -> feels bad miss updates
- catch up via notes/slides after LABM?

questions
- who do I ask first - PATL or lab side??
- is the section time fixed b/c of room booking?
- how flexible is any of this in week 2 vs later

- [ ] figure out who to email before this turns into a recurring mess

feels like one of those things that'll get worse if I wait
```

correct: yes
faithful: yes
note:

---

## G02

**Question:** What was the second set of EE P 596 C problem sets about?

**Gold answer:** CNNs.

**System answer:** The second set of EE P 596 C problem sets was about CNNs [2].

**Excerpts the system saw:**

```text
[1] E596C Lecture 2 - Gradient Descent (Mon 2025-10-06)
## Admin
- Prof. Lindqvist: midterm exam for EE P 596 C happening during week 5 -> start reviewing early, don't cram
- ?? what's covered on MIDT - everything up to then or just optimization stuff
- side note: already finished first set of E596C problem sets on gradient descent -> nice timing lecture lined up w/ what I did

## Gradient descent basics
- goal minimize loss L(θ) by stepping opposite gradient
- update: θ <- θ - η ∇L(θ)
- η = learning rate -> too big = overshoot / diverge too sall = crawls forever
- PLIN drew the classic bowl picture -> gradient points uphill so negate
- convex case = guaranteed to raech global min (w/ reasonable η)
- non-convex (aka basically every neural net) -> local mins, saddle pts, plateaus

## Batch vs stochastic vs mini-batch
- full batch: exact gradient, expensive per step
- SGD single sample, noisy but cheap
- mini-batch: middle ground, what everyone actually uses b/c GPU parallelism
- noise in SGD can help escape saddle pts?? -> he said yes-ish, intuition not proof

[2] E596C Lecture 6 - CNNs, Midterm Moved to Wk8 (Mon 2025-11-03)
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

[3] E596A Lecture 3 - Feature Tracking + Assignment 1 (Thu 2025-10-16)
## Assignment 1
- PSTE released first maojr coding assignment for EE P 596 A today
- skimmed spec in class, looks substantial -> start early, don't repeat last-minute mess
- check starter code env actually runs before anything else

## project chat w/ Liam
- Liam Ortiz suggested after lecture we build real-time object tracker for E596A
  - pretty natural fit w/ today's material
  - "real-time" on what hardware?? laptop vs edge device
  - overlaps w/ drone perception stuff -> could be nice synergy, or scope creep ??
- need to think about whether tracker is too close to lecture content / novvel enough

## TODO
- [ ] reread LK derivation esp pyramid part
- [ ] read Assignment 1 spec fully
- [ ] reply to LO w/ thoughts on tarcker idea

[4] E596C Lecture 1 - Backprop Fundamentals (Mon 2025-09-29)
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

[5] E596C Lecture 4 - Regularization (Mon 2025-10-20)
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
```

correct: yes
faithful: yes
note:

---

## G03

**Question:** what did MW show me how to do on GCLU?

**Gold answer:** Marcus Webb showed you how to profile PyTorch code efficiently on the GPU cluster.

**System answer:** MW showed me how to profile PyTorch code efficiently on GCLU by wrapping the region of interest in the built-in profiler instead of timing the entire script [4]. He emphasized profiling only a short window to avoid huge, useless traces and highlighted the importance of looking at CUDA vs CPU time separately [4]. He also demonstrated how to use the trace viewer to see gaps between kernels and identified idle GPU time as a key area to investigate [4].

**Excerpts the system saw:**

```text
[1] PyTorch Profiling on GCLU (Tue 2025-10-21)
## notes to self
- write down MW's steps somewhere permanent before I forget them
- don't profile the whole training loop again, seriously
- ask MW follow-ups in batch, not one ping at a time

[2] GCLU Library Path Fix (thanks MW) (Wed 2025-10-08)
## next
- [ ] write the fix down properly in vault so future me doesn't redo this
- [ ] sanity-check a tiny training run on cluster before real assignment work
- [ ] figure out how job submission works vs interactive session ??

[3] GCLU Overnight Storage Purge (Fri 2025-11-14)
## what happened
- MW warned lab earlier: GCLU storage almost completely full
- overnight -> cluster admins purged old data to free up storage space
- so the warning was basically the heads-up before the wipe. should've taken it more seriously

## what I tried / thinking
- haven't confirmed yet what got purged vs kept ??
- no idea what counts as "old" to admins last access? last modified? ??
- not clear if scratch vs home dirs treated differently ?? -> ask around
- mild panic re: checkpoints + cached datasets, but no point spiraling until I actually look

## open qs
- is there any recovery option or is purged = gone ??
- will this keep happening whenever GCLU fills up?? if so need a habit, not a one-time fix
- where's the actual storage policy written down ?? prob somewhere on wiki nobody reads

## next
- [ ] log in + check own dirs, list what's missing (if annything)
- [ ] ask MW how admins decide what to purge
- [ ] stop treating cluster storage like pemranent storage -> back up important stuff elsewhere
- [ ] clean up my own junk before someone else does it for me

lesson: when MW says storage is full, listen. ugh.

[4] PyTorch Profiling on GCLU (Tue 2025-10-21)
## what happened
- Marcus Webb sat down w/ me & showed how to profile PyTorch code efficiently on GCLU
- before this I was basically guessing where time goes -> sprinkling print timers everywhere lol
- his approach: wrap the region you care about in the built-in profiler instead of timing whole script
  - only profle a short window, not full run -> otherwise trace is huge & useless
  - look at CUDA time vs CPU time separately b/c they tell different stories
  - sort the op table, stare at the top few rows first
- also showed how to pull the trace into the viewer so you can actually *see* gaps between kernels
- big takeaway: idle GPU time is the thing to hunt, not just slow ops

## reactions
- way less painful than I expected
- the trace viewer is kind of addictive ngl
- feel dumb for not doing this sooner

## open qs
- is the dataloader the bottleneck or is that just how it loks on first glance ??
- does prrofiler overhead skew the numbers much on GCLU noodes ??
- waarmup stps -> how many to skip before recording ?? forgot to ask
- how to tell sync points apart from real compute in the trace ??

[5] GCLU Maintenance Downtime (Mon 2025-10-13)
## What happened
- tried to kick off training runs on the GPU cluster this aft -> jobs just hung, couldn't even ssh in reliably
- turns out GCLU was offline for four hours for scheduled network maintenance
  - totally missed the notice?? need to actually read cluster emails lol
- used downtime to clean up configs + reread my data loader code locally so not a total loss

## After it came back
- relaunched -> new problem: import errors, lib not found at runtime
- spent way too long poking at env vars myself, going in circles
- pinged Marcus Webb -> he spotted it fast tricky library path issue, my env was picking up wrong paths
- MW walked me through fixing it, jobs actually start now
  - write down eaxctly what he changed before I forget!!

## Next
- [ ] doc the library path fix in vault so I don't redo this mess
- [ ] check cluster status page before blaming my own code next time
- [ ] watch relaunched jobs make sure they don't silently die
- not sure if maintenance affects queued jobs too?? ask around
- owe Marcus coffee fr
```

correct: yes
faithful: yes
note:

---

## G04

**Question:** What topic were students getting help with during my massive EE 235 office hours session?

**Gold answer:** Fourier series.

**System answer:** Students were getting help with Laplace transforms during the office hours session, specifically with topics like ROC (Region of Convergence) and partial fractions, especially those involving repeated roots [1]. The session also involved working through problems step-by-step and encouraging students to explain their reasoning [3].

**Excerpts the system saw:**

```text
[1] DSEC Laplace Review + SK Covering OFHR (Wed 2025-10-22)
**Who:** me, Sarah Kim, PATL (msgs/quick chat not all at once)

## DSEC - Laplace review
- led review session on Laplace transforms for E235 during DSEC
- went thru basics -> transform pairs, properties, inverse via partial fractions
- students mostly ok w/ table lookups, shakier on ROC stuff + partial fractions w/ repeated roots
- maybe redo ROC w/ more pictures next time?? felt rsuhed

## Office hours coverage
- had dentist appt -> couldn't do my OFHR
- SK covered my E235 OFHR, huge help
- ask SK what ppl came in w/ -> prob same Laplace confusion

## Section time change
- PATL moved my DSEC to **Wednesdays at 4pm**, permanently
- so not a one-off -> fix everything around it
- does this clash w/ anything on my end?? double check

## next steps
- [ ] thank SK for covering OFHR
- [ ] update calendar for new Wednesdays at 4pm slot
- [ ] jot down which Laplace topics students struggled w/ while still fresh
- [ ] ping PATL if anything weird comes up w/ new time

[2] PATL - Final DSEC Slot + Moving OFHR (Mon 2025-10-13)
**Who:** me + Prof. Atlas

quick chat after lecture re: E235 schedulnig stuff

## DSEC
- PATL moved my DSEC to **Wednesdays at 4pm**, permanently
- -> no more shuffling around, this is the final slot
- honestly relieved, the back and forth was getting annoying

## Office hours
- brought up Friday OFHR -> attendance basically dead
- only **three students** showed up last Friday
- b/c of that moving my OFHR to **Wednesdays at 3pm**
- PATL fine w/ it, no pushback
- nice side effect: OFHR right before DSEC -> one block on Wed instead of splitting my week
- will Wed actually pull more people than Fri?? hopefully, Friday afternoon was prob just a bad time

## thoughts
- whole Wed afternoon = E235 now, need to protect that time
- don't schedule anything else Wed afternoon!!
- should I still keep an eye on turnout after the switch?? prob yes, just informally

## Next steps
- [ ] update my calendar w/ new Wed slots
- [ ] make sure students know about the OFHR change ??
- [ ] double check room for Wed (ask if unclear)

[3] OFHR - Only One Student (Wed 2025-11-19)
**Who:** me + 1 student. that's it.

- held E235 OFHR today -> only one student showed up
- kind of expected low turnout?? but still surprised it was literally one
- upside: got to go slow, actually work through stuff w/ them instead of rushing between ppl
- student seemed to get more out of it b/c of the 1-on-1 attention at least that's my read
- spent a lot of the time just sitting there otherwise, lol

**what was said**
- mostly walked throguh their questions step by step
- tried to get them to explain reasoning back to me innstead of me just giving answers -> felt like that worked ok
- they seemed less stuck by the end, hopefully

**Thoughts / open qs**
- why so empty?? timing? ppl not stuck yet? or just not aware OFHR exist??
- not sure if this is a one-off or a pattern don't want to overthink from one session
- maybe worth keeping an eye on turnout before reading into it

**next**
- [ ] jot down anything that came up that might be confusing for others too
- [ ] remind self low attendance != bad session, the one student still got helped

[4] Empty Office Hours (Wed 2025-10-15)
**Attendees:** just me. nobody else showed.

- E235 office hours this afternoon -> completely empty. zero students, the whole time
- context: had already moved OFHR to **Wednesdays at 3pm** b/c Friday attendance was so low
  - so the switch was supposed to fix this.. didn't, at least not today
- spent the slot sitting w/ laptop open half expecting someone to wander in. no one did

### thoughts / open qs
- did students actually nootice the time change?? not sure
- is it the time, or do people just not need help right now?? hard to tell from one empty session
- maybe they're using other channels instead of coming in person?? no idea
- don't want to overreact to a single afternoon

### decided
- nothing new. wednesday slot stays as is for now

### Next steps
- [ ] keep showing up for Wed OFHR, see if anyone comes
- [ ] think aobut why turnout is so low -> revisit when organizing notes Sunday
- [ ] use empty time productivly next time instead of just waiting aorund

mildly demoralizing ngl, but ok. one data point

[5] PATL - DSEC Reschedule (Tue 2025-10-07)
**who:** me, Prof. Atlas (quick chat after his office hrs, his office)

## Context
- realized Thursday 10am discussion section cofnlicts w/ my LABM -> can't be in two places obviously
- should've caught this wk 1 tbh.. calendar was a mess
- brought it up w/ PATL, half expected pushback

## What was said / decided
- PATL was chill abt it, no big deal
- he moved my E235 DSEC to Fridays at 2pm
- -> conflict resolved LABM stays untouched
- relief honestly

## Open qs
- will students who picked Thu slot b/c of their own schedules be ok w/ Fri?? 
- room for Fri - same one or new?? didn't ask dumb
- does this mess w/ how autograder stuff gets discussed in section?? prob not but check

## Next steps
- [ ] update Obsidian calendar + Google cal -> Fri 2pm
- [ ] delete old Thu 10am block so I stop double-booking myself
- [ ] double check no other overlaps hiding in rest of week
- [ ] prep section material w/ new day in mind

note to self: check schdule conflicts BEFORE committing to stuff. lesson learned.
```

correct: No
faithful: Yes
note: I think it didnt see the correct excerpt

---

## G05

**Question:** What were students asking about when my discussion section was packed?

**Gold answer:** Bode plots.

**System answer:** Students were asking about the same part of a problem, which suggests the wording of the question might have been unclear—this was noted during the final exam proctoring when a few students asked about the same section [5]. Additionally, during the packed office hours, the TA ended up working on a whiteboard for the entire room because there were too many students, and repeated confusions kept coming up, indicating that certain concepts were tripping up multiple students [1].

**Excerpts the system saw:**

```text
[1] Final OFHR - Room Packed (Wed 2025-12-03)
## Who
- me (TA)
- students.. lots of them. every seat taken, ppl standing by door

## what happened
- last E235 OFHR of quarter -> room **completely full**
- never seen it like this all quarter lol wheere was everyone weeks ago ??
- couldn't do proper 1-on-1 w/ anyone b/c too many ppl
  - ended up working stuff on whiteboard for whole room instead
  - honestly worked better than expected, same confusions kept coming up
- some ppl just sat + listened, didn't ask anything -> fine, still useful for them prob
- felt kinda rushed at end not sure everyone got their q answered ??

## thoughts
- packed room = sign students were stressed? or just last chance thing
- whiteboard-for-everyone format -> worth remembering if I TA again
- tired but good tired
- kinda sad it's over tbh

## next steps
- [ ] jot down which concepts kept tripping ppl up while still fresh
- [ ] reply to any leftover emails from ppl who didn't get to ask
- [ ] maybe mention crowd thing to Prof. Atlas ?? (just FYI)
- [ ] sleep

[2] Exam Question Submitted, SK Covering DSEC (Wed 2025-11-12)
- [x] proposed exam question for E235 -> submitted to PATL ✅
  - finally off my pate was dragging on this
  - wording ok?? whatever, it's sent
- [x] DSEC today -> skipped SK offered to cover for me
  - huge relief b/c today was packed
- [ ] thank SK properly (coffee??)
- [ ] check if PATL replies re question -> don't obsess tho
- [ ] ask SK how section went, anything students got stuck on??

note to self: owe her one don't forget

[3] E596C - Midterm Day (Mon 2025-11-17)
## context
- E596C MIDT -> finally happened tonght, Monday evening class session
- recap b/c this thing kept moving PLIN announced MIDT delayed *again* -> landed in week 8
  - honestly lost track of how many times it shifted ??
  - kind of a relief to just have it done vs. hanging over everything

## Exam itself
- took it during regular class slot, no separate room drama
- felt ok-ish?? some parts smooth, some parts brain went blank
- pacing weird at start -> rushed toward end, note to self: skim whole thing first next time
- couple qs I second-guessed, prob overthinking
- handwriting got bad near end lol

## Post-exam thoughts
- glad I kept reviewing even w/ the delays, otherwise would've forgotten stuff
- weird feeling, class is still on but exam pressure gone
- don't know how grading will go -> no point stressing rn
- ?? will solutions get posted or just scores back

[4] OFHR - Only One Student (Wed 2025-11-19)
**Who:** me + 1 student. that's it.

- held E235 OFHR today -> only one student showed up
- kind of expected low turnout?? but still surprised it was literally one
- upside: got to go slow, actually work through stuff w/ them instead of rushing between ppl
- student seemed to get more out of it b/c of the 1-on-1 attention at least that's my read
- spent a lot of the time just sitting there otherwise, lol

**what was said**
- mostly walked throguh their questions step by step
- tried to get them to explain reasoning back to me innstead of me just giving answers -> felt like that worked ok
- they seemed less stuck by the end, hopefully

**Thoughts / open qs**
- why so empty?? timing? ppl not stuck yet? or just not aware OFHR exist??
- not sure if this is a one-off or a pattern don't want to overthink from one session
- maybe worth keeping an eye on turnout before reading into it

**next**
- [ ] jot down anything that came up that might be confusing for others too
- [ ] remind self low attendance != bad session, the one student still got helped

[5] E235 Final Exam Proctoring (Fri 2025-12-05)
**Who:** me, SK, PATL

## Context
- proctored the E235 final today all three of us in the room
- mostly quiet -> walked aisles, answered clarification qs, collected exams at end

## Notes
- PATL approved my E235 final exam question w/ minor edits -> relief was nervous it'd get cut
  - edits were small moostly wording
  - good sign my problem-writing is getting closer to what he wants??
- SK + me split the room so neither of us was stuck at front the whole time, worked fine
- few students asked about same part of a problem -> maybe wording could've been clearer?? worth remembering for next time I write one
- PATL seemed fine w/ how proctoring went, no complaints

## open qs
- how exactly do grading logistics split btwn TAs?? didn't come up, should ask
- does my question get reused or archived?? curious

## next steps
- [ ] jot down my own takeaways on writing exam qs while still fresh
- [ ] check in w/ SK about anything we noticed during proctoring
- [ ] reread my question w/ his edits to see what changed + why

feeling: tierd but good. end of quarter energy. long day after a long week, need sleep before Sunday reorg of vault
```

correct: No
faithful: Yes
note: I think it didnt see the correct excerpt

---

## G06

**Question:** As of October 25, when I spent all Saturday studying, which week was the deep learning midterm scheduled for?

**Gold answer:** Week 5.

**System answer:** As of October 25, when you spent all Saturday studying, the deep learning midterm was scheduled for week 7 [2].

**Excerpts the system saw:**

```text
[1] Midterm Study Day - Backprop Review (Sat 2025-10-25)
Spent all day Saturday studying for the upcoming EE P 596 C midterm exam -> ging back over backprop since it's the foundation for everything else.

Source: my notes from the first E596C lecture, which covered backpropagation fundamentals + re-derived stuff by hand

## key pts
- backprop = chain rule applied systematically over a computational graph
- forward pass: compute + **cache** intermediate values (needed later!!)
- backward pass: upstream grad x local grad -> pass downstream
- each node only needs to know its own local derivative -> modular, nice
- branching paths -> grads **add** at merge pts (kept forgetting this)
- matrix case: check shapes dL/dW must match shape of W -> good sanity check
- sigmoid local grad = s(1 - s) -> saturates at extremes -> vanishing grads ??

## Reactions
- scalar version clicks now, vectorized/Jacobian version still shaky
- why is reverse mode cheaper than forward mode for nets?? I think b/c one scalar loss, many params -> one backward sweep gets all grads. confirm
- drawing graph first, then gradients, helped a LOT vs. just pushing symbols
- ReLU grad at exactly zero -> just pick a convention??

[2] E596C Lecture 5 - Midterm Delayed, CNN Intro (Mon 2025-10-27)
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

[3] Weekly Plan - Week 5 (Sun 2025-10-26)
## E596C
- studied all day Saturday for MIDT -> brain fried
- [ ] keep going on MIDT prep, don't lose momentum
- [ ] list topics still shaky ??

## E596A
- Prof. Seitz exxtended assigmnent deadline by exactly two days!! huge relief
- [ ] use the extra two days well, don't procrastinate b/c of it
- [ ] double check what PSTE actually said re extension -> confirm on course page

## misc
- [ ] sleep more??
- [ ] clean up vault notes from this week
- reminder to self one thing at a time

[4] E596C - Midterm Day (Mon 2025-11-17)
## Misc / reminders to self
- - [ ] look back over my scratch work while still fresh figure out where I got stuck
- - [ ] clean up deep learning notes in vault, they're a mess from cramming
- - [ ] sleep. seriously
- try not to obsess over individual answers tonight
- maybe revisit topics I felt shaky on, even w/o exam pressure -> useful for AutoNav anyway

## Vibe check
- tired but done
- the repeated delays made it feel bigger than it was
- moving on -> rest of week stuff tomorrow

[5] E596C Lecture 6 - CNNs, Midterm Moved to Wk8 (Mon 2025-11-03)
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
```

correct: No
faithful: Yes
note: It picked the info from oct 27, even though the questions specifies oct 25

---

## G07

**Question:** What did Sarah Kim contribute to the EE 235 grading script, when did I finalize it, and when did I finish grading my stack of final exams?

**Gold answer:** In week 5, Sarah Kim sent me her half of the automated grading script. On November 30, I finalized it for the final exams. I finished grading my assigned stack of final exams on December 6.

**System answer:** Sarah Kim sent over her half of the E235 automated grading script, which was merged with yours to finalize the grading script [1]. The script was finalized on Sun 2025-11-30 [1]. You finished grading your stack of E235 final exams on Sat 2025-12-06 [2].

**Excerpts the system saw:**

```text
[1] E235 Final Exam Grading Script (Sun 2025-11-30)
## what happened
- SK sent over her half of the E235 automated grading script -> finally have both pieces in one place
- merged her part w/ mine, read through the whole thing end to end
- -> finalized the E235 grading script for the final exams
- relief honestly this one had been hanging over me

## what I tried / notes
- first pass at merging = messy her naming style vs mine didn't line up perfectly
- spent a while just reading her logic before touching anything b/c didn't want to break stuff I didn't understand
- tolerance handling for numeric answers -> looked fine on both sides, nothing obviously off
- partial credit logic was the part I was most nervous about seems ok now??
- a few spots where we both wrote helper-ish code that overlaps -> left it for now not worth the risk of refactoring at this stage

## open qs
- edge cases w/ weird student formatting (extra spaces, units written in) — did we cover enough?? not sure
- does output format mtach what the gradebook side expects?? should double check
- any section where her half + my half disagree on rounding?? didn't spot any but eyes were tired

[2] E235 Final Grading Finished (Sat 2025-12-06)
- [x] proctored E235 fnial w/ SK + PATL -> long morning, room was freezing
- [x] finished grading my assigned stack of E235 finals!!
  - finally done, hand cramping lol
- [ ] re-skim my stack once more?? just to be safe
- [ ] tidy up grading notes -> messy scribbles everywhere
- [ ] clear desk return red pens
- [ ] actually sleep tonight

weird feleing w/ grading off my plate. still feels like smth is missing ??
remind self: don't open laptop til tmrw b/c brain = fied

[3] E235 Grading Done (Tue 2025-10-14)
## E235 gading

- [x] grade first batch of E235 submissions -> Sarah Kim asked me to take this one
- [x] finished grading the whole homework batch!! done done done
- [ ] tell SK it's finished
- [ ] double-check nothing got skipped?? scroll through once more
- [ ] note down weird edge cases while still frsh

scribbles:
- took longer than expected ugh
- some answers were hard to read -> just be consistent w/ partial credit
- feels good to cross this off b/c it was hanging over me all week

[4] E235 TA Kickoff with PATL (Wed 2025-10-01)
**Who:** Prof. Atlas, Sarah Kim, me

quick kickoff for EE 235 TA stuff. Short mostly logistics

## Discussed
- PATL assigned me to teach the E235 discussion section on **Thursdays at 10am**
  - -> so I own the DSEC, not shared
  - first time leading a section solo.. slightly nervous lol
- SK + me split remaining TA duties details still fuzzy
  - autograding scripts = joint w/ SK, who does what?? not decided yet
- PATL wants section to reinforce lecture material, not introduce new stuff
  - format of worksheets?? didn't really get to it, ran out of time

## open qs
- do I prep my own materials or does PATL send something each week??
- attendance tracked or not??
- where are past section notes do they even exist??

## Next steps
- [ ] email PATL re: section materials question
- [ ] ping SK to sort out script spilt
- [ ] block Thursday mornings on calendar so nothing else lands there
- [ ] skim intro lecture slides before first DSEC

feels manageable as long as prep doesn't eat into my own coursework -> watch that

[5] E235 Grading - Batch 1 (Wed 2025-10-08)
Sarah Kim pinged -> wants me to grade first batch of E235 submissions

- [ ] pull batch 1 from coruse site
- [ ] cheeck rubric w/ SK before starting??
- [ ] skim a few subs first -> get sense of common mistakes
- [ ] grade batch
- [ ] flag weird/borderline ones, don't guess
- [ ] leave short comments, not essays
- [ ] sanity check scores at end b/c fatigue = inconsistent
- [ ] msg SK when done

notes:
- partial credit policy?? ask
- do this in one sitting if possible, context switching kills me
- ugh handwriting scans
```

correct: Yes
faithful: Yes
note:

---

## G08

**Question:** Where did I get the AutoNav poster printed?

**Gold answer:** At the university library.

**System answer:** You got the AutoNav poster printed at the university library [2].

**Excerpts the system saw:**

```text
[1] Department Showcase with PFOX (Thu 2025-12-04)
**Who:** PFOX + me

**where:** dept showcase, ANAV poster sesson

## Prep
- printed ANAV poster at univ library -> came out ok, colors a bit darker than on screen?? whatever readable
- carried it over rolled up, slightly wrinkled corner, nobody noticed (hopefully)

## at the showcase
- PFOX and I presented ANAV pster together
- split talking roughly -> PFOX did big-picture framing, I did the details / figures
- lots of ppl stopping by, some quick drive-bys some longer convos
- got a bunch of qs on the perception side, mostly "why lightweight" type stuff -> answered ok I think
- felt kinda nervous first few visitors got smoother after
- PFOX seemed happy w/ how it went (?? didn't say much explicitly, but good vibe)

## random thoughts
- should practice short pitch more, my explanation ran long a few times
- people liked visuals more than text-heavy parts -> note to self for future posters
- some qs I didn't have crisp answers for... can't remember all of them exactly ugh should've written them down live

[2] ANAV Poster Printed (Mon 2025-12-01)
## Tried
- laid out ANAV poster in Illustrator
  - blocks for motivation / perception mdel / results / takeaways
  - fought w/ alignment guides forever snapping kept grabbing wrong edge
  - exported -> checked on screen looked ok-ish?? hard to tell at real scale
- printed it at the university library

## what happened
- print came out fine overall -> rlief
- colors a bit darker than on monitor, esp. the figure backgrounds
  - b/c screen vs paper, always happens should've expected
- small text in captions borderline readable from a step back ??
- whitspace on one side looks uneven wasn't obvious in Illustrator
- overall legit looks like a real poster now, not a slide deck pasted together

## Notes to self
- keep Illustrator file organized, layers were a mess by the end
- next time do a test print of one section first?? would've caught the color thing
- save print settings somewhere so not guessing again

## Next
- [ ] look over printed ANAV poster again w/ fresh eyes
- [ ] jot down anything that bugs me in the layout
- ?? whether capton size actually matters or I'm overthinking

feels good to have something physical for ANAV finally

[3] Weekly Plan - Week 10 (Sun 2025-11-30)
## carryover / done-ish

- [x] E235 grading script for final exams -> finalized
  - finally. no more weird edge cases pls
  - re-read once more w/ fresh eyes?? prob fine
- [x] ANAV poster layout -> designed in Illustrator
  - spacing feels cramped near bottom?? idk
  - colors ok on laptop unsure how they print

## misc

- [ ] skim this list again before bed b/c brain is fried
- [ ] don't forget to sleep lol

> Week 10 feels like a lot -> one thing at a time

[4] E596C Final Lecture - Wrap-Up (Mon 2025-12-01)
## Open questions for myself
- did I really get backprop through conv layers or just pattern-match?? redo one by hand at some point
- how much of this transfers to edge deployment constraints? quantization etc wasn't the focus here

## To self
- [ ] dump CNN notes into vault properly on Sunday, link to CV + AutoNav pages
- [ ] clean up problem set notes before I forget what my scribbles mean
- breathe. one less thing.

[5] ANAV Poster Layout in Illustrator (Sat 2025-11-29)
## what I tried
- designed the ANAV poster layout in Illustrator today
- started from blank artboard instead of a template -> more control but way slower than expected
- messed around w/ guides + grid snapping, kept nudging text boxes by hand anyway lol
- placeholder boxes for figures, real plots not dropped in yet
- fought w/ fonts for way too long. why does Illustrator make text frames so annoying ??

## what happeened
- overall structure feels ok reads left -> right roughly like the story of the project
- whitespace looks uneven in spots, some secions cramped, otheers empty
- color choices = undecided, everything grayscale for now b/c didn't want to bikeshed
- exported a quick preview looks very different zoomed out vs zoomed in -> need to check at actual print scale somehow ??
- title area too busy?? not sure

## next
- [ ] swap placeholders for real figures once I pull them
- [ ] clean up alignment, stop eyeballing
- [ ] ask PFOX if layyout direction makes sense before polishing further
- [ ] figure out if lab has a poster template I should've used (oops)

notes to self:
- save versions often Illustrator crashed once already today, lost a bit of work
- don't spend all weeend on pixel pushing, content matters more
- ugh design is not my strong suit
```

correct: Yes
faithful: Yes
note:

---

## G09

**Question:** As of October 30, which week was the EE P 596 C midterm set for?

**Gold answer:** Week 7. Prof. Lindqvist had delayed it from week 5.

**System answer:** As of October 30, the EE P 596 C midterm was set for week 5 [5].

**Excerpts the system saw:**

```text
[1] Weekly Plan - Week 2 (Sun 2025-10-05)
## EE 235
- [ ] PATL assigned me Thurs 10am discussion section -> confirm room location??
- [ ] prep outline for first DSEC, keep it short
- [ ] skim E235 lecure slides bfeore Thurs
- [ ] check what OH looks like, ask around??

## EE P 500 D
- [x] bought required textbook
- [ ] start reading, figure out which chapters map to week 2 ??
- [ ] look at reflection format for E500D, don't wing it

## misc
- [ ] block calendar time b/c Thurs is now packed -> morning section + CV at night
- [ ] sleep more lol

[2] Weekly Plan - Week 4 (Sun 2025-10-19)
## EE P 596 A
- [ ] read thru first big coding assignmnet from Prof. Seitz -> finally out
- [ ] skim starter code before diving in
- ?? what exactly PSTE wants in the writeup -> check handout again
- [ ] set up env for E596A stuff, don't wait till last min

## EE P 500 D
- [ ] finish first reading reflection (already started, rough draft only)
- [ ] clean up messy notes from the reading -> tie back to main argument
- E500D reflection feels thin rn... needs more own take, less summary

## misc
- [ ] Sunday review again next wk, don't let inbox pile up
- coffee. lots of it

[3] E596C - Midterm Day (Mon 2025-11-17)
## Misc / reminders to self
- - [ ] look back over my scratch work while still fresh figure out where I got stuck
- - [ ] clean up deep learning notes in vault, they're a mess from cramming
- - [ ] sleep. seriously
- try not to obsess over individual answers tonight
- maybe revisit topics I felt shaky on, even w/o exam pressure -> useful for AutoNav anyway

## Vibe check
- tired but done
- the repeated delays made it feel bigger than it was
- moving on -> rest of week stuff tomorrow

[4] Midterm Study Day - Backprop Review (Sat 2025-10-25)
Spent all day Saturday studying for the upcoming EE P 596 C midterm exam -> ging back over backprop since it's the foundation for everything else.

Source: my notes from the first E596C lecture, which covered backpropagation fundamentals + re-derived stuff by hand

## key pts
- backprop = chain rule applied systematically over a computational graph
- forward pass: compute + **cache** intermediate values (needed later!!)
- backward pass: upstream grad x local grad -> pass downstream
- each node only needs to know its own local derivative -> modular, nice
- branching paths -> grads **add** at merge pts (kept forgetting this)
- matrix case: check shapes dL/dW must match shape of W -> good sanity check
- sigmoid local grad = s(1 - s) -> saturates at extremes -> vanishing grads ??

## Reactions
- scalar version clicks now, vectorized/Jacobian version still shaky
- why is reverse mode cheaper than forward mode for nets?? I think b/c one scalar loss, many params -> one backward sweep gets all grads. confirm
- drawing graph first, then gradients, helped a LOT vs. just pushing symbols
- ReLU grad at exactly zero -> just pick a convention??

[5] E596C Lecture 1 - Backprop Fundamentals (Mon 2025-09-29)
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
```

correct: No
faithful: Yes
note: It didnt fetch the excerpt from the correct date

---

## G10

**Question:** When was the deep learning midterm originally supposed to be, and when did I actually end up taking it?

**Gold answer:** It was originally announced for week 5. After being delayed more than once, it landed in week 8, and I took it on Monday, November 17, during the evening class session.

**System answer:** The deep learning midterm was originally supposed to be during week 5 [2]. You actually ended up taking it in week 8 [3].

**Excerpts the system saw:**

```text
[1] E596C - Midterm Day (Mon 2025-11-17)
## Misc / reminders to self
- - [ ] look back over my scratch work while still fresh figure out where I got stuck
- - [ ] clean up deep learning notes in vault, they're a mess from cramming
- - [ ] sleep. seriously
- try not to obsess over individual answers tonight
- maybe revisit topics I felt shaky on, even w/o exam pressure -> useful for AutoNav anyway

## Vibe check
- tired but done
- the repeated delays made it feel bigger than it was
- moving on -> rest of week stuff tomorrow

[2] E596C Lecture 2 - Gradient Descent (Mon 2025-10-06)
## Admin
- Prof. Lindqvist: midterm exam for EE P 596 C happening during week 5 -> start reviewing early, don't cram
- ?? what's covered on MIDT - everything up to then or just optimization stuff
- side note: already finished first set of E596C problem sets on gradient descent -> nice timing lecture lined up w/ what I did

## Gradient descent basics
- goal minimize loss L(θ) by stepping opposite gradient
- update: θ <- θ - η ∇L(θ)
- η = learning rate -> too big = overshoot / diverge too sall = crawls forever
- PLIN drew the classic bowl picture -> gradient points uphill so negate
- convex case = guaranteed to raech global min (w/ reasonable η)
- non-convex (aka basically every neural net) -> local mins, saddle pts, plateaus

## Batch vs stochastic vs mini-batch
- full batch: exact gradient, expensive per step
- SGD single sample, noisy but cheap
- mini-batch: middle ground, what everyone actually uses b/c GPU parallelism
- noise in SGD can help escape saddle pts?? -> he said yes-ish, intuition not proof

[3] E596C Lecture 6 - CNNs, Midterm Moved to Wk8 (Mon 2025-11-03)
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

[4] E500D Textbook Ch. 1 - Intro to Agents (Sun 2025-10-05)
## reactions
- PEAS feels obvious but actually forces clarity, could use for my own projects
- where do LLM agents fit?? utility-based w/ fuzzy utility? or just facy reflex w/ huge context as "state"
- partial observability + continuous = basically every real robotics problem, intro glosses over how hard that is
- "problem generator" = exploration -> link to RL stuff from deep learning class
- curious how E500D readings bridge this classic framing to modern agentic systems

- [ ] jot reflection thoughts while fresh

[5] Fourier Series OFHR Rush (Wed 2025-10-29)
**who:** me + tons of E235 students (way more than usual, lost count lol)

**what:** massive OFHR session basically all Fourier series all the time

## what came up
- most ppl stuck on same stuff -> computing coefficients, esp. setting up the integral over one period
- lots of confusion re: even/odd symmetry shortcuts -> when can you just drop the sine or cosine terms??
- some mixing up trig form vs complex exponential form -> walked thru how they relate on whiteboard, multiple times
- couple ppl asking about what the coefficients actually *mean* physically -> tried the "how much of each frequency" framing, seemed to land
- someone asked abt convergence at discontinuities -> gave quick answer, not sure it was super clean ??

## notes to self
- whiteboard got packed fast had to keep erasing -> annoying
- ended up repeating same explanation over and over b/c ppl kept arriving at diff times
- energy was good tho, students seemed less panicked by the end
- felt pretty drained after but ok
```

correct: Yes
faithful: Yes
note:

---

## G11

**Question:** In week 2, after the lab meeting conflict came up, when was my EE 235 discussion section scheduled?

**Gold answer:** Fridays at 2pm. Prof. Atlas moved it there on October 7.

**System answer:** In week 2, your EE 235 discussion section was initially scheduled for Thursdays at 10am [2]. However, due to the conflict with your LABM meeting, it was rescheduled to Fridays at 2pm [3].

**Excerpts the system saw:**

```text
[1] Schedule Conflict - DSEC vs LABM (Mon 2025-10-06)
- PATL put me on the EE 235 discussion section -> Thursdays 10am
- just realized: Thursday 10am = my lab meeting slot. direct conflict ugh
- how did I not catch this earlier??

half-formed options:
- swap DSEC time w/ someone?? not sure if that's even allowed for E235
- ask if LABM can shift?? prob not, whole group's schedule
- join LABM remotely / late?? -> feels bad miss updates
- catch up via notes/slides after LABM?

questions
- who do I ask first - PATL or lab side??
- is the section time fixed b/c of room booking?
- how flexible is any of this in week 2 vs later

- [ ] figure out who to email before this turns into a recurring mess

feels like one of those things that'll get worse if I wait

[2] Weekly Plan - Week 2 (Sun 2025-10-05)
## EE 235
- [ ] PATL assigned me Thurs 10am discussion section -> confirm room location??
- [ ] prep outline for first DSEC, keep it short
- [ ] skim E235 lecure slides bfeore Thurs
- [ ] check what OH looks like, ask around??

## EE P 500 D
- [x] bought required textbook
- [ ] start reading, figure out which chapters map to week 2 ??
- [ ] look at reflection format for E500D, don't wing it

## misc
- [ ] block calendar time b/c Thurs is now packed -> morning section + CV at night
- [ ] sleep more lol

[3] PATL - DSEC Reschedule (Tue 2025-10-07)
**who:** me, Prof. Atlas (quick chat after his office hrs, his office)

## Context
- realized Thursday 10am discussion section cofnlicts w/ my LABM -> can't be in two places obviously
- should've caught this wk 1 tbh.. calendar was a mess
- brought it up w/ PATL, half expected pushback

## What was said / decided
- PATL was chill abt it, no big deal
- he moved my E235 DSEC to Fridays at 2pm
- -> conflict resolved LABM stays untouched
- relief honestly

## Open qs
- will students who picked Thu slot b/c of their own schedules be ok w/ Fri?? 
- room for Fri - same one or new?? didn't ask dumb
- does this mess w/ how autograder stuff gets discussed in section?? prob not but check

## Next steps
- [ ] update Obsidian calendar + Google cal -> Fri 2pm
- [ ] delete old Thu 10am block so I stop double-booking myself
- [ ] double check no other overlaps hiding in rest of week
- [ ] prep section material w/ new day in mind

note to self: check schdule conflicts BEFORE committing to stuff. lesson learned.

[4] LABM - Back to Python (Mon 2025-11-10)
**who:** me, Prof. Fox (+ rest of lab, didn't track everyone)

## context
- came into lab meeting w/ update: finished porting core ANAV logic to C++ -> finally done
- was kind of proud of this tbh, lots of evenings on it

## Discussion
- Prof. Fox asked how fast we can try new ideas w/ C++ setup -> honest answer: slow
  - every small change = rebuild debug, rebuild
  - perception experiments need quick turnaround, C++ fights that
- general feeling in room: speed of iteration > raw runtime speed right now
- **Decision:** switch ANAV backend back to Python for faster iteration
  - yes right after C++ port finished. oof
- C++ work not totally wasted?? -> maybe useful later for deployment side didn't really settle that

## My take
- anonying but makes sense b/c project still in exploring phase
- lesson -> ask about iteration needs *before* big port next time
- keep C++ bracnh around, don't delete

[5] First ANAV Lab Meeting - Repo Architecture (Thu 2025-10-09)
**who:** me, Prof. Fox (+ rest of lab, didn't catch everyone's names yet lol)

## Context
- first lab meeting for AutoNav -> whole ting was about repo architecture
- mosttly listening, still getting oriented

## Notes from discussion
- PFOX walked through how repo is laid out / how pieces are supposed to fit
- perception module = my corner of things, so paid most attention there
- lots of talk re: keeping structure clean so ppl don't step on each other -> makes sense w/ multiple ppl touching same codebase
- didn't fully follow some of the reasoning on module boundaries ?? -> reread repo before next LABM
- unsure where shared utils are supposed to live vs module-specific code ??
- felt a bit lost on naming conventions, prob just b/c it's week 1 of me in this repo

## Me / after mtg
- configured my local env for ANAV perception module
- went mostly ok couple of dependency annoyances but sorted
- should write down what I did so I don't have to redo from memory later
```

correct: Yes 
faithful: Yes
note:

---

## G12

**Question:** After Ryan and I decided to go open-source with EchoSense, why did we change our minds?

**Gold answer:** We switched the target back to the smart home workshop because its deadline was extended.

**System answer:** We changed our minds because the open-source direction felt right for a side project, as it reduced pressure to polish everything for one narrow use and allowed others to contribute, potentially finding bugs we might have missed [1]. This shift was also seen as relieving, as it meant less need for perfection and more room for community input [1].

**Excerpts the system saw:**

```text
[1] ECHO Sync - Pivot to Open Source (Fri 2025-10-17)
**Attendees:** me, Ryan Park

quick sync on EchoSense direction Short call but kind of a big shift.

## Discussion
- talked through where ECHO should actually end up -> kept circling back to who'd use it
- **decision:** target open-source release instead
  - feels right for a side project less pressure to polish everything for one narrow use
  - other ppl can poke at it, maybe find bugs we'd miss
  - honestly kind of relieved tbh
- RP shared initial data collection script
  - skimmed it during call, looks clean-ish
  - need to actually run it myself beffore saying anthing smart about it
  - not sure how it handles mic config differences ??

## Open qs
- what does open source change re: repo strutcure / docs ??
- license?? no idea which one makes sense didn't discuss
- how much cleanup before anything goes puublic ??
- does this change what data we collect at all? b/c public dataset concerns maybe ??

## Next steps
- [ ] pull RP's script + read through properly
- [ ] jot down questions on it before next sync
- [ ] think about what open-source framing means for the README

misc: don't let this side project eat into coursework/TA time this week -> keep it light

[2] ECHO Feature Extraction Bug (Fri 2025-10-24)
## What happened
- Ryan Park pinged re **critical bug** in EchoSense feature extraction step
  - his words: "critical" -> taking seriously, everything downstream depends on features
  - haven't seen exact failure myself yet -> need his repro / logs
- open qs:
  - is it the extraction code itself or upstream audio loding?? 
  - silent bad output vs crash?? silent = way worse means anything tained on these features is suspect
  - when did it get introduced?? check reccent commits

## target change
- deadline got extended -> switched ECHO target **back to the workshop**
  - honestly relief, bug would've been painful otherwise
  - extra time should go to fixing this properly, not hacking around it

## tried so far
- nothing concrete yet on my end, only read RP's report
- skimmed extraction code nothing obvious jumped out -> prob need actual failing input to see it

## next
- [ ] get repro case + logs from RP
- [ ] run extraction on known-good sample, compare outputs
- [ ] diff recent changes to feature extraction step
- [ ] once fixed -> sanity check features before any more training
- [ ] upadte shared task list w/ new workshop target

note to self don't let this eat into coursework time, timebox debugging b/c it can spiral

[3] ECHO Got Starred - Next Steps (Tue 2025-12-02)
- RP texted me today -> ECHO got starred by a major tech company!! wild
- context: RP published the ECHO repo on the open-source portal, didn't expect anyone big to notice this fast

## half-formed thoughts
- who exactly starred it?? one engineer browsing or something more deliberate
- README probably needs cleanup now that ppl are actually looking -> setup steps demo audio clips??
- licensing -> did we even pick one properly?? chheck w/ Ryan
- issues/PRs might start coming in -> who triages, me or Ryan??
- worth writing up model/power tradeoffs as short blog post? or too early
- don't let this eat time from coursework + TA sttuff b/c end of quarter

- [ ] ask Ryan what he knows re the star
- [ ] skim repo w/ fresh eyes, note embarrassing bits

[4] ECHO Data Collection Script (Fri 2025-10-10)
## What happened
- Ryan Park shared initial data collection script for EchoSense -> finally something concrete to poke at
- skimmed through it structure looks reasonable at first glance
- open qs while reading:
  - how is auudio chunked / windowed?? need to check before trusting any of it
  - is sample rate hardcoded or configurable??
  - where do labels come from -> manual tagging or some auto heuristic??
  - any metadata logged w/ each clip (room, device, time)?? would matter later for anomaly stuff
- feels like a good starting base, not trying to rewrite it, just understand it first

## Decision
- talked w/ RP -> we're submitting ECHO to a smart home workshop
- kinda exciting also kinda scary lol
- means data collection quality matters way more now b/c reviewers will ask about it

## next
- [ ] actually read script line by line, not just skim
- [ ] write down my questions + send to RP instead of guessing
- [ ] look up workshop page -> what format / scope do they want??
- [ ] think about what "low-power" claim needs for evidence?? don't want to overpromise

## notes to self
- don't let this eat into coursework time, side project = side project
- keep log updated so Sunday cleanup is less painful

[5] ECHO - Smart Home Workshop Submission? (Thu 2025-10-02)
- talked w/ Ryan Park after class -> decided: we're submitting EchoSense to a smart home workshop
- feels kinda early?? but workshop venue = lower bar good forcing function

**half-formed thoughts**
- what's the actual story for ECHO? low-power angle vs anomaly detection accuracy -> prob can't sell both equally
- do we even have enough results yet?? need to check what's actually working
- framing: "always-on acoustic sensing on tiny hw" -> sounds nice is it true tho
- privacy angle for smart homes -> reviewers will def ask about it
- who writes what?? split w/ RP, maybe he takes hw side, me model side?

- [ ] look up workshop format / page limits
- [ ] ask RP what figs he thinks we need

idk, exciting but don't let this eat into coursework b/c TA stuff too ugh
```

correct: Yes
faithful: Yes
note:

---

## G13

**Question:** What topic did my Agentic AI final paper end up on, what had I originally planned, and when did I submit it?

**Gold answer:** I first planned to write about LLM tool use, then switched to multi-agent reinforcement learning. I submitted the paper on December 3.

**System answer:** Your Agentic AI final paper ended up on the topic of multi-agent reinforcement learning (MARL), which you switched to from your original plan of focusing on E500D paper topic related to LLM agent coordination [1]. You originally planned to work on a topic involving LLM agents coordinating, which you felt was too narrow [1]. The paper was submitted on Wednesday, 2025-12-03 [3].

**Excerpts the system saw:**

```text
[1] Switching E500D Paper to MARL (Mon 2025-11-24)
- ok decided: switching E500D paper topic -> multi-agent reinforcement learning
- old topic felt too thin?? MARL has way more to dig into re: agents coordinating
- half-formed angles:
  - credit assignment w/ many agents -> how do LLM agent setups handle this??
  - emergent communication b/w agents.. too broad?
  - centralized training / decentralized execution -> maybe tie to edge stuff later??
- q: does this still fit what weekly reflections have been coevring? prob yes, looely
- classes canceled entire Thanksgiving week -> no lecture to sanity check w/ anyone, just me + papers
- need to not overscope b/c always do that
- [ ] skim MARL survey papers, figure out what's actually open
- [ ] jot 2-3 candidate research questions before committing further
- ?? is switching this late dumb eh. feels right

[2] MARL Survey Reading (Wed 2025-11-26)
## reactions
- this connects way better to agentic AI stuff than my old topic did -> multiple LLM agents coordinating is basically a MARL problem w/o the RL formalism??
- CTDE framing might map onto planner + executor agent setups
- not sure how much of classic MARL theory traansfers to language aegnts tbh
- eval section weak lots of toy benchmarks

**decision: switching E500D paper topic to multi-agent RL.** feels like more to say + better fit w/ course readings

- [ ] dig up follow-up papers on credit assignment
- [ ] figure out angle -> survey-ish vs small experiment??
- [ ] reread comms section, missed stuff

[3] E500D Final Paper Submitted (Wed 2025-12-03)
### reactions
- relief mostly. also kind of proud of how the argument came together
- writing this forced me to actually synthesize the weekly readings instead of treating them as separate
- open q: is any of this worth extending into something bigger?? ties into agent stuff I care about

- [ ] archive drafts + bib file somewhere sane in the vault
- [ ] jot down ideas I cut from the paper before I forget them

[4] E500D Reflection 3 Submitted (Mon 2025-11-10)
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

[5] MARL Survey Reading (Wed 2025-11-26)
skimmed most of the MARL survey tonight, notes while fresh

## key pts
- core problem = non-stationarity -> each agent's env keeps shifting b/c other agents are learning at same time
- settings split: cooperative / competitive / mixed
- centralized training w/ decentralized execution (CTDE) seems like the dominant paradigm
  - critic sees global state during training, actors only use local obs at runtime
- cerdit assignment in shared-reward setups = still messy value decomposition approaches try to fix
- communication learning section -> agents learn what msgs to send, interesting but felt hand-wavy
- scalability joint acion space blows up w/ # agents, mean-field style approx as workaround
```

correct: Yes
faithful: Yes
note:

---

## G14

**Question:** As of week 2, when were my EE 235 office hours held?

**Gold answer:** Fridays at 3pm.

**System answer:** As of week 2, your EE 235 office hours were held on Fridays at 3pm [3]. This change was made because Friday attendance was low, and moving to Wednesdays at 3pm was discussed as a potential solution [1]. However, the initial official posting of the Friday time was noted in excerpt [3], which states: "add EE 235 office hours to calendar -> Fridays at 3pm, official now" [3]. Therefore, at the time of week 2, the office hours were officially scheduled for Fridays at 3pm.

**Excerpts the system saw:**

```text
[1] PATL - Final DSEC Slot + Moving OFHR (Mon 2025-10-13)
**Who:** me + Prof. Atlas

quick chat after lecture re: E235 schedulnig stuff

## DSEC
- PATL moved my DSEC to **Wednesdays at 4pm**, permanently
- -> no more shuffling around, this is the final slot
- honestly relieved, the back and forth was getting annoying

## Office hours
- brought up Friday OFHR -> attendance basically dead
- only **three students** showed up last Friday
- b/c of that moving my OFHR to **Wednesdays at 3pm**
- PATL fine w/ it, no pushback
- nice side effect: OFHR right before DSEC -> one block on Wed instead of splitting my week
- will Wed actually pull more people than Fri?? hopefully, Friday afternoon was prob just a bad time

## thoughts
- whole Wed afternoon = E235 now, need to protect that time
- don't schedule anything else Wed afternoon!!
- should I still keep an eye on turnout after the switch?? prob yes, just informally

## Next steps
- [ ] update my calendar w/ new Wed slots
- [ ] make sure students know about the OFHR change ??
- [ ] double check room for Wed (ask if unclear)

[2] OFHR - Only One Student (Wed 2025-11-19)
**Who:** me + 1 student. that's it.

- held E235 OFHR today -> only one student showed up
- kind of expected low turnout?? but still surprised it was literally one
- upside: got to go slow, actually work through stuff w/ them instead of rushing between ppl
- student seemed to get more out of it b/c of the 1-on-1 attention at least that's my read
- spent a lot of the time just sitting there otherwise, lol

**what was said**
- mostly walked throguh their questions step by step
- tried to get them to explain reasoning back to me innstead of me just giving answers -> felt like that worked ok
- they seemed less stuck by the end, hopefully

**Thoughts / open qs**
- why so empty?? timing? ppl not stuck yet? or just not aware OFHR exist??
- not sure if this is a one-off or a pattern don't want to overthink from one session
- maybe worth keeping an eye on turnout before reading into it

**next**
- [ ] jot down anything that came up that might be confusing for others too
- [ ] remind self low attendance != bad session, the one student still got helped

[3] Friday TA Logistics + Coffee (Fri 2025-10-03)
- [ ] add EE 235 office hours to calendar -> Fridays at 3pm, official now
- [ ] update Canvas/syllabus page w/ OFHR time ?? check if Prof. Atlas wants to post it himself
- [ ] block Friday mornings for cofefe w/ Chloe Nguyen -> every Friday this quarter, agreed
- [ ] set recurring reminder so I don't double-book mornings
- [ ] prep something to do during E235 slots if nobody shows up (wk 1 prob quiet)

notes:
- coffee w/ CN = good anchor before the 3pm block, don't skip it b/c of work
- where do I hold OFHR?? room not confirmed yet

[4] Empty Office Hours (Wed 2025-10-15)
**Attendees:** just me. nobody else showed.

- E235 office hours this afternoon -> completely empty. zero students, the whole time
- context: had already moved OFHR to **Wednesdays at 3pm** b/c Friday attendance was so low
  - so the switch was supposed to fix this.. didn't, at least not today
- spent the slot sitting w/ laptop open half expecting someone to wander in. no one did

### thoughts / open qs
- did students actually nootice the time change?? not sure
- is it the time, or do people just not need help right now?? hard to tell from one empty session
- maybe they're using other channels instead of coming in person?? no idea
- don't want to overreact to a single afternoon

### decided
- nothing new. wednesday slot stays as is for now

### Next steps
- [ ] keep showing up for Wed OFHR, see if anyone comes
- [ ] think aobut why turnout is so low -> revisit when organizing notes Sunday
- [ ] use empty time productivly next time instead of just waiting aorund

mildly demoralizing ngl, but ok. one data point

[5] PATL - DSEC Reschedule (Tue 2025-10-07)
**who:** me, Prof. Atlas (quick chat after his office hrs, his office)

## Context
- realized Thursday 10am discussion section cofnlicts w/ my LABM -> can't be in two places obviously
- should've caught this wk 1 tbh.. calendar was a mess
- brought it up w/ PATL, half expected pushback

## What was said / decided
- PATL was chill abt it, no big deal
- he moved my E235 DSEC to Fridays at 2pm
- -> conflict resolved LABM stays untouched
- relief honestly

## Open qs
- will students who picked Thu slot b/c of their own schedules be ok w/ Fri?? 
- room for Fri - same one or new?? didn't ask dumb
- does this mess w/ how autograder stuff gets discussed in section?? prob not but check

## Next steps
- [ ] update Obsidian calendar + Google cal -> Fri 2pm
- [ ] delete old Thu 10am block so I stop double-booking myself
- [ ] double check no other overlaps hiding in rest of week
- [ ] prep section material w/ new day in mind

note to self: check schdule conflicts BEFORE committing to stuff. lesson learned.
```

correct: Yes
faithful: Yes
note: Answer is a bit too wordy but it is correct

---

## G15

**Question:** what bug did RP flag in ECHO, and when did i get it fixed?

**Gold answer:** On Oct 24 (week 4), Ryan reported a critical bug in the EchoSense feature extraction step. You fixed it on Oct 31 (week 5).

**System answer:** RP flagged a critical bug in the ECHO feature extraction step, which was affecting the downstream pipeline and causing garbage outputs [2]. You got it fixed on Friday, October 31, 2025 [1].

**Excerpts the system saw:**

```text
[1] ECHO Feature Extraction Bug Fixed (Fri 2025-10-31)
## context
- RP flagged critical bug in ECHO feature extraction step -> whole downstream pipeline basically garbage until fixed
- been chasing this way too long, ugh

## what I tried
- first guess: input audio loading wrong?? -> checked, looked fine
- then suspected windowing / framing logic -> stepped through w/ debugger, compared intermediate arrays by hand
- printed shapes at every stage b/c something felt off w/ dims
- tried isolating extraction fn on its own w/ tiny dummy clip -> bug reproduced good, at least not falky

## what happened
- found it. finally fixed feature extraction bug in ECHO pipeline
- features now look sane when plotted, no more weird flat/blown-up regions
- honestly kind of embarrassing how small the actual mistake was once found lol
- relief tbh

## next / open qs
- does this change anything we concluded earlier from bad features?? prob need to recheck
- why didn't anything catch this sooner -> need some sanity checks on extraction output??
- tell RP it's fixed + ask him to pull and confirm on his end
- [ ] write down root cause somewhere so I don't repeat it
- [ ] look over rest of pipeline for similar sient issues?? paranoid now

note to self shape asserts are cheap, just add them

[2] ECHO Feature Extraction Bug (Fri 2025-10-24)
## What happened
- Ryan Park pinged re **critical bug** in EchoSense feature extraction step
  - his words: "critical" -> taking seriously, everything downstream depends on features
  - haven't seen exact failure myself yet -> need his repro / logs
- open qs:
  - is it the extraction code itself or upstream audio loding?? 
  - silent bad output vs crash?? silent = way worse means anything tained on these features is suspect
  - when did it get introduced?? check reccent commits

## target change
- deadline got extended -> switched ECHO target **back to the workshop**
  - honestly relief, bug would've been painful otherwise
  - extra time should go to fixing this properly, not hacking around it

## tried so far
- nothing concrete yet on my end, only read RP's report
- skimmed extraction code nothing obvious jumped out -> prob need actual failing input to see it

## next
- [ ] get repro case + logs from RP
- [ ] run extraction on known-good sample, compare outputs
- [ ] diff recent changes to feature extraction step
- [ ] once fixed -> sanity check features before any more training
- [ ] upadte shared task list w/ new workshop target

note to self don't let this eat into coursework time, timebox debugging b/c it can spiral

[3] ECHO First Raspberry Pi Prototype (Thu 2025-11-06)
## what happened
- RP got first ECHO acoustic model prototype running on Raspberry Pi -> actual hardware, not just laptop sim anymore!!
- me: FINALLY fixed feature extraction bug in ECHO pipeline
  - been staring at this way too long, felt good to kill it
  - features coming out of pipeline now look sane (at least by eye)

## tried / noes
- Ryan handled Pi side, I stayed on pipeline side -> split worked ok
- fix landed around same time as deploy -> unclear if Pi build has old or new feature code ??
- need to double check both sides compute features same way, otherwise model sees garbage on device
- haven't really looked at power draw yet ?? whole point of project is low-power so can't ignore

## open qs
- does model behave same on Pi as on laptop ?? no idea yet
- any other silent bugs in preprocessing that I'm missing ??
- how noisy is real room audio vs whatever we tested w/ ??

## next (rough nothing decided)
- [ ] sync w/ Ryan re: which pipeline version is on Pi
- [ ] write down what the bug actually was b/c I will forget
- [ ] sanity check outputs on device before getting excited

feels like real progress for once. don't jinx it

[4] ECHO Repo Published (Wed 2025-11-26)
## what I did
- Sunday -> sat down & drafted intro section of ECHO GitHub README
  - tried to keep it short: what it is, why low-power matters, who it's for (smart home ppl)
  - first pass way too wordy, kept rewriting the opening paragraph
  - ended up w/ something decent?? still not sure tone is right reads kinda like a class report lol

## what happened
- RP published the ECHO repo on the open-source portal
- so it's actually public now -> weird feeeling anyone can see it
- my intro section = first thing ppl will read b/c it's at the top of the README... slightly nervous
- haven't checked yet how it renders on the portal vs GitHub, formatting might be off

## next / open qs
- [ ] reread intro w/ fresh eyes, cut fluff
- [ ] check rendering on portal page
- does intro oversell anything?? don't want claims we can't back up
- ask RP what he thinks of wording
- other README sections still feel thin -> revisit when I have time
- note to self: don't let this eat into coursework, it's a side project

[5] ECHO Got Starred - Next Steps (Tue 2025-12-02)
- RP texted me today -> ECHO got starred by a major tech company!! wild
- context: RP published the ECHO repo on the open-source portal, didn't expect anyone big to notice this fast

## half-formed thoughts
- who exactly starred it?? one engineer browsing or something more deliberate
- README probably needs cleanup now that ppl are actually looking -> setup steps demo audio clips??
- licensing -> did we even pick one properly?? chheck w/ Ryan
- issues/PRs might start coming in -> who triages, me or Ryan??
- worth writing up model/power tradeoffs as short blog post? or too early
- don't let this eat time from coursework + TA sttuff b/c end of quarter

- [ ] ask Ryan what he knows re the star
- [ ] skim repo w/ fresh eyes, note embarrassing bits
```

correct: Yes
faithful: Yes
note:
