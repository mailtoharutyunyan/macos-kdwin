#!/bin/bash
# Installs the KDWin Armenian and Russian keyboards for the current user.
# Safe to run again: the second run (after logging out and in) turns them on.
set -euo pipefail
cd "$(dirname "$0")"

DEST="$HOME/Library/Keyboard Layouts"
mkdir -p "$DEST"
cp layouts/*.keylayout layouts/*.icns "$DEST/"
echo "Copied keyboards to $DEST"

if ! command -v swift >/dev/null; then
    echo
    echo "Swift is not available, so turn the keyboards on by hand:"
    echo "  log out and back in, then System Settings → Keyboard → Input Sources → Edit → +"
    echo "  and add 'Armenian KDWin' and 'Russian KDWin'."
    exit 0
fi

if swift tools/keyboards.swift enable 2>/dev/null; then
    echo
    echo "Done. Switch keyboards with Ctrl+Space or the flag in the menu bar."
else
    echo
    echo "macOS loads new keyboards at login. Log out, log back in, then run ./install.sh again."
fi
