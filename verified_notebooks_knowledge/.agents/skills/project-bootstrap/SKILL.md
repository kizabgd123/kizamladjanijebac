---
name: project-bootstrap
description: Bootstrap, initialize, and scaffold HALO RAG Studio workspace environments.
---

# Project Bootstrap Skill

## When to Activate
Activate during initial project setup, environment migration, or workspace scaffolding.

## Required Context
- Target workspace path (`/home/kizamladjanijebac/verified_notebooks_knowledge`)
- Existence of 15 verified notebook source files
- Available Python, uv, and agy binaries

## Execution Steps
1. Run discovery and audit to verify system binaries.
2. Calculate and persist SHA-256 hashes for all 15 source files to `data/corpus_baseline_hashes.sha256`.
3. Scaffold `.agents/`, `src/`, `config/`, `docs/`, and `tests/` directories.
4. Establish `config/halo.yaml` and `pyproject.toml`.
5. Execute initial verification checks.

## Verification & Checks
- Confirm baseline checksums match.
- Validate configuration files parse cleanly.

## Failure Handling
If any existing knowledge file is missing or modified, abort immediately and alert the user.
