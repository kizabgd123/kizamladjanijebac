#!/usr/bin/env bash
set +e
echo "== Antigravity =="
command -v agy && agy --version
echo "Antigravity skills folder (~/.gemini/antigravity/skills):"
ls -1 "$HOME/.gemini/antigravity/skills" 2>/dev/null | head -10 || echo "(nema)"
echo "== Hermes =="
command -v hermes && hermes doctor 2>&1 | head -40
echo "Hermes skills folder (~/.hermes/skills):"
ls -1 "$HOME/.hermes/skills" 2>/dev/null | head -10 || echo "(nema)"
echo "== Node/npx (za MCP) =="
node --version 2>/dev/null || echo "node nije instaliran"
npx --version 2>/dev/null || echo "npx nije instaliran"
echo "== Config fajlovi =="
ls -l ~/.hermes/config.yaml ~/.hermes/.env ~/.gemini/antigravity/mcp_config.json 2>/dev/null || true

