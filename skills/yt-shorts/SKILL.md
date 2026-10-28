---
name: yt-shorts
description: >-
  Find the Shorts hiding inside a long video and write them, using the
  transcript to pick self-contained moments. Use for "cut this into shorts",
  "clip this", "repurpose this video", "what should I clip".
---

# yt-shorts

A Short cut out of a long video is not a clip of the best moment. It is a moment that **survives
without the video around it**, which is a much smaller set.

## Picking

Read the transcript and find spans of 20-55 seconds where all three are true:

1. It opens on a complete thought. If the first sentence needs the previous minute, it is not a Short.
2. There is a turn in it - a claim, then something that complicates or proves it.
3. It ends on a line, not a trail-off.

Rank the candidates and show the user the top five with their timecodes and first line, so they can
reject one without reading the whole transcript.

## Writing each one

- **A NEW first line.** The long video's line assumes context this viewer does not have. Write the
  replacement and run it through `../yt-script/hookscore.py`.
- **On-screen text for the first two seconds**, different words from the spoken line.
- **A loop point**: what the last line sets up so the first line answers it.
- Vertical framing note - what gets cropped out of a 16:9 frame and whether that matters.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**

## Save to the video pack

When the result is final, save it so the user gets one file per video instead of only a chat reply.
Show the result in chat as usual, then save the Short candidates with timecodes and their new first lines. Save it as the `shorts` section.

1. Use the video's name (reuse the name already used in this conversation, otherwise the working title). The pack lives in the `videos` folder at the root of the user's open workspace.
2. Write the section text to a temporary file with your file tool, then run this from this skill's
   folder (use `python` if `python3` is not found):

```bash
python3 ../yt-pack/pack.py add --root "<workspace>/videos" --video "<video name>" --section shorts --file "<temp file>" --delete-source
```

3. End your reply with the file path the command prints. If the command refuses the folder, ask the
   user for their project folder. Never save inside the skills folder.

