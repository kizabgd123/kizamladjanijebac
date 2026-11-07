# Research Sources & Ingested Literature

**Campaign:** Autonomous Investigation of `retail-product-search`  
**Ingestion Date:** 2026-11-06T23:28:00Z  

## 1. Primary Skill Artifacts Ingested
- `README.md` (`/home/kizamladjanijebac/Desktop/discord-openclaw/.agents/skills/retail-product-search/README.md`)
  - Installation pathways, surfacing personas, Q-MODE triggers, sample queries, failure modes.
- `SKILL.md` (`/home/kizamladjanijebac/Desktop/discord-openclaw/.agents/skills/retail-product-search/SKILL.md`)
  - Agent instructions, Q-MODE state machine, bootstrap sequencing, environment variables, MCP migration map.
- `EVAL.yaml` (`/home/kizamladjanijebac/Desktop/discord-openclaw/.agents/skills/retail-product-search/EVAL.yaml`)
  - 10 comprehensive evaluation scenarios, LLM-as-judge rubrics, deterministic test assertions.
- `references/architecture.md`
  - Semantic similarity vs. structured filtering breakdown, architectural insertion points for price/stock filters.
- `references/troubleshooting.md` & `references/install-paths.md`
  - Python version mismatches, YAML frontmatter parser failures, newline bugs in `VECTOR_SEARCH_COLLECTION`, bare `adk` venv leakage.
- `tests/test_runnability.py`
  - Smoke testing runner verifying `scripts.agent.root_agent` instantiation.

## 2. Platform & Protocol Standards
- `AUTONOMOUS_RESEARCH_PROTOCOL.md` (Antigravity 8-Pillar Standard).
- Google ADK (Agent Development Kit) runtime specifications.
- Gemini Enterprise Agent Platform Vector Search 2.0 API guidelines.
