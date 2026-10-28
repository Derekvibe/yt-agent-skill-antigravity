#!/usr/bin/env bash
# Install the yt-* skills for Google Antigravity.
#   ./install.sh               global (all workspaces)  -> ~/.gemini/config/skills
#   ./install.sh --workspace   this project only        -> ./.agents/skills
#   ./install.sh --cli         Antigravity CLI global   -> ~/.gemini/antigravity-cli/skills
# The yt-* folders must stay side by side: yt-chapters and yt-retention import from yt-edit.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
case "${1:-}" in
  --workspace) DEST="$PWD/.agents/skills";             VOICE="$PWD/.agents/youtube" ;;
  --cli)       DEST="$HOME/.gemini/antigravity-cli/skills"; VOICE="$HOME/.gemini/config/youtube" ;;
  "")          DEST="$HOME/.gemini/config/skills";     VOICE="$HOME/.gemini/config/youtube" ;;
  *) echo "usage: $0 [--workspace|--cli]"; exit 1 ;;
esac
mkdir -p "$DEST" "$VOICE"
cp -r "$HERE"/skills/yt-* "$DEST"/
find "$DEST" -name __pycache__ -type d -prune -exec rm -rf {} + 2>/dev/null || true
[ -f "$VOICE/voice.md" ] || cp "$HERE/templates/voice.md" "$VOICE/voice.md"
echo "Installed 11 skills to $DEST"
echo "Fill in your voice profile: $VOICE/voice.md"
