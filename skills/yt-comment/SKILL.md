---
name: yt-comment
description: >-
  Draft replies to YouTube comments in the creator's voice, triaged by which
  ones are worth answering. Use for "reply to my comments", "handle the
  comment section", "someone asked X", or a pasted comment thread.
---

# yt-comment

The comment section is a retention surface, not a chore. Replies in the first few hours are what
decide whether a thread becomes a conversation other people read.

## Before you write

1. Read `.agents/youtube/voice.md` in the workspace, or `~/.gemini/config/youtube/voice.md` if that is where it lives, whichever exists. That is the user's voice profile: how they talk
   on camera, the words they never use, who they are talking to, what they will not claim. If it
   does not exist, ask for **three of their own videos**, read or transcribe them, infer the voice,
   and write the file. A script in the wrong voice is worse than no script, because they have to
   read it out loud.
2. Never invent a number, a result or a source. If a figure would strengthen it and you do not have
   one, ask for it or write the line without it. That includes prices, percentages, savings amounts, bank or product names and "studies show" claims. Exception: if voice.md says illustrative estimates are allowed, round example amounts are fine when labelled as examples or estimates ("say, around $200"), but never present a made-up figure as the creator's own result, a real statistic or a sourced fact.

## Triage first, always

Sort what the user pastes into four piles and say how many are in each before writing anything:

1. **Questions** - answer them. These are your next video's topics, so note the repeats.
2. **Corrections** - if they are right, say so plainly and thank them. Never argue a fact you
   cannot check.
3. **Praise** - reply to a few, briefly, with something specific from their comment. A wall of
   identical "thank you!" replies reads as automated because it is.
4. **Bait** - do not reply. Say so and move on. Never write a comeback, however deserved.

## Writing the reply

- Under 30 words. A long reply in a comment thread is a blog post nobody asked for.
- Answer the actual question in the first sentence.
- One question back, only when it is real.
- No emoji unless the user's own replies use them. Check their voice file.
- Never promise a video you have not agreed to make.

## The heart and the pin

Say which ONE comment to pin and why. Pin the question the most people also have, not the nicest
one. Heart generously - it costs nothing and it is visible.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**

## Save to the video pack

When the result is final, save it so the user gets one file per video instead of only a chat reply.
Show the result in chat as usual, then save the triage and the drafted replies. Save it as the `comments` section.

1. Use the video's name (reuse the name already used in this conversation, otherwise the working title). The pack lives in the `videos` folder at the root of the user's open workspace.
2. Write the section text to a temporary file with your file tool, then run this from this skill's
   folder (use `python` if `python3` is not found):

```bash
python3 ../yt-pack/pack.py add --root "<workspace>/videos" --video "<video name>" --section comments --file "<temp file>" --delete-source
```

3. End your reply with the file path the command prints. If the command refuses the folder, ask the
   user for their project folder. Never save inside the skills folder.

