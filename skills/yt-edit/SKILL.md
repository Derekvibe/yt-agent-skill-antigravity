---
name: yt-edit
description: >-
  Turn a raw recording's transcript into an edit decision list - dead air,
  filler cues and retakes, with timecodes. Use for "edit this", "cut the
  dead space", "tighten this video", "I rambled", or any request to shorten
  footage from a transcript.
---

# yt-edit

An edit decision list from a timestamped transcript. It prints the cuts. You apply them.

Run these from this skill's own folder (the one containing this SKILL.md). If `python3` is not found (common on Windows), use `python`.

```bash
python3 deadair.py transcript.srt              # srt, vtt or whisper json
python3 deadair.py transcript.srt --floor 0.35 --json
```

No transcript yet? Ask for one, or produce one first - `whisper`, `faster-whisper`, or the caption
track YouTube generates on an unlisted upload all work. Do not guess at timings.

## What it finds

- **DEAD** - gaps longer than the floor, trimmed from the MIDDLE so both sides keep a breath.
  Cutting flush against speech is what makes a tightened take sound gasping.
- **FILLER** - cues that are nothing but "um", "so yeah", "basically".
- **REPEAT** - a sentence restarted. Compared against the last cue that was actually speech, not
  the literal previous cue, because most retakes have an "um" between the two attempts.

## What it will not do

It does not touch media. It has no opinion about your B-roll. A 40% cut on the report is a 40% cut
of SPEECH, and if the video has a long silent demo in it that number is wrong - check the report
against the footage before you trust the runtime at the bottom.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**

## Save to the video pack

When the result is final, save it so the user gets one file per video instead of only a chat reply.
Show the result in chat as usual, then save the edit decision list with timecodes. Save it as the `edit` section.

1. Use the video's name (reuse the name already used in this conversation, otherwise the working title). The pack lives in the `videos` folder at the root of the user's open workspace.
2. Write the section text to a temporary file with your file tool, then run this from this skill's
   folder (use `python` if `python3` is not found):

```bash
python3 ../yt-pack/pack.py add --root "<workspace>/videos" --video "<video name>" --section edit --file "<temp file>" --delete-source
```

3. End your reply with the file path the command prints. If the command refuses the folder, ask the
   user for their project folder. Never save inside the skills folder.

