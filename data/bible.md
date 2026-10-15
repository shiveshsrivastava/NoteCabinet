<!--
WORLD BIBLE - the ground truth every note, question and Organize page is generated from.

How to fill this in:
- Text inside these comment markers is stripped before anything is sent to Claude. Delete them when done if you like.
- Background sections (Me, Courses, Projects, TA job, People) are context only. They are NOT asked about.
  Anything you want an eval question to test must be a [F...] fact in the Timeline.
- Every fact: one line, `- [F###] (wkN, YYYY-MM-DD) text.` The date is optional; without it the fact
  starts on the Monday of week N. Make facts concrete: dates, numbers, names, decisions.
- A fact that changes: write a new fact ending in `supersedes F###`. Aim for 5+ of these (SPEC: >= 3).
- Facts may use glossary abbreviations (e.g. "R", "p2"); the scripts expand them where needed.
- Glossary meanings are written into notes EXACTLY as you type them here, so use the form you'd
  actually write in full ("Prof. Ramirez", not "my advisor Professor Ramirez").
- Target: ~80-150 facts across wk1-wk10, >= 15 glossary entries.
- The example lines below are real, parseable entries. Keep, edit or replace them.
- Check your work any time:  uv run python -c "import sys; sys.path.insert(0,'scripts'); import common; b=common.load_bible(); print(len(b.facts), 'facts,', len(b.glossary), 'glossary')"
-->

Quarter start: 2025-09-29

## Me
I am Shivesh, a first-year master's student in Electrical and Computer Engineering at the University of Washington. I study computer vision, Agentic AI, and edge deployment. I take notes by dumping bullet points into an Obsidian vault during the day. Every Sunday night, I organize those notes into clear task lists.

## Courses
- EE P 596 C Foundations of Applied Deep Learning: Mondays 6:30 PM - 9:50 PM, graded via four problem sets and a midterm exam.
- EE P 500 D Agentic AI: Tuesdays 4:30 PM - 6:20 PM, graded via a final research paper and weekly reading reflections.
- EE P 596 A Computer Vision: Thursdays 6:30 PM - 9:50 PM, graded via biweekly coding assignments and a final project.

## Projects
- AutoNav: Training lightweight perception models for drone navigation, supervised by Prof. Fox.
- EchoSense: A side project building a low-power acoustic anomaly detection system for smart homes, done with my classmate Ryan Park.

## TA job
I am a teaching assistant for EE 235 Continuous Time Linear Systems, instructed by Prof. Atlas. My duties include leading a weekly discussion section, holding office hours, and writing autograding scripts with my co-TA Sarah Kim.

## People
- Prof. Fox: My advisor for the AutoNav project.
- Ryan Park: A fellow student and my collaborator on EchoSense.
- Prof. Atlas: The primary instructor for the EE 235 course I am TAing.
- Sarah Kim: A fellow grad student serving as the other TA for EE 235.
- Liam Ortiz: A classmate and my designated project partner for EE P 596 A.
- Prof. Seitz: The primary instructor for my EE P 596 A computer vision course.
- Prof. Lindqvist: The primary instructor for my EE P 596 C deep learning course.
- Chloe Nguyen: My close friend who I regularly coordinate daily tasks and study sessions with.
- Marcus Webb: A senior labmate who helps me navigate the university computing resources.

## Timeline

### Week 1
- [F001] (wk1, 2025-09-29) I attended the first E596C lecture on backpropagation fundamentals.
- [F002] (wk1, 2025-09-30) PFOX scheduled our weekly 1ON1 for Wednesdays at 2pm.
- [F003] (wk1) I requested access to GCLU for the E596C programming assignments.
- [F004] (wk1, 2025-10-01) PATL assigned me to teach the E235 DSEC on Thursdays at 10am.
- [F005] (wk1, 2025-10-02) RP and I decided to submit ECHO to a smart home workshop.
- [F006] (wk1) I configured my local environment for the ANAV perception module.
- [F007] (wk1, 2025-10-03) My E235 OFHR are officially set for Fridays at 3pm.
- [F008] (wk1) CN and I agreed to get coffee every Friday morning this quarter.
- [F009] (wk1, 2025-10-04) LO agreed to be my partner for the E596A final project.
- [F010] (wk1) PLIN announced the E596C MIDT will take place during week 5.
- [F011] (wk1, 2025-10-05) I bought the required textbook for the E500D course.

### Week 2
- [F012] (wk2, 2025-10-06) I realized the Thursday 10am DSEC conflicts with my LABM.
- [F013] (wk2, 2025-10-07) PATL moved my E235 DSEC to Fridays at 2pm. supersedes F004
- [F014] (wk2) MW helped me resolve a tricky library path issue on GCLU.
- [F015] (wk2, 2025-10-08) SK asked me to grade the first batch of E235 submissions.
- [F016] (wk2, 2025-10-09) We held the first LABM to discuss repository architecture for ANAV.
- [F017] (wk2) I finished the first set of E596C HWKS on gradient descent.
- [F018] (wk2, 2025-10-10) RP shared the initial data collection script for ECHO.
- [F019] (wk2) CN canceled our Friday coffee because she caught a cold.
- [F020] (wk2, 2025-10-11) I spent Saturday morning reviewing robotic coordinate transformations.
- [F021] (wk2) Only three students showed up to my Friday OFHR.

### Week 3
- [F022] (wk3, 2025-10-13) PATL moved my E235 DSEC to Wednesdays at 4pm permanently. supersedes F013
- [F102] (wk3, 2025-10-13) I moved my E235 OFHR to Wednesdays at 3pm because Friday attendance was so low. supersedes F007
- [F023] (wk3) PSTE released the first major coding assignment for E596A.
- [F024] (wk3, 2025-10-14) I completed the grading for the E235 homework batch.
- [F025] (wk3, 2025-10-15) My E235 OFHR were completely empty this afternoon.
- [F026] (wk3, 2025-10-16) LO suggested we build a real-time object tracker for E596A.
- [F027] (wk3) I successfully integrated the new sensor suite into the ANAV simulation.
- [F028] (wk3, 2025-10-17) RP and I decided to target an open-source release instead for ECHO. supersedes F005
- [F029] (wk3) I met CN for our weekly coffee at the library cafe.
- [F030] (wk3, 2025-10-18) I started writing the first E500D reading reflection.
- [F031] (wk3) GCLU was offline for four hours for scheduled network maintenance.

### Week 4
- [F032] (wk4, 2025-10-20) PFOX told me to switch the ANAV backend from Python to C++.
- [F033] (wk4) LO and I submitted our E596A project proposal on multi-object tracking.
- [F034] (wk4, 2025-10-22) I led a review session for E235 Laplace transforms during DSEC.
- [F035] (wk4, 2025-10-22) SK covered my E235 OFHR because I had a dentist appointment.
- [F036] (wk4, 2025-10-23) I finished porting the core ANAV logic to C++.
- [F037] (wk4) PSTE extended the E596A assignment deadline by exactly two days.
- [F038] (wk4, 2025-10-24) RP reported a critical bug in the ECHO feature extraction step.
- [F039] (wk4) MW showed me how to profile PyTorch code efficiently on GCLU.
- [F040] (wk4, 2025-10-25) I studied all day Saturday for the upcoming E596C MIDT.
- [F041] (wk4) We changed our ECHO target back to the workshop since the deadline was extended. supersedes F028

### Week 5
- [F042] (wk5, 2025-10-27) PLIN announced the E596C MIDT is delayed to week 7. supersedes F010
- [F043] (wk5) LO and I realized our E596A tracker had a major occlusion flaw.
- [F044] (wk5, 2025-10-29) I held a massive E235 OFHR session to help students with Fourier series.
- [F045] (wk5, 2025-10-29) PFOX canceled our 1ON1 this week due to a grant deadline.
- [F046] (wk5, 2025-10-30) We held a LABM to discuss on-device model optimization techniques.
- [F047] (wk5) CN and I went out for dinner to celebrate surviving week 5.
- [F048] (wk5, 2025-10-31) I finally fixed the feature extraction bug in the ECHO pipeline.
- [F049] (wk5) SK sent me her half of the E235 automated grading script.
- [F050] (wk5, 2025-11-01) I started downloading the KITTI dataset onto GCLU.
- [F051] (wk5) I got the C++ backend for ANAV to compile without warnings.

### Week 6
- [F052] (wk6, 2025-11-03) I completed the second set of E596C HWKS on CNNs.
- [F053] (wk6) PATL asked me to write one difficult question for the E235 final exam.
- [F054] (wk6, 2025-11-05) I had a great 1ON1 with PFOX about scalable Edge AI architecture.
- [F055] (wk6, 2025-11-05) The KITTI dataset download finally finished on GCLU.
- [F056] (wk6, 2025-11-06) RP deployed the first ECHO acoustic model prototype on a Raspberry Pi.
- [F057] (wk6) LO fixed the occlusion bug in our E596A tracking code.
- [F058] (wk6, 2025-11-05) My DSEC was packed with students asking about Bode plots.
- [F059] (wk6) PLIN announced the E596C MIDT was delayed again to week 8. supersedes F042
- [F060] (wk6, 2025-11-08) MW warned the lab that GCLU storage is almost completely full.
- [F061] (wk6) I started preparing my review notes for the delayed E596C MIDT.

### Week 7
- [F062] (wk7, 2025-11-10) I submitted the third E500D reading reflection online.
- [F063] (wk7) We decided to switch the ANAV backend back to Python for faster iteration. supersedes F032
- [F064] (wk7, 2025-11-11) PFOX was impressed with the simulation demo for ANAV.
- [F065] (wk7, 2025-11-12) I submitted my proposed E235 exam question to PATL.
- [F066] (wk7, 2025-11-13) RP and I started writing the system architecture document for ECHO.
- [F067] (wk7) LO and I tested the E596A tracking algorithm on real street footage.
- [F068] (wk7, 2025-11-12) I skipped DSEC today because SK offered to cover it for me.
- [F069] (wk7) I spent the afternoon finalizing the Python interface for ANAV.
- [F070] (wk7, 2025-11-15) CN helped me review my reading reflections for E500D.
- [F071] (wk7) GCLU administrators purged old data overnight to free up storage space.

### Week 8
- [F072] (wk8, 2025-11-17) I finally took the E596C MIDT during the Monday evening class session.
- [F073] (wk8) PSTE announced the final project presentation schedule for E596A.
- [F074] (wk8, 2025-11-18) I decided to do a E500D paper on LLM tool use.
- [F075] (wk8, 2025-11-19) I held E235 OFHR but only one student attended.
- [F076] (wk8, 2025-11-20) RP generated the final latency benchmarks for ECHO.
- [F077] (wk8) PFOX asked me to prepare a poster detailing the ANAV project architecture.
- [F078] (wk8, 2025-11-21) LO and I finished all the code for our E596A project.
- [F079] (wk8) We held a LABM to practice upcoming poster presentations.
- [F080] (wk8, 2025-11-22) PATL approved my E235 final exam question with minor edits.
- [F081] (wk8) I spent Sunday drafting the ECHO GitHub README introduction section.

### Week 9
- [F082] (wk9, 2025-11-24) Classes were canceled for the entire week of Thanksgiving.
- [F083] (wk9) I decided to switch my E500D paper topic to multi-agent reinforcement learning. supersedes F074
- [F084] (wk9, 2025-11-25) I merged my Python changes into the main ANAV branch.
- [F085] (wk9, 2025-11-26) RP published the ECHO repository on the open-source portal.
- [F086] (wk9, 2025-11-27) I had Thanksgiving dinner at a local restaurant with CN.
- [F087] (wk9) LO sent me the first draft of our E596A project report.
- [F088] (wk9, 2025-11-28) I worked on compiling the E500D references over the holiday break.
- [F089] (wk9, 2025-11-29) I designed the ANAV poster layout in Illustrator.
- [F090] (wk9) MW asked me to review his latest PyTorch PR for the lab repository.
- [F091] (wk9, 2025-11-30) I finalized the E235 grading script for the final exams.

### Week 10
- [F092] (wk10, 2025-12-01) I printed the ANAV poster at the university library.
- [F093] (wk10, 2025-12-04) LO and I presented our E596A project in class.
- [F094] (wk10) I held my final E235 OFHR and the room was completely full.
- [F095] (wk10, 2025-12-03) I submitted the E500D final research paper online.
- [F096] (wk10, 2025-12-04) PFOX and I presented the ANAV poster at the department showcase.
- [F097] (wk10) RP texted me that ECHO got starred by a major tech company.
- [F098] (wk10, 2025-12-05) I proctored the E235 final exam alongside SK and PATL.
- [F099] (wk10) CN and I grabbed celebratory coffee to mark the end of classes.
- [F100] (wk10, 2025-12-06) I finished grading my assigned stack of E235 final exams.
- [F101] (wk10, 2025-12-07) I pushed all my final quarter notes to my backup drive.

## Glossary

| id  | abbrev | meaning               |
|-----|--------|-----------------------|
| G01 | PFOX   | Prof. Fox             |
| G02 | RP     | Ryan Park             |
| G03 | PATL   | Prof. Atlas           |
| G04 | CN     | Chloe Nguyen          |
| G05 | SK     | Sarah Kim             |
| G06 | LO     | Liam Ortiz            |
| G07 | PSTE   | Prof. Seitz           |
| G08 | MW     | Marcus Webb           |
| G09 | ANAV   | AutoNav               |
| G10 | ECHO   | EchoSense             |
| G11 | E596A  | EE P 596 A            |
| G12 | E596C  | EE P 596 C            |
| G13 | E500D  | EE P 500 D            |
| G14 | E235   | EE 235                |
| G15 | OFHR   | office hours          |
| G16 | 1ON1   | 1:1 meeting           |
| G17 | HWKS   | problem sets          |
| G18 | MIDT   | midterm exam          |
| G19 | GCLU   | the GPU cluster       |
| G20 | DSEC   | discussion section    |
| G21 | LABM   | lab meeting           |
| G22 | PLIN   | Prof. Lindqvist       |