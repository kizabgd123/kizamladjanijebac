# Antigravity + Hermes Agent Kit (2026)

Kompletno prenosivo rešenje za pokretanje i orkestraciju **Google Antigravity** i **Nous Research Hermes Agent** okruženja sa zajedničkim MCP serverima i SKILL.md skilovima.

## ⚡ Brzi start (Instalacija iz početka na novoj mašini)

Klonirajte repozitorijum i pokrenite master bootstrap skriptu:

```bash
git clone https://github.com/kizabgd123/kizamladjanijebac.git
cd kizamladjanijebac/agy-hermes-kit
./bootstrap.sh
```

Bootstrap skripta automatski:
1. Proverava preduslove (`git`, `curl`, `python3`, `node`, `npx`).
2. Instalira Python zavisnosti (`pyyaml`, `mcp`).
3. Kreira standardnu strukturu foldera (`~/.agents/skills`, `~/.gemini/antigravity/skills`, `~/.hermes/skills`).
4. Povezuje i sinhronizuje sve skilove iz ovog kita u Antigravity i Hermes.
5. Sinhronizuje `configs/connections.json` u `~/.gemini/antigravity/mcp_config.json` i `~/.hermes/config.yaml`.
6. Proverava/vodi instalaciju `agy` i `hermes` CLI alata i pokreće `verify.sh`.

---

## Sadržaj kita
- `bootstrap.sh` — Automatizovani installer i sinhronizator za celu mašinu
- `configs/` — Centralni `connections.json`, primeri konfiguracija i `.env.example`
- `scripts/` — `sync_mcp.py`, `install_antigravity.sh`, `install_hermes.sh`, `verify.sh`
- `skills/` — Paket proverenih skilova (`antigravity-orchestration`, `cm-skill-index`, `code-review-and-quality`)
- `custom_tools/` — Primer FastMCP Python servera (`my_tool_server.py`)
- `SOURCES.md` — Izvori dokumentacije i referenci

Oznake pouzdanosti: [V] = potvrđeno u više izvora ili zvaničnoj dokumentaciji, [?] = specifičnosti verzija.

---------------------------------------------------------------------
## 1. PREGLED I PREDUSLOVI

### Sta je sta
- Antigravity: Google-ov agentni razvojni alat. Postoje desktop IDE, Antigravity CLI (komanda `agy`, nasljednik Gemini CLI-ja; potrosacki Gemini CLI pristup se gasi 18. juna 2026 prema CoinGecko dokumentaciji) i Python SDK (`pip install google-antigravity`, research preview, Apache 2.0). [V]
- Hermes Agent: open-source agent kompanije Nous Research (MIT licenca), repo https://github.com/NousResearch/hermes-agent, dokumentacija https://hermes-agent.nousresearch.com/docs . Napomena: ovo je agent, ne samo Hermes model; radi sa bilo kojim provajderom (Nous Portal, OpenRouter, OpenAI-kompatibilni endpoint...). [V]

### Preduslovi
- Git (Hermes instaler: "no prerequisites except git"). [V]
- Hermes instaler sam instalira uv, Python 3.11, Node.js, ripgrep, ffmpeg. [V]
- Node.js + npx treba za MCP servere pokretane preko `npx` (npr. filesystem). [V]
- Python 3.11+ za Hermes ACP i za custom_tools/. [V]
- Google nalog (browser login) ili `GEMINI_API_KEY` za headless Antigravity CLI. [V]
- API kljuc za LLM provajdera Hermesa (OPENROUTER_API_KEY, ili Nous Portal login, ili OPENAI_BASE_URL + OPENAI_API_KEY). [V]
- GITHUB_TOKEN (PAT) ako koristis GitHub MCP.
- Windows: Hermes README iz 2026 pominje nativnu instalaciju (PowerShell), stariji README kaze samo WSL2. [?] Najsigurnije: WSL2.

### Kljucne promene i dobre prakse 2026
Antigravity:
- Gemini CLI -> Antigravity CLI migracija; stari ~/.gemini/ ostaje netaknut pa je migracija reverzibilna. [V]
- Skilovi su folderi sa SKILL.md; workspace lokacija je .agents/skills/<ime>/SKILL.md. [V]
- MCP je u zasebnom fajlu (mcp_config.json), odvojeno od skilova. [V]
- Instaliraj samo iz zvanicnog izvora (antigravity.google), ne iz "neoficijelnih" paketa; pocni sa review-driven politikom i probnim repozitorijumom bez osetljivih podataka. [V]
- Najmanje privilegija: eksplicitno odobravanje terminal/browser/network akcija.

Hermes:
- Jedan config (~/.hermes/config.yaml), jedan secrets fajl (~/.hermes/.env), skilovi u ~/.hermes/skills/. [V]
- MCP je nativni klijent; posle izmene configa koristi /reload-mcp. [V]
- Tajne nikad u config.yaml: koristi ${VAR} u headers (Hermes ih zamenjuje pri konektovanju) i drzi vrednosti u ~/.hermes/.env. [V]
- Za nepoverene servere dodaj `trust: untrusted` da Hermes trazi potvrdu. [V]
- `hermes doctor` za dijagnostiku, `hermes update` za azuriranje. [V]

---------------------------------------------------------------------
## 2. KORAK-PO-KORAK INSTALACIJA

### Korak 1: Antigravity CLI
Zvanicna migraciona dokumentacija (reference u izvorima): https://antigravity.google/docs/gcli-migration

macOS/Linux:
    curl -fsSL https://antigravity.google/cli/install.sh | bash
    export PATH="$HOME/.local/bin:$PATH"
    agy --version

Windows PowerShell:
    irm https://antigravity.google/cli/install.ps1 | iex

Prijava: pokreni `agy` i prati browser login. Headless/CI: postavi GEMINI_API_KEY i u settings.json "modelProvider":"gemini". [V, jedan izvor za modelProvider]

Preporuka: pre `| bash` skini skriptu, procitaj je, pa pokreni:
    curl -fsSL https://antigravity.google/cli/install.sh -o agy_install.sh && less agy_install.sh && bash agy_install.sh

Migracija sa Gemini CLI: tacna komanda se razlikuje po izvorima (jedan pominje `antigravity migrate --from-gemini-cli`). [?] Proveri na https://antigravity.google/docs/gcli-migration . Rucna varijanta za skilove: `git mv .gemini/skills .agents/skills`.

Antigravity IDE (desktop): skini samo sa zvanicne stranice antigravity.google.

Opciono, Python SDK:
    python3 -m venv .venv && source .venv/bin/activate
    pip install google-antigravity

### Korak 2: Hermes Agent
Linux, macOS, WSL2, Termux:
    curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
    source ~/.bashrc    # ili ~/.zshrc

Alternativa (raw GitHub skripta, ista stvar iz repozitorijuma):
    curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

Podesavanje:
    hermes setup            # wizard: provajder, model, kljucevi
    hermes setup --portal   # alternativa: Nous Portal OAuth + Tool Gateway
    hermes model            # promena provajdera/modela
    hermes doctor           # dijagnostika
    hermes                  # interaktivni CLI

Rucne varijable (~/.hermes/.env), vidi configs/hermes.env.example:
    OPENROUTER_API_KEY=...
    # ili custom endpoint:
    OPENAI_BASE_URL=...
    OPENAI_API_KEY=...

Optimizacija (iz dokumentacije): modele menjaj sa `hermes model` bez izmene koda; ako imas dugacke sesije, pogledaj sekciju compression u ~/.hermes/config.yaml (https://hermes-agent.nousresearch.com/docs ima "Configuration" stranicu sa svim opcijama). Konkretne vrednosti compression-a nisam potvrdio, ne menjam ih naslepo.

### Korak 3: Povezivanje Antigravity i Hermes
Bitno: NISAM nasao zvanicnu, dokumentovanu direktnu integraciju Antigravity <-> Hermes. Zato kit koristi tri potvrdjena gradivna elementa. Nista od ovoga nije "jedno dugme".

Opcija A (preporucena): zajednicki MCP serveri.
Obe strane citaju MCP. U configs/connections.json definises servere jednom, a scripts/sync_mcp.py generise oba formata:
    python3 scripts/sync_mcp.py --target both            # dry-run, samo prikaz
    python3 scripts/sync_mcp.py --target both --write    # upisuje uz backup

Opcija B: zajednicki skilovi (isti SKILL.md format, razliciti folderi).
    mkdir -p ~/.hermes/skills .agents/skills
    ln -s "$(pwd)/skills/example-custom-skill" ~/.hermes/skills/example-custom-skill
    ln -s "$(pwd)/skills/example-custom-skill" .agents/skills/example-custom-skill
Skill alat `npx skills add <repo> --agent hermes-agent` potvrdjeno cilja Hermes; isti alat instalira i za Antigravity (u ~/.agents/skills, pa se premesta u ~/.gemini/skills ili .agents/skills). [V]

Opcija C: Hermes kao editor-agent preko ACP (Agent Client Protocol).
Hermes dokumentuje ACP za VS Code, Zed i JetBrains: `pip install -e ".[acp]"` u Hermes checkout-u, pa komanda `hermes acp`. Zed primer:
    { "agent_servers": { "hermes-agent": { "type": "custom", "command": "hermes", "args": ["acp"] } } }
Da li Antigravity IDE (VS Code fork) moze da koristi ACP klijent ekstenziju nisam potvrdio. [?] Ne oslanjaj se na to bez testa.

---------------------------------------------------------------------
## 3. INTEGRACIJA PRILAGODJENIH SKILOVA I KONEKCIJA

### 3.1 Skilovi
Antigravity:
- Workspace: .agents/skills/<ime>/SKILL.md (svaki skill u svom podfolderu). [V]
- Globalno: ~/.gemini/skills (Dazbo, maj 2026) ili ~/.gemini/antigravity-cli/skills (inventivehq). [?] Izvori se razilaze; koristi workspace putanju dok ne potvrdis, i proveri sa `agy skills list` ili `/skills` u CLI-ju.
Hermes:
- ~/.hermes/skills/ ; plugin instalacija: `hermes plugins install <owner>/<repo>`. [V]
- Migracija sa Claude Code: `hermes import-agent claude-code` (prenosi mcpServers, skilove, instrukcije). [V]

Primer: skills/example-custom-skill/SKILL.md u ovom zipu.

### 3.2 Konekcije (MCP)
Jedan izvor istine: configs/connections.json.
Antigravity IDE cita ~/.gemini/antigravity/mcp_config.json (CoinGecko dokumentacija); noviji clanak (maj 2026) opisuje zajednicki ~/.gemini/config/mcp_config.json. [?] Skripta ima --antigravity-path za oba slucaja.
Format za udaljene servere u Antigravity: kljuc "serverUrl". Za lokalne: "command","args","env". [V]
Hermes: ~/.hermes/config.yaml pod `mcp_servers`; lokalni = command/args/env, udaljeni = url/headers/timeout. [V]

Primeri su u configs/antigravity_mcp_config.example.json i configs/hermes_config.example.yaml.

Custom Python alat: custom_tools/my_tool_server.py (FastMCP iz `pip install mcp`). Pokrece ga oba klijenta kao stdio proces.

Tajne: GITHUB_TOKEN stavi u ~/.hermes/.env (Hermes zamenjuje ${GITHUB_TOKEN} u headers). Za Antigravity skripta upisuje stvarnu vrednost u mcp_config.json (nisam potvrdio da Antigravity radi ${VAR} zamenu), pa se fajl postavlja na chmod 600. Ne commit-uj ga.

---------------------------------------------------------------------
## 4. TROUBLESHOOTING I VERIFIKACIJA

### Test
    bash scripts/verify.sh
Rucno:
    agy --version
    agy skills list            # skill mora da se pojavi
    hermes doctor
    hermes                     # zatim u sesiji: /reload-mcp, pa pitaj "list your MCP tools"
Antigravity IDE: Agent pane -> MCP Servers -> Manage MCP Servers -> View raw config; server treba da se pojavi pod Available Tools.

### 3 najcesce greske
1. MCP alati se ne pojavljuju u Hermesu.
   Uzroci iz dokumentacije: kljuc nije `mcp_servers` (ne `mcp` ni `servers`), pogresna YAML indentacija, server nije povezan, nema npx/node.
   Resenje: proveri `node --version && npx --version`, ispravi indentaciju, `pip install --upgrade mcp` (stariji mcp paket nema HTTP klijent), pa /reload-mcp. Za OAuth servere: `hermes mcp login <ime>`.
2. `agy` ili `hermes` komanda nije pronadjena posle instalacije.
   Resenje: `export PATH="$HOME/.local/bin:$PATH"` (agy se instalira u ~/.local/bin); za Hermes `source ~/.bashrc` / `source ~/.zshrc`.
3. Antigravity ne vidi skill ili MCP posle migracije sa Gemini CLI.
   Resenje: skilovi i MCP se premestaju odvojeno (`git mv .gemini/skills .agents/skills`, pa MCP u mcp_config.json); "tihi neuspeh" MCP-a je opisan kao poznata zamka, proveri raw config i putanju iz sekcije 3.2.

### Dodatno
- Hermes debug: `HERMES_LOG_LEVEL=DEBUG hermes acp`.
- Windows antivirus moze oznaciti uv.exe (Rust binar) kao sumnjiv; Hermes dokumentacija opisuje verifikaciju preko GitHub CLI.

Svi linkovi: SOURCES.md
