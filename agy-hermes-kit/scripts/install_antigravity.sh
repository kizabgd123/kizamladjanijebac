#!/usr/bin/env bash
set -euo pipefail
# Skini, pregledaj, pa pokreni (preporuceno umesto direktnog curl | bash)
curl -fsSL https://antigravity.google/cli/install.sh -o /tmp/agy_install.sh
echo "Pregledaj /tmp/agy_install.sh pa pokreni: bash /tmp/agy_install.sh"
echo 'Zatim: export PATH="$HOME/.local/bin:$PATH" && agy --version'
