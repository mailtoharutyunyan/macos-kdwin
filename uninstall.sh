#!/bin/bash
# Turns off and removes the KDWin keyboards.
set -euo pipefail
cd "$(dirname "$0")"

command -v swift >/dev/null && swift tools/keyboards.swift disable 2>/dev/null || true
rm -f "$HOME/Library/Keyboard Layouts/"{"Armenian KDWin","Russian KDWin"}.{keylayout,icns}
echo "Removed. Log out and back in if they still show in the menu bar."
