---
name: yt-pack
description: Keeps one living Markdown file per video (a video pack) so a script, hooks, title, thumbnail, SEO, chapters and edit list end up in one place instead of scattered through chat. Use when the user asks to save, compile, show or list their video files, or when another yt-* skill has finished a result that should be saved.
---

# yt-pack

One file per video. Every yt-* skill saves its finished result into the same pack, so the user ends
up with a single document per video that they can open, edit and keep. The chat is the working
space. The pack is the product.

## How it works

Packs live in a `videos` folder in the user's own project (the workspace root), never in the skills
folder:

```
<workspace>/videos/
  index.md                         every video, which sections it has, when it changed
  i-tracked-every-naira/
    video-pack.md                  idea, hooks, script, package, seo, chapters, edit list...
```

A section is replaced when the same skill runs again, new sections slot into a fixed order, and
anything the user wrote outside the marked blocks is left alone.

## Commands

Run from this skill's folder (or use the full path). If `python3` is not found (common on
Windows), use `python`. Always pass the workspace `videos` folder as `--root`.

```bash
python3 pack.py add --root "<workspace>/videos" --video "Video name" --section script --file notes.md --delete-source
python3 pack.py show --root "<workspace>/videos" --video "Video name"
python3 pack.py list --root "<workspace>/videos"
```

Sections: `idea` `hooks` `script` `package` `seo` `chapters` `edit` `shorts` `retention`
`comments` `viral` `plan` `audit` `notes`.

## Rules

1. One video, one name. If the video already has a name in this conversation, reuse that exact name
   so every skill writes to the same pack. If it has none, use the working title.
2. Channel-level work (`yt-audit`, `yt-plan`, `yt-viral`) uses the video name `channel`.
3. Write the finished section to a temporary text file with your file tool, then pass it with
   `--file ... --delete-source`. Do not paste long text into the command line.
4. Save only finished work, and save exactly what the user was shown. Do not add claims, numbers or
   sources that were not in the result.
5. After saving, tell the user the file path the command printed.
6. If the user asks "show my pack", "what have we got for this video" or similar, run `show`.
7. Never write into the skills folder or `.gemini`. The command refuses, so if it does, ask for the
   project folder.
