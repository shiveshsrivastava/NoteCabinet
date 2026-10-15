---
title: "KITTI Download Started on GCLU"
date: 2025-11-01
tags: ["gpu-cluster", "data"]
---

## what I tried
- kicked off KITTI dataset download onto GCLU today
- ran it from login session -> hopefully won't die if I disconnect?? need to double check how the session handles that
- didn't bother w/ fancy stuff, just got it going

## what happened
- download started, seems to be moving
- no errors so far (knock on wood)
- progress output kind of hard to read, not sure if it's actually fast or just looks fast
- ?? is my storage quota on GCLU even big enough for all of it. probably should've checked first lol
- ?? which dir is it even writing to, scratch or home. pretty sure I picked rght but not 100%

## next
- [ ] check back on download make sure it didn't stall overnight
- [ ] verify files actually landed + nothing corrupted
- [ ] look at folder structure once it's done -> figure out what's actually in there beofre witing any loader code
- [ ] remember to not leave random junk files in shared space

## misc
- annoying that big downloads always take forever, nothing to do but wait
- reminder to self: write down exact commands used somewhere so I don't have to rediscover them next time
- feels good to finally have this moving tho
