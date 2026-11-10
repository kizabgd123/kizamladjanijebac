#!/usr/bin/env bash
set -euo pipefail
curl -fsSL https://hermes-agent.nousresearch.com/install.sh -o /tmp/hermes_install.sh
echo "Pregledaj /tmp/hermes_install.sh pa pokreni: bash /tmp/hermes_install.sh"
echo "Zatim: source ~/.bashrc && hermes setup && hermes doctor"
