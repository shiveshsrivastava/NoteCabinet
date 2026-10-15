---
title: "E235 Final Exam Grading Script"
date: 2025-11-30
tags: ["ta", "autograder"]
---

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

## next
- [ ] ping SK to say thanks + confirm she's happy w/ merged version
- [ ] dry run on some fake submissions before trusting it for real
- [ ] skim comments so future me / anyone else can follow it

- reminder to self: don't touch it again late at night lol
