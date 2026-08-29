# 🚀 Sveska 4: Google Anti-gravity: Agentni IDE za Kodiranje

- **UUID:** `b9e49fa1-1e97-4614-80ea-62da45ae9d43`
- **Vlasništvo:** `owned` (Lična sveska korisnika)
- **Broj izvora:** 30 izvora (Zvanične objave Google DeepMind-a, vodiči, pravila, bezbednosne polise)
- **Verifikacioni status:** ✅ 100% VERIFIKOVANO (Upisana Antigravity Wiki beleška ID: `b6a5048d-bbe7-49e6-9d6a-6282aa57f48e`)

## ⚙️ Arhitektura i operativni radni tok IDE platforme:
1. **Tri radne površine:**
   - **Editor View:** Sinhrono kodiranje sa tab-autocomplete, tab-to-import i Cmd + I inline komandama.
   - **Agent Manager View ("Mission Control"):** Asinhrona paralelna orkestracija više agenata i radnih prostora sa Inbox praćenjem.
   - **Browser Agent:** Chrome subagent na izolovanom profilu za istraživanje, autonomno UI testiranje, snimanje sesija i self-healing UI.
2. **Verifiable Artifacts (Rešavanje "Trust Gap-a"):**
   - Tasks, Implementation Plans, Walkthroughs sa video snimcima i screenshotovima.
   - Korisnik može ostavljati inline komentare u stilu Google Docs-a pre klika na Proceed.
3. **Bezbednosni okviri:**
   - Terminal Execution Policies: Off (samo Allow lista), Auto (procena rizika), Turbo (sve osim Deny liste).
   - Browser URL Allowlist: Fajl ~/.gemini/antigravity/browserAllowlist.txt štiti od prompt-injection napada.
4. **Prilagođavanje:** Rules (~/.gemini/GEMINI.md, .agent/rules/) kao trajna sistemska savest naspram Workflows (.agent/workflows/) kao promptova na zahtev sa / prečicom.
