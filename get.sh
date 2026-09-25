#!/bin/bash
# One-line installer:
#   curl -fsSL https://raw.githubusercontent.com/mailtoharutyunyan/KDWin-Keyboards/main/get.sh | bash
# Downloads the latest version from GitHub and runs install.sh. Run it again
# after logging out and back in to turn the keyboards on.
set -euo pipefail

REPO="mailtoharutyunyan/KDWin-Keyboards"
BRANCH="main"
DIR="$HOME/Library/Application Support/KDWin-Keyboards"

echo "Downloading KDWin Keyboards from github.com/$REPO..."
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
curl -fsSL "https://github.com/$REPO/archive/refs/heads/$BRANCH.tar.gz" | tar -xz -C "$TMP"

rm -rf "$DIR"
mkdir -p "$(dirname "$DIR")"
mv "$TMP"/*/ "$DIR"

"$DIR/install.sh"
