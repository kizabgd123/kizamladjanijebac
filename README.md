# Sovereign AI Agent Architecture & Antigravity-Hermes Kit

Dobrodošli u centralni repozitorijum za autonomni multi-agentni sistem (Antigravity + Hermes Agent) sa integrisanim bezbednosnim mehanizmom (JudgeGuard) i automatizovanim bootstrap-om.

---

## 🚀 Brza instalacija iz početka (Quickstart)

Kada klonirate ovaj repozitorijum na bilo koji novi računar (Linux ili Windows WSL2), kompletno okruženje se podiže u jednoj komandi:

```bash
git clone https://github.com/kizabgd123/kizamladjanijebac.git
cd kizamladjanijebac/agy-hermes-kit
./bootstrap.sh
```

### Šta bootstrap skripta radi

1. **Sistemske provere:** Verifikuje prisustvo `git`, `curl`, `python3`, `node`, `npx`.
2. **Paketi okruženja:** Instalira `pyyaml` i `mcp` (FastMCP).
3. **Struktura foldera:** Kreira `~/.agents/skills`, `~/.gemini/antigravity/skills`, `~/.hermes/skills`, `~/projects`.
4. **Distribucija skilova:** Automatski povezuje sve zajedničke skilove u oba sistema.
5. **MCP Sinhronizacija:** Parsira `configs/connections.json` i upisuje konfiguracije u:
   - Antigravity: `~/.gemini/antigravity/mcp_config.json`
   - Hermes: `~/.hermes/config.yaml`
6. **Agensi:** Proverava i po potrebi vodi instalaciju `agy` (Antigravity CLI) i `hermes` (Hermes Agent).
7. **Verifikacija:** Pokreće `scripts/verify.sh` i dijagnostiku celog sistema (`hermes doctor`).

---

## 🏛️ Arhitektura sistema

```text
                         [ connections.json ]
                         (Single Source of Truth)
                                  │
                   ┌──────────────┴──────────────┐
                   ▼                             ▼
       [ Antigravity System ]           [ Hermes Agent ]
       ~/.gemini/antigravity/           ~/.hermes/
       ├── mcp_config.json              ├── config.yaml
       └── skills/                      ├── .env
           └── SKILL.md                 └── skills/
                                            └── SKILL.md
                   │                             │
                   └──────────────┬──────────────┘
                                  ▼
                     [ JudgeGuard & WORK_LOG.md ]
                     (Safety, Tracking & Governance)
```

---

## 🛡️ Pravila verifikacije i razvojni tok (MANDATORY)

Svi agenti i saradnici moraju poštovati protokol definisan u `~/.gemini/MASTER_ORCHESTRATION.md`:

Pre svake akcije:

```bash
echo "🟡 Starting [ACTION]" >> WORK_LOG.md
python3 judge_guard.py "Start [ACTION]"
```

Nakon izvršene akcije:

```bash
echo "✅ Completed [ACTION]" >> WORK_LOG.md
python3 judge_guard.py "Verify [ACTION] Complete"
git add . && git commit -m "checkpoint: [ACTION]"
```

Ograničenje taskova: Maksimalno 5 paralelnih `🟡 Starting` taskova pre nego što se prethodni moraju zatvoriti (`✅ Completed` ili `⚠️ Abandoned`).

---

## 📂 Struktura repozitorijuma

- **`agy-hermes-kit/`** — Prenosivi instalacioni i konfiguracioni kit za Antigravity + Hermes.
  - `bootstrap.sh` — Master skripta za instalaciju na novoj mašini.
  - `configs/connections.json` — Centralni registar MCP servera.
  - `configs/hermes.env.example` — Šablon za environment varijable i API ključeve.
  - `scripts/sync_mcp.py` — Generator MCP konfiguracija za oba formata.
  - `scripts/verify.sh` — Skripta za brzu dijagnostiku instalacije.
  - `skills/` — Paket unapred pripremljenih skilova (`antigravity-orchestration`, `cm-skill-index`, `code-review-and-quality`).
  - `custom_tools/my_tool_server.py` — Primer prilagođenog FastMCP servera.
- **`judge_guard.py`** — 3-slojni zaštitni modul za kontrolu integriteta i bezbednosti.
- **`WORK_LOG.md`** — Zvanični revizorski dnevnik aktivnosti.
- **`AGENTS.md`** — Uputstvo i kontekst za AI agente koji rade u ovom repozitorijumu.
