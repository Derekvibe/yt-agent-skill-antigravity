# YouTube Agent Skills for Google Antigravity
 
[![test](https://github.com/Derekvibe/yt-agent-skill-antigravity/actions/workflows/test.yml/badge.svg)](https://github.com/Derekvibe/yt-agent-skill-antigravity/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
 
Eleven skills that help you run a YouTube channel, packaged for [Google Antigravity](https://antigravity.google).
Free, MIT licensed, no signup, no API key, nothing to connect.
 
One skill writes your script from 21 hook formulas and scores the hook before you film a take.
One lints the title and thumbnail as a single pairing. One reads your retention export and tells you
where people left. One turns a transcript into an edit decision list. One finds the Shorts hiding
inside a long video. One ranks what is working in your niche by how far each video beat its own
channel's median.
 
**Nothing gets published for you.** These skills write and analyse. You upload.
 
> **Ported and maintained by [Derek (@Derekvibe)](https://github.com/Derekvibe).**
> This is an Antigravity port of
> [Jakeschincariol/youtube-agent-skill](https://github.com/Jakeschincariol/youtube-agent-skill) by
> Jake Schincariol (MIT). The skills and the six Python tools are his. This repo changes the install
> locations, the `voice.md` path and the docs, adds Windows-safe text handling, tests and CI.
> Not affiliated with Google or the original author.
 
## Quick start
 
You need Antigravity and Python 3.6+ (3.9+ recommended).
 
```bash
git clone https://github.com/Derekvibe/yt-agent-skill-antigravity.git
cd yt-agent-skill-antigravity
```
 
**Windows (PowerShell)**
 
```powershell
.\install.ps1
```
 
If Windows blocks the script, run it for this one time with
`powershell -ExecutionPolicy Bypass -File .\install.ps1`.
 
**macOS / Linux**
 
```bash
./install.sh
```
 
Then restart Antigravity and ask for something in plain words:
 
> Write me a script for a YouTube video about how I built an app in 7 days.
 
Antigravity chooses skills by reading their descriptions, so you describe the job rather than typing
a slash command. Naming the skill ("use yt-script") works too.
 
## Where the skills go
 
Antigravity skills are folders containing a `SKILL.md`. The installer copies the `yt-*` folders to:
 
| Scope | Location | Installer flag |
| --- | --- | --- |
| Everywhere (IDE) | `~/.gemini/config/skills/` | none (default) |
| This project only | `<workspace>/.agents/skills/` | `--workspace` / `-Workspace` |
| Antigravity CLI | `~/.gemini/antigravity-cli/skills/` | `--cli` (bash only) |
 
Keep all eleven `yt-*` folders side by side. `yt-chapters` and `yt-retention` import from `yt-edit`,
and `yt-viral` reads the hook list in `yt-script`.
 
## Your voice file
 
Six of the skills read a voice profile so the output sounds like you. The installer creates it from
[`templates/voice.md`](templates/voice.md):
 
- everywhere: `~/.gemini/config/youtube/voice.md`
- one project: `<workspace>/.agents/youtube/voice.md`
Fill it in, or paste three of your own transcripts into the agent chat and say
"write my voice.md from these".
 
## The eleven skills
 
| Skill | What it does | Try saying |
| --- | --- | --- |
| `yt-script` | One idea into a script. Five hooks from [21 formulas](skills/yt-script/hooks.json), scored, then the spoken script with retention beats marked. | "Write a script about X" |
| `yt-package` | Title and thumbnail as one pairing, linted for truncation, duplication and vagueness. | "Check this title and thumbnail text" |
| `yt-edit` | A transcript into an edit decision list: dead air, filler cues, retakes, with timecodes. | "Find the dead air in this transcript" |
| `yt-comment` | The comment section triaged into four piles, then replies in your voice. | "Triage these comments" |
| `yt-plan` | A week of content that fits the hours you actually have. | "Plan my week, I have 6 hours" |
| `yt-viral` | What is working in your niche, ranked by multiple over each channel's own median. | "What is outperforming in my niche?" |
| `yt-retention` | Your retention export read properly: hook leak, cliffs, slide, and what to change. | "Read this retention CSV" |
| `yt-shorts` | The Shorts already inside a long video, with a new first line for each. | "Find Shorts in this transcript" |
| `yt-seo` | Description, tags worth having, and the three queries this should win. | "Write the description and tags" |
| `yt-chapters` | Chapters from a transcript, validated against YouTube's own rules. | "Make chapters from this transcript" |
| `yt-audit` | The whole channel, ending in ONE fix. | "Audit my channel" |
 
## The six tools
 
Plain Python, standard library only. The agent runs them for you, and you can run them yourself
from the repo folder (use `python` instead of `python3` on Windows):
 
```bash
python3 skills/yt-script/hookscore.py --hook "one line"
python3 skills/yt-package/title.py --title "..." --thumb "..."
python3 skills/yt-edit/deadair.py transcript.srt
python3 skills/yt-chapters/chapters.py transcript.srt
python3 skills/yt-retention/retention.py retention.csv
python3 skills/yt-viral/swipe.py collected.json --min 2.0
```
 
Transcripts can be SRT, VTT or Whisper JSON. Accented text and files with a BOM are handled.
 
## Troubleshooting
 
| Problem | Fix |
| --- | --- |
| The agent ignores the skills | Restart Antigravity fully. Check the `yt-*` folders are in one of the locations above, each with a `SKILL.md`. Try naming the skill: "use yt-script". |
| `python3` not found | Use `python` (Windows) or install Python from python.org and tick "Add Python to PATH". |
| PowerShell says scripts are disabled | `powershell -ExecutionPolicy Bypass -File .\install.ps1` |
| The agent cannot run the tools | Check Antigravity's terminal command policy allows the agent to run commands. |
| A skill says the voice file is missing | Run the installer again, or create `voice.md` in one of the two locations above. |
 
## Status and testing
 
```bash
python tests/smoke_test.py
```
 
13 checks cover skill frontmatter, all six tools, SRT / VTT / Whisper input, accented text under a
non-UTF-8 locale, bad-input exit codes, and the cross-skill imports from an installed layout.
GitHub Actions runs them on Linux, Windows and macOS. `pyflakes` is clean.
 
Checked by hand: the tests on Windows with Python 3.13, `install.ps1` on Windows, `install.sh` on Linux.
Skill discovery inside Antigravity depends on your Antigravity version. If it does not work for you,
please [open an issue](https://github.com/Derekvibe/yt-agent-skill-antigravity/issues) with your
Antigravity version and what the agent said.
 
## Changes from upstream
 
- Antigravity install paths, `voice.md` location, installers (PowerShell and bash), docs.
- Tools read and write UTF-8 explicitly, so accented titles and transcripts no longer crash on
  Windows or non-UTF-8 consoles.
- `hookscore.py` exits non-zero on a bad path or a bare `--hook`.
- `SKILL.md` files say where to run the tools from.
- Lint clean, tests and CI added.
## The fine print
 
- **It does not publish.** Every skill ends in a block you copy.
- **`hookscore.py` is a heuristic, not a predictor.** Low score: look again. High score: not a promise.
- **`yt-viral` reads, it does not scrape.** Public listings only, never your logged-in session.
- **Nothing invents a number.** Missing figure: it asks, or writes the line without it.
## Author and maintainer
 
Antigravity port created and maintained by **Derek** ([@Derekvibe](https://github.com/Derekvibe)).
Questions, bugs and pull requests are welcome through
[GitHub issues](https://github.com/Derekvibe/yt-agent-skill-antigravity/issues).
 
Original skills and Python tools by [Jake Schincariol](https://github.com/Jakeschincariol).
 
## License
 
MIT. Copyright Jake Schincariol (original work) and Derekvibe (Antigravity port); see [LICENSE](LICENSE).
 