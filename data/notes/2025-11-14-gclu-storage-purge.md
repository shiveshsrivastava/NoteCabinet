---
title: "GCLU Overnight Storage Purge"
date: 2025-11-14
tags: ["gpu-cluster"]
---

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
