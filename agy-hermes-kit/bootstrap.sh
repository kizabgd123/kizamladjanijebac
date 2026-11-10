#!/usr/bin/env bash
# ==============================================================================
# Antigravity + Hermes Agent Kit - Master Bootstrap Script
# Instalacija i sinhronizacija celog okruženja iz početka (Linux / WSL2)
# ==============================================================================
set -euo pipefail

KIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECTS_DIR="${PROJECTS_DIR:-$HOME/projects}"

echo "============================================================"
echo "🚀 Pokrećem Antigravity + Hermes Bootstrap Setup..."
echo "📂 Kit lokacija: $KIT_DIR"
echo "============================================================"

# 1. Provera operativnog sistema
OS="$(uname -s)"
if [[ "$OS" != "Linux"* ]]; then
    echo "⚠️  Upozorenje: Preporučeno okruženje je Linux ili Windows WSL2."
fi

# 2. Provera i instalacija osnovnih sistemskih paketa (ako je apt dostupan)
echo "🔍 [1/6] Provera osnovnih alata (git, curl, python3, node)..."
MISSING_PKGS=()
for cmd in git curl python3 node npx; do
    if ! command -v "$cmd" &>/dev/null; then
        MISSING_PKGS+=("$cmd")
    fi
done

if [[ ${#MISSING_PKGS[@]} -gt 0 ]]; then
    echo "⚠️  Nedostaju sledeći alati: ${MISSING_PKGS[*]}"
    if command -v apt-get &>/dev/null && [[ $EUID -eq 0 ]]; then
        echo "📦 Instaliram nedostajuće pakete preko apt-get..."
        apt-get update && apt-get install -y "${MISSING_PKGS[@]}"
    else
        echo "👉 Instalirajte ih ručno pre nastavka: sudo apt install -y ${MISSING_PKGS[*]}"
    fi
else
    echo "✅ Svi osnovni alati su prisutni."
fi

# 3. Python zavisnosti za sync i custom MCP servere (PyYAML, mcp)
echo "🐍 [2/6] Provera Python paketa (pyyaml, mcp)..."
python3 -c "import yaml" 2>/dev/null || {
    echo "📦 Instaliram PyYAML..."
    python3 -m pip install --user pyyaml || pip install pyyaml || true
}
python3 -c "import mcp" 2>/dev/null || {
    echo "📦 Instaliram mcp (FastMCP)..."
    python3 -m pip install --user mcp || pip install mcp || true
}

# 4. Kreiranje ciljnih direktorijuma
echo "📁 [3/6] Kreiranje strukture direktorijuma..."
mkdir -p "$HOME/.agents/skills"
mkdir -p "$HOME/.gemini/antigravity/skills"
mkdir -p "$HOME/.gemini/config"
mkdir -p "$HOME/.hermes/skills"
mkdir -p "$PROJECTS_DIR"

# 5. Sinhronizacija i povezivanje skilova
echo "🔗 [4/6] Sinhronizacija skilova u Antigravity i Hermes..."
if [[ -d "$KIT_DIR/skills" ]]; then
    for skill_path in "$KIT_DIR/skills"/*; do
        if [[ -d "$skill_path" ]]; then
            skill_name="$(basename "$skill_path")"
            # Link u ~/.agents/skills (univerzalni standard)
            ln -sfn "$skill_path" "$HOME/.agents/skills/$skill_name"
            # Link u ~/.gemini/antigravity/skills
            ln -sfn "$skill_path" "$HOME/.gemini/antigravity/skills/$skill_name"
            # Link u ~/.hermes/skills
            ln -sfn "$skill_path" "$HOME/.hermes/skills/$skill_name"
            echo "   • Linkovan skil: $skill_name"
        fi
    done
fi

# 6. Priprema konfiguracionih fajlova i tajni
echo "⚙️  [5/6] Priprema konfiguracije i MCP sinhronizacija..."
if [[ ! -f "$HOME/.hermes/.env" ]]; then
    echo "📄 Kreiram inicijalni $HOME/.hermes/.env iz primera..."
    mkdir -p "$HOME/.hermes"
    cp "$KIT_DIR/configs/hermes.env.example" "$HOME/.hermes/.env"
    chmod 600 "$HOME/.hermes/.env"
fi

# Pokretanje MCP sync skripte (--write režim)
export PROJECTS_DIR
python3 "$KIT_DIR/scripts/sync_mcp.py" --write

# 7. Opciona instalacija samih CLI agenata ako nisu instalirani
echo "🤖 [6/6] Provera instalacije agenata..."
if ! command -v agy &>/dev/null; then
    echo "ℹ️  Antigravity CLI ('agy') nije pronađen u PATH-u."
    echo "   Za instalaciju pokreni: bash $KIT_DIR/scripts/install_antigravity.sh"
else
    echo "✅ Antigravity CLI ('agy') je instaliran: $(agy --version 2>&1 | head -n 1)"
fi

if ! command -v hermes &>/dev/null; then
    echo "ℹ️  Hermes Agent ('hermes') nije pronađen u PATH-u."
    echo "   Za instalaciju pokreni: bash $KIT_DIR/scripts/install_hermes.sh"
else
    echo "✅ Hermes Agent ('hermes') je instaliran."
fi

# Pokretanje verifikacije
echo ""
echo "============================================================"
echo "🩺 Pokrećem verifikaciju stanja..."
echo "============================================================"
bash "$KIT_DIR/scripts/verify.sh" || true

echo ""
echo "============================================================"
echo "🎉 Bootstrap završen uspešno!"
echo "Sledeći koraci:"
echo "1. Popunite API ključeve u ~/.hermes/.env po potrebi"
echo "2. Pokrenite Hermes Agent sa: hermes setup (ili hermes)"
echo "3. Pokrenite Antigravity sa: agy"
echo "============================================================"
