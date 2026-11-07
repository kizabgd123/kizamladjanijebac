# Reciprocal Relay Report: Agent B extending Agent A

**Relay Agent:** Agent_B_Evaluation  
**Reading:** `research/discoveries/discovery_A.md`  
**Date:** 2026-11-06T23:30:30Z  

## 1. Valuable Empirical Clues Identified in Peer Discovery
- **Vector Search 2.0 Region Lock:** Agent A identified that `us-central1` is currently the only supported region for auto-embeddings in Vector Search 2.0, with other regions returning `501 MethodNotImplemented`.
- **Newline Environment Poisoning:** The revelation that `VECTOR_SEARCH_COLLECTION` breaks silently if an unstripped newline exists explains common customer setup failures.
- **5-10 Minute Indexing Delay:** The auto-indexing lag directly explains intermittent test failures where immediate post-setup queries yield empty arrays (`[]`).

## 2. Complementary Technical Techniques & System Expansions
- **Defensive Healthcheck Polling:**
  Before the agent marks setup complete or opens the browser at `http://localhost:8765`, `setup.py` should execute an active probe loop (polling `search('test')` until a non-empty response or healthy index status is returned), preventing premature user query failure.
- **Environment Sanitization Hook:**
  In `config.py` and `bootstrap.sh`, add explicit string sanitization: `export VECTOR_SEARCH_COLLECTION="$(echo "$VECTOR_SEARCH_COLLECTION" | tr -d '[:space:]')"`.

## 3. Translation into Concrete Falsifiable Experiments
- **Experiment Proposal 3 (HYP-003):**
  *Hypothesis:* Implementing an automated indexing readiness probe in `scripts/setup.py` reduces initial query failure rate from 80% to 0% during the first 10 minutes post-provisioning.
- **Experiment Proposal 4 (HYP-004):**
  *Hypothesis:* Sanitizing environment variables against whitespace/newlines at import time in `scripts/config.py` prevents 100% of `MethodNotImplemented: 501` configuration errors.
