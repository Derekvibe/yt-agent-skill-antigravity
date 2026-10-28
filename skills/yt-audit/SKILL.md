---
name: yt-audit
description: >-
  Audit a YouTube channel end to end - packaging, consistency, the first
  fifteen seconds, and what to fix first. Use for "audit my channel", "why
  isn't my channel growing", "review my videos", or a pasted channel URL.
---

# yt-audit

An audit that lists twenty problems is a way of avoiding the one that matters. This ends in ONE fix.

## Before you write

1. Read `.agents/youtube/voice.md` in the workspace, or `~/.gemini/config/youtube/voice.md` if that is where it lives, whichever exists. That is the user's voice profile: how they talk
   on camera, the words they never use, who they are talking to, what they will not claim. If it
   does not exist, ask for **three of their own videos**, read or transcribe them, infer the voice,
   and write the file. A script in the wrong voice is worse than no script, because they have to
   read it out loud.
2. Never invent a number, a result or a source. If a figure would strengthen it and you do not have
   one, ask for it or write the line without it. That includes prices, percentages, savings amounts, bank or product names and "studies show" claims. Exception: if voice.md says illustrative estimates are allowed, round example amounts are fine when labelled as examples or estimates ("say, around $200"), but never present a made-up figure as the creator's own result, a real statistic or a sourced fact.

## What to look at, in this order

1. **The last ten titles, as a set.** Read them as a list, the way the channel page shows them. Do
   they promise different things? Run them through `../yt-package/title.py`. A channel where every
   title is the same shape has a format problem, not a title problem.
2. **The thumbnails, at feed size.** Shrink them. What survives? If three of them are unreadable at
   that size, that is the fix and nothing else matters yet.
3. **The first fifteen seconds of the three most recent.** Transcribe them and score with
   `../yt-script/hookscore.py`. This is where most channels lose.
4. **Upload rhythm.** Not frequency - CONSISTENCY. Six videos in one week and then nothing for a
   month is worse than one a fortnight forever.
5. **The retention shape**, if they can export it. `/yt-retention`.

## What to hand back

- The single biggest fix, named, with what to do this week.
- Three things that are already working, so they do not break them. Be specific; "your energy is
  good" is not an observation.
- What NOT to do yet, and why.

Never open an audit with praise you do not mean, and never end one with a list of twenty things.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**

## Save to the video pack

When the result is final, save it so the user gets one file per video instead of only a chat reply.
Show the result in chat as usual, then save the audit and the ONE fix. Save it as the `audit` section.

1. Use the video name `channel`. The pack lives in the `videos` folder at the root of the user's open workspace.
2. Write the section text to a temporary file with your file tool, then run this from this skill's
   folder (use `python` if `python3` is not found):

```bash
python3 ../yt-pack/pack.py add --root "<workspace>/videos" --video channel --section audit --file "<temp file>" --delete-source
```

3. End your reply with the file path the command prints. If the command refuses the folder, ask the
   user for their project folder. Never save inside the skills folder.

