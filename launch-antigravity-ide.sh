#!/usr/bin/env bash
# ==============================================================================
#  🚀 Google Antigravity IDE Launcher (v2.5.5)
# ==============================================================================
#  Upotreba:
#    ./launch-antigravity-ide.sh                  # Otvara trenutni folder
#    ./launch-antigravity-ide.sh /putanja/folder  # Otvara navedeni folder/fajl
#    ./launch-antigravity-ide.sh --bg             # Pokreće u pozadini (detachable)
# ==============================================================================

set -euo pipefail

APP_DIR="/home/kizamladjanijebac/Antigravity IDE"
BINARY="$APP_DIR/antigravity-ide"

if [ ! -f "$BINARY" ]; then
    echo "❌ Antigravity IDE izvršni fajl nije pronađen:" >&2
    echo "   $BINARY" >&2
    exit 1
fi

FLAGS=(
    "--no-sandbox"
    "--dangerously-skip-permissions"
)

# Proveri da li je zatraženo pokretanje u pozadini
DETACH=false
ARGS=()

for arg in "$@"; do
    if [ "$arg" == "--bg" ] || [ "$arg" == "-d" ]; then
        DETACH=true
    else
        ARGS+=("$arg")
    fi
done

echo "=================================================="
echo " 🚀 Pokretanje Google Antigravity IDE"
echo " 📁 Lokacija: $APP_DIR"
if [ ${#ARGS[@]} -gt 0 ]; then
    echo " 🎯 Argumenti: ${ARGS[*]}"
else
    echo " 🎯 Radni folder: $PWD"
fi
echo "=================================================="

if [ "$DETACH" = true ]; then
    if [ ${#ARGS[@]} -gt 0 ]; then
        nohup "$BINARY" "${FLAGS[@]}" "${ARGS[@]}" >/dev/null 2>&1 &
    else
        nohup "$BINARY" "${FLAGS[@]}" "$PWD" >/dev/null 2>&1 &
    fi
    echo "✅ Antigravity IDE je uspešno pokrenut u pozadini (PID: $!)."
else
    if [ ${#ARGS[@]} -gt 0 ]; then
        exec "$BINARY" "${FLAGS[@]}" "${ARGS[@]}"
    else
        exec "$BINARY" "${FLAGS[@]}" "$PWD"
    fi
fi
