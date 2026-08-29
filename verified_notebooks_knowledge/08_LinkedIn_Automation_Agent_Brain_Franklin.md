# 🤖 Sveska 8: LinkedIn Automation Agent Brain — Elegant Franklin 2026

- **UUID:** `4f6b5323-3465-4071-851d-e153416be6d3`
- **Vlasništvo:** `shared_with_me` (Deljena sveska za čitanje)
- **Broj izvora:** 25 izvora (Arhitektura, SOP priručnik, moderni CLI alati, benchmark testovi)
- **Verifikacioni status:** ✅ 100% VERIFIKOVANO

## 🚀 Arhitektura autonomnog publishing sistema:
1. **Slojevita Plugin arhitektura i Dualni interfejs:**
   - Hibridni model: CLI (main.py sa argparse) + FastMCP (mcp_server.py) nad zajedničkim domenom bez dupliranja koda.
   - Decoupled Planner-Executor: Odvajanje kognitivnog stratega od tehničkog egzekutora.
2. **Moderni CLI ekosistem i GPU akceleracija:**
   - ripgrep (rg) + fzf + bat: Fuzija pretrage (change:reload:sleep 0.1 debouncer, ANSI render, dinamički preview prozor).
   - Ghostty: GPU-akcelerisani terminal u Zig jeziku (Apple Metal render, native 120Hz ProMotion, 4x brži ispis).
3. **Sigurnosna kapija i Opservabilnost:**
   - JudgeGuard (judge_guard.py): Pre/post-check provera WORK_LOG.md svežine (5 min) i MASTER_ORCHESTRATION.md usklađenosti.
   - OBS Telemetry Bridge (obs_wiggum_bridge.py): NVENC hardversko strimovanje toka misli agenta na OBS HUD.
4. **Content Lifecycle:**
   - NotebookLM Query -> Deep Web Research -> Soul.py Validation (7 QA nivoa) -> JudgeGuard Check -> LinkedIn UGC API v2 -> Feedback Loop u NotebookLM.
