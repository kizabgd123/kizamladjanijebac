# 🧠 Sveska 5: CodyMaster Brain

- **UUID:** `5655b056-6070-485b-a6ba-aa45a0d28a32`
- **Vlasništvo:** `owned` (Lična sveska korisnika)
- **Broj izvora:** 1 sveobuhvatan izvor (Kompajlirano znanje, lekcije i katalog veština)
- **Verifikacioni status:** ✅ 100% VERIFIKOVANO (Upisana Antigravity Wiki beleška ID: `0e120c98-d752-4500-930b-906cdd8dfbc7`)

## 🧱 Principi i arhitektura sistema:
1. **Dual-Brain Koncept:**
   - Global Master Brain (codymaster): Univerzalno znanje i katalog veština.
   - Project-isolated Brain (.cm/notebook_id): Znanje specifično za lokalni repozitorijum.
2. **Deterministički RAG Pajplajn (7 faza):**
   - Authorize -> Classify -> Plan -> Retrieve -> Validate -> Synthesize -> Verify -> Policy Gate -> Audit
   - Sprečava suptilna odstupanja i halucinacije probabilističkih modela kroz mehaničko proveravanje dokaza.
3. **Pravilo od tri sloja (Rule of 3):**
   - Skill Index: Sloj 1 (Indeks ~100 tokena), Sloj 2 (Rezime ~300 tokena), Sloj 3 (Puni SKILL.md pri izvršavanju).
   - 3 Agenta sa po 3 protokola: Agent za kuriranje (Reddit, YouTube, PDF), Agent za kognitivno slojevanje (Anchoring, Progressive complexity, Analogije), Agent za dijagnostiku (Failure mode, Tradeoff, Stress-testing).
4. **Memory Sync i PYTHONPATH izolacija:**
   - Podela na memory/YYYY-MM-DD.md (dnevni logovi) i MEMORY.md (isključivo glavna sesija).
   - Sve komande se pokreću sa PYTHONPATH= prefiksom radi sprečavanja konflikata biblioteka.
