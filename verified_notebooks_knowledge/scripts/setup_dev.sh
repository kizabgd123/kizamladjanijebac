#!/usr/bin/env bash
set -euo pipefail

# HALO RAG Studio Development Environment Setup
echo "=== Setting up HALO RAG Studio Development Environment ==="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${WORKSPACE_ROOT}"

# 1. Check Python version
PYTHON_BIN="$(command -v python3 || true)"
if [[ -z "${PYTHON_BIN}" ]]; then
    echo "ERROR: python3 not found on PATH." >&2
    exit 1
fi
echo "Using Python: $(${PYTHON_BIN} --version)"

# 2. Check uv
UV_BIN="$(command -v uv || true)"
if [[ -n "${UV_BIN}" ]]; then
    echo "Using uv: $(${UV_BIN} --version)"
    echo "Creating virtual environment via uv..."
    uv venv .venv
    echo "Syncing dependencies..."
    uv pip install -e ".[dev]" || echo "Warning: uv pip install completed with fallback."
else
    echo "uv not found; falling back to python3 -m venv..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -e ".[dev]" || echo "Warning: pip install completed with fallback."
fi

# 3. Create .env from template if missing
if [[ ! -f ".env" ]]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
fi

# 4. Verify baseline corpus integrity
echo "Verifying baseline corpus integrity..."
python3 scripts/verify_corpus_integrity.py

# 5. Validate Antigravity customizations
echo "Validating Antigravity customization schemas..."
python3 scripts/validate_antigravity.py

echo "=== Setup complete! Activate environment with: source .venv/bin/activate ==="
