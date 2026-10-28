---
name: yt-chapters
description: >-
  Write YouTube chapters from a transcript, validated against YouTube's own
  rules so they actually render. Use for "add chapters", "timestamps",
  "break this video into sections".
---

# yt-chapters

Run these from this skill's own folder (the one containing this SKILL.md). If `python3` is not found (common on Windows), use `python`.

```bash
python3 chapters.py transcript.srt --target 8
```

## The rules, which are not optional

A chapter list that breaks any of these silently does not become chapters at all - the block just
sits in the description doing nothing:

- The first entry must be **00:00**.
- There must be **at least three**.
- Each must be **at least 10 seconds** long.

The tool checks all three and tells you when a list is invalid rather than letting you paste it.

## Retitle every line

`chapters.py` finds the BOUNDARIES well - it scores the pauses you actually took by how much the
vocabulary shifts across them. The titles it emits are the topic words, and they are a draft. A
chapter called "Thumbnails Titles Packaging" is a placeholder. Rewrite each one as the promise of
that section, in the user's voice, three to five words.

Chapters are also a retention diagnostic: if a section cannot be named in five words, it is two
sections or it is filler.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**

## Save to the video pack

When the result is final, save it so the user gets one file per video instead of only a chat reply.
Show the result in chat as usual, then save the final chapter list, ready to paste. Save it as the `chapters` section.

1. Use the video's name (reuse the name already used in this conversation, otherwise the working title). The pack lives in the `videos` folder at the root of the user's open workspace.
2. Write the section text to a temporary file with your file tool, then run this from this skill's
   folder (use `python` if `python3` is not found):

```bash
python3 ../yt-pack/pack.py add --root "<workspace>/videos" --video "<video name>" --section chapters --file "<temp file>" --delete-source
```

3. End your reply with the file path the command prints. If the command refuses the folder, ask the
   user for their project folder. Never save inside the skills folder.

