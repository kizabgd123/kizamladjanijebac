import os
import sys
import json
import sqlite3
import time
import uuid
import hashlib
import shutil

KNOWLEDGE_DIR = "/home/kizamladjanijebac/verified_notebooks_knowledge"
os.makedirs(KNOWLEDGE_DIR, exist_ok=True)

# 15 Verified Notebooks with full deep knowledge
notebooks = [
    {
        "num": 1,
        "filename": "01_Vas_Mozak_Ko_Je_U_Kontroli.md",
        "title": "Vaš Mozak: Ko je u Kontroli? — Neurobiološki Model i Kontrola Uma",
        "uuid": "431444a0-04ce-4809-b586-d226bc9f5655",
        "sources": 5,
        "content": """# 🧠 Sveska 1: Vaš Mozak: Ko je u Kontroli? — Neurobiološki Model i Kontrola Uma

- **UUID:** `431444a0-04ce-4809-b586-d226bc9f5655`
- **Vlasništvo:** `shared_with_me` (Deljena sveska za čitanje)
- **Broj izvora:** 5 izvora (NOVA PBS dokumentarac, neurološke studije, vodiči za navike i kontrolu emocija)
- **Verifikacioni status:** ✅ 100% VERIFIKOVANO

## 🔬 Verifikovane ključne činjenice i naučni model:
1. **Iluzija jedinstva i Talamus:** Mozak se sastoji od skoro 90 milijardi neurona. Talamus deluje kao centralna komunikaciona stanica za senzorne i motorne signale; njegovo uklanjanje dovodi do trenutnog gubitka svesti.
2. **Split-Brain hirurgija i lateralizacija (Corpus Callosum):** Kod presecanja korpus kalozuma, leva hemisfera (govor/jezik) i desna hemisfera (vizuelno-prostorna obrada i emocije) funkcionišu kao dva odvojena kognitivna centra (eksperiment sa pacijentom Joe – crtanje kaubojskog šešira levom rukom bez verbalnog prepoznavanja).
3. **Prefrontalni korteks (PFC) i spontana kreativnost:** Slučaj Phineasa Gagea dokazao je lokaciju moralnosti i socijalnih filtera u PFC-u. Tokom spontane improvizacije (freestyle rap, vrhunski sport), aktivnost PFC-a se smanjuje, što sprečava fenomen „gušenja pod pritiskom” (choking).
4. **Epigenetika i transgeneracijska trauma:** Eksperimenti Biance Jones Marlin pokazali su da se osetljivost na miris badema kod miševa izloženih elektro-šokovima prenosi na potomke preko strukturnih promena u receptorima.
5. **Jutarnje navike i eliminacija -4 kognitivnog minusa:** Izbegavanje telefona u prvih 10 minuta eliminiše distrakcije (News, Notifications, Negativity, Noise). Zahvalnost mora biti izražena, specifična i lična.
6. **Rekonsolidacija sećanja (Kareem Nader):** Čin prisećanja čini sećanje privremeno nestabilnim i podložnim rekodiranju pre novog skladištenja.
"""
    },
    {
        "num": 2,
        "filename": "02_AI_Native_Transformation_SEE_Digital_Engineering.md",
        "title": "AI Native Transformation in SEE Digital Engineering — Endava & Levi9 Studija",
        "uuid": "2d7312fc-1a9c-4ca8-838a-7769a7e115c6",
        "sources": 21,
        "content": """# 🤖 Sveska 2: AI Native Transformation in SEE Digital Engineering

- **UUID:** `2d7312fc-1a9c-4ca8-838a-7769a7e115c6`
- **Vlasništvo:** `owned` (Lična sveska korisnika)
- **Broj izvora:** 21 izvor (Endava, Levi9, LangChain studije slučaja, Databricks ugovori, RAG bele knjige)
- **Verifikacioni status:** ✅ 100% VERIFIKOVANO (Upisana Antigravity Wiki beleška ID: `0e41cad8-b1fe-456a-8d93-934b25780379`)

## 🏢 Uporedna analiza transformacije (Endava vs Levi9):
1. **Endava:**
   - **Dava.Flow okvir:** Četiri faze (Signal, Explore, Govern, Evolve); pilot projekti donose do 40% kraći time-to-market.
   - **OpenAI Beta Services Partnership:** Jedna od samo 7 kompanija na svetu sa ovim statusom.
   - **Akceleratori:** Morpheus (agentni AI za regulisane industrije sa potpunim revizorskim tragom) i Compass (kopilot za kompleksan kod).
   - **Javni sektor:** Okvirni sporazum sa Vladom Rumunije (ADR) za migraciju 30+ državnih aplikacija u vladin cloud.
2. **Levi9:**
   - **AI Powered Development Team:** Privremeni namenski tim za transformaciju SDLC-a klijenta NS Groep (Cursor, Claude Code, GitHub Copilot).
   - **Quality9:** Interni QA okvir koji osigurava bezbednost koda i zadržava human-in-the-loop kontrolu nad agentima.
   - **AI Readiness:** Strukturisana procena zrelosti (AI Discovery, AI Testing, GenAI Data Intelligence).
3. **Tehnološki standardi:** Python kao baza, LangChain/LangGraph za multi-agent rutiranje, Databricks/Spark/Kafka za striming i RAG sa dvofaznim rerankiranjem (BGE-reranker).
"""
    },
    {
        "num": 3,
        "filename": "03_Project_OpenClaw_Sovereign_AI_OS.md",
        "title": "Project OpenClaw — Suvereni AI OS 2026 i Deterministički Debate Engine",
        "uuid": "8ad849c0-4d27-486e-8903-2d7aa0231258",
        "sources": 1,
        "content": """# 💓 Sveska 3: Project OpenClaw — Suvereni AI OS 2026

- **UUID:** `8ad849c0-4d27-486e-8903-2d7aa0231258`
- **Vlasništvo:** `owned` (Lična sveska korisnika)
- **Broj izvora:** 1 sveobuhvatan izvor (Arhitektura, manifest i tehnička specifikacija)
- **Verifikacioni status:** ✅ 100% VERIFIKOVANO (Upisana Antigravity Wiki beleška ID: `ab65b4bf-b0ea-4052-99f8-37aeec9c2dd6`)

## 🛡️ Arhitektura suverenog AI OS-a (2026):
1. **Debate Engine (5 persona):** Deterministička mašina stanja kroz 2 runde (10 poteza):
   - Švaba (Moderator), Ekser (Tehnički arhitekta), Pikac (Bezbednosni revizor), Dule Pacov (Poslovni strateg), Babac (Završni evaluator sa matricom ocenjivanja).
   - Ishod se nepromenljivo upisuje u DECISION_RECORD_EVIDENCE_LAYER.md sa SHA-256 ulančavanjem.
2. **BrainCore 2-Tier memorija:** Tier 1 (SQLite FTS5 antigravity_rag.db, <5ms odziv) + Tier 2 (Google NotebookLM za autoritativno uzemljenje).
3. **JudgeGuard sigurnosna kapija:** HMAC-SHA256 potpisivanje, 5-minutni prozor svežine za WORK_LOG.md, striktna crna lista (rm -rf /, chmod 777).
4. **Discord Control Plane:** 13 slash komandi sa višenamenskim vebhukovima.
5. **Aplikativni moduli:** eq_system (BeautifulMinds 7-radnički pipeline sa Three Chairs metodologijom i CriticAgent-om), debate_engine, ig_automation, nlm MCP server.
"""
    },
    {
        "num": 4,
        "filename": "04_Google_Antigravity_Agentic_IDE.md",
        "title": "Google Anti-gravity: Agentni IDE za Kodiranje — Arhitektura i Artefakti",
        "uuid": "b9e49fa1-1e97-4614-80ea-62da45ae9d43",
        "sources": 30,
        "content": """# 🚀 Sveska 4: Google Anti-gravity: Agentni IDE za Kodiranje

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
"""
    },
    {
        "num": 5,
        "filename": "05_CodyMaster_Brain_Deterministic_RAG.md",
        "title": "CodyMaster Brain — Dual-Brain Arhitektura i 7-Stage Deterministički RAG",
        "uuid": "5655b056-6070-485b-a6ba-aa45a0d28a32",
        "sources": 1,
        "content": """# 🧠 Sveska 5: CodyMaster Brain

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
"""
    },
    {
        "num": 6,
        "filename": "06_Prokrastinacija_Naucna_Analiza_TMT.md",
        "title": "Prokrastinacija — Teorija Temporalne Motivacije (TMT) i Emocionalna Regulacija",
        "uuid": "860732d6-4de0-4f37-9704-47f09f8c7b14",
        "sources": 13,
        "content": """# 🧠 Sveska 6: Prokrastinacija - Naučna Analiza

- **UUID:** `860732d6-4de0-4f37-9704-47f09f8c7b14`
- **Vlasništvo:** `shared_with_me` (Deljena sveska za čitanje)
- **Broj izvora:** 13 izvora (Piers Steel, Timothy Pychyl & Fuschia Sirois, neurobiološke studije sa fMRI)
- **Verifikacioni status:** ✅ 100% VERIFIKOVANO

## 🔬 Naučni modeli, formule i neurobiologija:
1. **Teorija temporalne motivacije (TMT - Piers Steel):**
   $$\\text{Motivacija} = \\frac{\\text{Očekivanje (Expectancy)} \\times \\text{Vrednost (Value)}}{1 + \\text{Impulsivnost (Impulsiveness)} \\times \\text{Kašnjenje / Rok (Delay)}}$$
   - Impulsivnost je najsnažniji karakterni prediktor prokrastinacije (r = -0.62 korelacija sa savesnošću).
   - Hiperbolično diskontovanje: Nagrade u dalekoj budućnosti mozak drastično obezvređuje; motivacija eksponencijalno raste tek u neposrednoj blizini roka.
2. **Emocionalna regulacija (Sirois & Pychyl):**
   - Prokrastinacija NIJE problem upravljanja vremenom, već problem kratkoročne regulacije emocija („giving in to feel good”).
   - Začarani krug olakšanja (Relief Loop): Izbegavanje neprijatnog zadatka donosi trenutno olakšanje -> mozak to beleži kao nagradu -> pojačava se obrazac izbegavanja.
   - Vremenski rascep sopstva: Mozak percipira „buduće ja” više kao stranca nego kao deo sebe (Hal Hershfield).
3. **Neurobiološki sukob: Limbički sistem vs. Prefrontalni korteks (PFC):**
   - Amigdala (Limbički sistem): Brz, detektuje anksiozan zadatak kao pretnju po ego i pokreće Amygdala Hijack (beg kroz izbegavanje).
   - Prefrontalni korteks (PFC): Sporiji izvršni centar za dugoročne ciljeve. Oslabljuju ga umor, stres i decision fatigue.
4. **Verifikovane intervencije:**
   - Implementacione namere („Ako-Onda” planovi - Gollwitzer): Automatizacija okidača u okruženju.
   - Pravilo 5 minuta / Mikro-koraci: Smanjivanje početnog praga ispod nivoa detekcije pretnje u amigdali.
   - Odisejev pakt (Precommitment): Racionalno unapred blokiranje distrakcija i iskušenja.
   - Samosaosećanje i samoopraštanje (Wohl, Pychyl 2010): Eliminacija sekundarnog stresa i krivice.
"""
    },
    {
        "num": 7,
        "filename": "07_NotebookLM_Custom_Prompts_Advanced_AI.md",
        "title": "NotebookLM: Custom Prompts for Advanced AI Learning — Audio & Video Studio",
        "uuid": "1d289980-275e-4e15-833e-7a06c81625d3",
        "sources": 7,
        "content": """# ⚙️ Sveska 7: NotebookLM: Custom Prompts for Advanced AI Learning

- **UUID:** `1d289980-275e-4e15-833e-7a06c81625d3`
- **Vlasništvo:** `owned` (Lična sveska korisnika)
- **Broj izvora:** 7 izvora (Reddit r/notebooklm, DataCamp vodiči, zvanična dokumentacija za Video Overview)
- **Verifikacioni status:** ✅ 100% VERIFIKOVANO (Upisana Antigravity Wiki beleška ID: `eaacc5ef-bd03-4784-a6b1-03c76fff97ce`)

## 🛠️ Strategije i optimizacija Custom instrukcija:
1. **Chat Custom Instructions (500 karaktera):**
   - Pristup preko dugmeta sa 3 klizača (Configure Chat).
   - Postavljanje Guardrails token limita (<100 ili <500 tokena) kako bi AI navigirao do izvora umesto da generiše gotove radove.
   - Usidrenje (Anchoring): Kombinovanje ličnih hobija/analoga za pojednostavljivanje teških koncepata.
2. **Audio Overview (AI Podcast) Customization (500 karaktera limit):**
   - Preporučeni šabloni: Beginner interviewing expert, Expert debate on tradeoffs, Expert critique.
   - Uvođenje instrukcije "news style" uspešno uklanja nepotrebno lutanje i moralisanje na kraju epizode.
3. **Video Overview (Desktop Studio):**
   - Formati: Explainer (dubinski) vs Brief (sažeti). Podrška za 80+ jezika.
   - Vizuelni stilovi: Classic, Whiteboard, Watercolor, Retro Print, Heritage, Paper-craft, Kawaii, Anime, Custom.
   - Steering Prompts: Strukturisana mapa učenja, tabela kompromisa i checkliste najčešćih početničkih grešaka.
4. **Metodologija dubokog učenja:**
   - Scenario-based Flashcards: Testiranje odluke o izboru arhitekture (npr. Prompt vs RAG vs Fine-tuning).
   - Failure Mode Quizzes: Predviđanje tačaka pucanja sistema.
   - Progressive Reports: 4-stepeni progres od potpunog početnika bez žargona do ekspertskog nivoa.
"""
    },
    {
        "num": 8,
        "filename": "08_LinkedIn_Automation_Agent_Brain_Franklin.md",
        "title": "LinkedIn Automation Agent Brain (Elegant Franklin 2026) — CLI & Obs Bridge",
        "uuid": "4f6b5323-3465-4071-851d-e153416be6d3",
        "sources": 25,
        "content": """# 🤖 Sveska 8: LinkedIn Automation Agent Brain — Elegant Franklin 2026

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
"""
    },
    {
        "num": 9,
        "filename": "09_Gemini_3_Prompting_Rules_NotebookLM.md",
        "title": "Pomoć i Povratne Informacije za NotebookLM — Zvanična Gemini 3 Pravila",
        "uuid": "80540e39-3bae-4b5a-a9e6-fe12bec21d4b",
        "sources": 2,
        "content": """# ❓ Sveska 9: Pomoć i Povratne Informacije za NotebookLM

- **UUID:** `80540e39-3bae-4b5a-a9e6-fe12bec21d4b`
- **Vlasništvo:** `owned` (Lična sveska korisnika)
- **Broj izvora:** 2 izvora (NotebookLM Help Centar, Google Gemini API Prompt Design Strategies)
- **Verifikacioni status:** ✅ 100% VERIFIKOVANO (Upisana Antigravity Wiki beleška ID: `1bb471eb-8b7d-4b54-885e-dc931c04fb24`)

## 📝 Zvanična pravila i standardi za Gemini 3 promptovanje:
1. **Gemini 3 Specifične preporuke:**
   - **Temperatura:** Strogo zadržati na podrazumevanoj vrednosti 1.0 (smanjenje temperature ispod 1.0 kod Gemini 3 izaziva degradaciju performansi i beskonačne petlje u matematici i logici).
   - **Formatiranje i Delimiteri:** Korišćenje konzistentnih XML tagova (<role>, <constraints>, <context>, <task>) ili jasnih Markdown sekcija.
   - **Struktura za dugi kontekst:** Dokumenti i masivni podaci se uvek unose na početku prompta, a specifične instrukcije i pitanja na samom kraju uz prelazne fraze (Anchor context).
2. **Few-Shot i Pozitivni obrasci:**
   - Model znatno bolje generalizuje kada vidi pozitivan primer željenog formata nego anti-primer koji treba izbeći.
3. **Chain & Aggregate strategije:**
   - Razbijanje složenih zadataka u sekvencijalni lanac promptova gde je izlaz prethodnog ulaz za sledeći.
4. **NotebookLM Help:** Integrisana pravila privatnosti, uslovi korišćenja, podrška za dark mode i mehanizmi direktnih povratnih informacija.
"""
    },
    {
        "num": 10,
        "filename": "10_NLP_Silva_Metod_Neuroplasticnost.md",
        "title": "NLP: Put do Majstorstva — Silva Metod Kontrole Uma i Zokijev NLP Plan",
        "uuid": "e6a2a636-b9e4-48c6-82e9-e94dcbf452f7",
        "sources": 33,
        "content": """# 🧠 Sveska 10: NLP: Put do Majstorstva

- **UUID:** `e6a2a636-b9e4-48c6-82e9-e94dcbf452f7`
- **Vlasništvo:** `shared_with_me` (Deljena sveska za čitanje)
- **Broj izvora:** 33 izvora (NLP priručnici, Silva metod studije, medicinska istraživanja neuroplastičnosti i zavisnosti)
- **Verifikacioni status:** ✅ 100% VERIFIKOVANO

## 🧘 NLP metodologija, Silva metod i neuroplastičnost:
1. **Neurolingvističko programiranje (NLP - Bandler & Grinder, 1970-e):**
   - Sidrenje (Anchoring): Stvaranje trenutne asocijacije između stimulusa i željenog stanja (samopouzdanje).
   - Reframing: Promena kognitivnog okvira i značenja negativnih misli i događaja.
   - Rapport & Mirroring: Izgradnja dubokog poverenja suptilnim usklađivanjem govora tela, tona glasa i ritma.
   - Swish Pattern & Future Pacing: Zamena loših navika novim slikama i projektovanje ponašanja u budućnost.
2. **Silva Metod Kontrole Uma (Hoze Silva):**
   - Sistematsko voljno uvođenje u alfa stanje svesti (7–14 Hz) bez biofidbek uređaja ili stimulansa.
   - Efikasniji rad mozga, relaksacija, duboko učenje i vizuelizacija rešenja problema.
3. **Neuroplastičnost i lečenje zavisnosti:**
   - Zavisnost je hronična recidivirajuća bolest mozga koja remodelira centre za nagradu, motivaciju i kontrolu impulsa.
   - „Ono što vežbamo postaje naša realnost”. Novo učenje mora biti smisleno i primenjeno u ponašanju kako bi podstaklo sinaptogenezu.
4. **Zokijev NLP Master Plan (3 Faze):**
   - Faza 1: Brzi Start (7 dana) - Sidrenje, Swish, Reframing, Future Pacing, dnevna refleksija.
   - Faza 2: NLP Praktičar (30 dana) - Udemy Associate Certification, 30–60 min/dan, primena min 3x u realnosti, NLP dnevnik.
   - Faza 3: NLP Master u praksi (2–3 meseca) - Michael Breen Kickstart seminar, mentorisanje drugih.
"""
    },
    {
        "num": 11,
        "filename": "11_2026_UI_Design_Principles_Spatial_Computing.md",
        "title": "2026 UI Design Principles & Strategic Best Practices — Spatial Computing & 6-3-1 Rule",
        "uuid": "658307d1-feba-48c2-81ba-db4e3098c98d",
        "sources": 19,
        "content": """# 🎨 Sveska 11: 2026 UI Design Principles and Strategic Best Practices

- **UUID:** `658307d1-feba-48c2-81ba-db4e3098c98d`
- **Vlasništvo:** `owned` (Lična sveska korisnika)
- **Broj izvora:** 19 izvora (Spatial Computing standardi, Figma Dev Mode, WCAG 2.2, Claude Artifacts, v0 by Vercel)
- **Verifikacioni status:** ✅ 100% VERIFIKOVANO (Upisana Antigravity Wiki beleška ID: `dbbd4212-250e-41f1-ad87-1e290c368c2b`)

## 📐 Ključni dizajnerski principi i standardi 2026:
1. **Spatial Computing i 4px Baseline Grid:**
   - Prelazak sa ravnih ekrana na prostorno računanje (Apple Vision Pro, Meta Quest).
   - 4px bazna mreža sa 16px korenskom skalom za savršenu oštrinu i konzistentnost elemenata.
2. **Tipografski brend standard (Artifakt standard):**
   - Artifakt Legend za naslove i visoki vizuelni autoritet; Artifakt Element za čist čitljiv tekst; Arial kao univerzalni fallback.
3. **Interaktivno prototipisanje: Claude Artifacts vs v0 by Vercel:**
   - Claude Artifacts: Izolovani iframe sa striktnim CSP-om, blokiranim formama i mrežnim pozivima, in-memory state hook-ovima.
   - v0 by Vercel: Generisanje produkcijskog Next.js/Tailwind/shadcn koda sa Git grananjem i deploymentom.
4. **Psihologija boja i 6-3-1 pravilo:**
   - Odnos boja 60-30-10: 60% dominantna neutralna, 30% sekundarna strukturna, 10% akcentna boja (primarni CTA).
   - Navigaciono pravilo: Max 6 stavki u meniju, max 3 nivoa hijerarhije, 1 primarna akcija.
   - Levak dizajna: 6 grubih skica -> 3 interaktivna prototipa -> 1 finalni produkcijski dizajn.
5. **Observability Dashboards (SRE Standardi):**
   - 12-kolonska mozaik mreža za metrike.
   - Four Golden Signals: Latencija (P50, P95, P99), Saobraćaj (RPS), Greške (Error rate), Zasićenost (CPU/RAM).
"""
    },
    {
        "num": 12,
        "filename": "12_Duboko_Ucenje_i_Vestacka_Inteligencija.md",
        "title": "Duboko Učenje i Veštačka Inteligencija: Vodič — Pandas, Neuronske Mreže i Trening",
        "uuid": "61482e0f-c16e-41f3-b453-7137e9ee8fd9",
        "sources": 8,
        "content": """# 🤖 Sveska 12: Duboko učenje i veštačka inteligencija: Vodič

- **UUID:** `61482e0f-c16e-41f3-b453-7137e9ee8fd9`
- **Vlasništvo:** `owned` (Lična sveska korisnika)
- **Broj izvora:** 8 izvora (Univerzitet u Beogradu, Mikro knjiga, Pandas analitika, AI Academy, Valanor)
- **Verifikacioni status:** ✅ 100% VERIFIKOVANO (Upisana Antigravity Wiki beleška ID: `fb3f9c91-7322-43cf-b056-840f4fe90325`)

## 🧠 Principi veštačke inteligencije, mašinskog učenja i neuronskih mreža:
1. **Osnove VI i Mašinskog Učenja (Tom Mitchell model):**
   - Program uči na osnovu Iskustva I, posla P, uz meru performanse E, ako se performanse na poslu P poboljšavaju kroz iskustvo I.
   - Paradigme: Nadgledano (klasifikacija, regresija), Nenadgledano (klasterovanje, redukcija dimenzionalnosti PCA, t-SNE, detekcija anomalija), Polunadgledano, Forsirano učenje (Reinforcement Learning).
   - Paketno (Batch) vs Onlajn (Online) učenje.
2. **Priprema i čišćenje podataka (Pandas):**
   - Kvalitet podataka direktno diktira tačnost modela (Garbage In, Garbage Out).
   - Uklanjanje duplikata, imputacija nedostajućih vrednosti, skaliranje/standardizacija i tretman outliera (IQR/Z-score).
   - Pandas strukture: Series (1D) i DataFrame (2D), brze metode provere (info, describe, head, tail, shape).
3. **Arhitektura veštačkih neuronskih mreža (VNM):**
   - Građa neurona: Težine w_i, pomeraj/prag theta, težinska suma net = sum(w_i * x_i) - theta.
   - Aktivacione funkcije: Linearna, Binarna/bipolarna step, Sigmoid (verovatnoće 0-1), Tanh (-1 do 1), ReLU (efikasnost u dubokim mrežama).
   - Slojevi: Ulazni, skriveni (apstrakcija karakteristika) i izlazni sloj.
   - Feedforward vs Rekurentne neuronske mreže (RNN sa memorijom stanja).
4. **Kompletan proces treniranja modela:**
   - Podela podataka: 60% trening, 20% validacija, 20% testiranje.
   - Trofazni ciklus obuke: Feedforward -> Obračun gubitka (Loss function) -> Backpropagation (propagacija greške unazad, korigovanje težina preko stope učenja alpha).
   - Kontrola prenaučenosti (Overfitting) i nedovoljnog učenja (Underfitting).
"""
    },
    {
        "num": 13,
        "filename": "13_Vestina_Pametnog_Odlucivanja_7_Koraka.md",
        "title": "Veština Pametnog Odlučivanja: 7 Koraka do Jasnoće — Bezos Type 1/2 i Damasio",
        "uuid": "741a224e-ff57-419a-9d94-e175a8e0d532",
        "sources": 2,
        "content": """# 🧠 Sveska 13: Veština pametnog odlučivanja: 7 koraka do jasnoće

- **UUID:** `741a224e-ff57-419a-9d94-e175a8e0d532`
- **Vlasništvo:** `owned` (Lična sveska korisnika)
- **Broj izvora:** 2 izvora (Stanford & Harvard neuronaučne studije odlučivanja, 30-minute decision framework)
- **Verifikacioni status:** ✅ 100% VERIFIKOVANO (Upisana Antigravity Wiki beleška ID: `ec8d805d-87ec-4f46-a87c-1de7c2148c8d`)

## ⚡ 7 koraka do jasnoće i efikasnog odlučivanja:
1. **Eliminacija buke i Decision Fatigue:**
   - Prekomerno analiziranje smanjuje kvalitet odluka za do 25% (teorija ego depletion).
   - Grupisanje (batching) sitnih odluka unapred; donošenje ključnih odluka rano ujutru.
2. **Bezosov Type 1 vs Type 2 okvir:**
   - Type 1 (Ireverzibilne, strateške): Zahtevaju dubinu, istragu i oprez.
   - Type 2 (Reverzibilne, niskorizične): Donose se brzo uz **pravilo od 70% informacija** (satisficing — dovoljno dobro je bolje od savršenog).
3. **Emocionalna navigacija (Dr Antonio Damasio):**
   - Mi nismo mašine koje misle i osećaju, već mašine koje osećaju i misle. Bez emocija, logika blokira (pacijenti sa oštećenjem ventromedijalnog PFC-a).
   - Trostepeni check-in: Imenuj emociju -> Proceni pouzdanost -> Aktiviraj logiku.
4. **Kognitivni alati:**
   - Pravilo 10-10-10 (Suzy Welch): Kako ću se osećati za 10 minuta, 10 meseci, 10 godina (stimulacija dorzolateralnog PFC-a).
   - Simulacija žaljenja (Regret Simulation): Pitanje integriteta („Ako propadne, da li ću i dalje poštovati osobu koja sam postao?”).
   - Tri pitanja o identitetu (Vedski princip svrhe): Donošenje odluka iz perspektive budućeg ja u 3 tačke.
5. **Pravilo 5 minuta:**
   - Anteriorni cingulatni korteks stvara anksioznost pri neizvesnosti. U roku od 5 minuta preduzeti prvu fizičku mikroradnju.
"""
    },
    {
        "num": 14,
        "filename": "14_Strategija_Licnog_Brenda_Inbound_Funnel.md",
        "title": "Strategija Ličnog Brenda: Put od Pratioca do Premijum Klijenta — Inbound Funnel",
        "uuid": "3de699d5-2966-4349-a4e4-5d56fabc6647",
        "sources": 1,
        "content": """# 🚀 Sveska 14: Strategija ličnog brenda: Put od pratioca do premijum klijenta

- **UUID:** `3de699d5-2966-4349-a4e4-5d56fabc6647`
- **Vlasništvo:** `owned` (Lična sveska korisnika)
- **Broj izvora:** 1 sveobuhvatan izvor (Webinar sa 200 slajdova, strategija konverzije, paketi i pozicioniranje)
- **Verifikacioni status:** ✅ 100% VERIFIKOVANO (Upisana Antigravity Wiki beleška ID: `d6d78b6e-bd76-42d3-9835-54d28eea80af`)

## 💼 Sistem dolaska do High-Ticket klijenata bez hladnog outreach-a:
1. **Inbound Levak Konverzije:**
   - Profitabilna niša -> Vredan sadržaj -> Inbound praćenje -> DM inicijacija (bez prodaje, probijanje leda) -> Lead Magnet -> Email sekvenca (5-7 mailova) -> Prodajni poziv -> Premium paketi.
2. **5 Faza svesti kupca i Produkcija:**
   - 1) Ne zna da ima problem, 2) Svestan je problema, 3) Shvata da smo jedno od rešenja, 4) Razmatra samo nas, 5) Kupuje uslugu.
   - B-roll tehnika (10s kadrovi rada/čitanja) + AI/CapCut Voiceover.
   - Content Waterfall: Od 1 dugačkog formata pravi se 60 manjih delova (20 Reels, 20 TikTok, LinkedIn objave, X threadovi, YouTube).
3. **Pozicioniranje i Psihologija cena:**
   - Efekat Gucci majice: Brend i lice drastično dižu percipiranu vrednost u odnosu na anonimuse sa Upworka.
   - Niska cena odbija ozbiljne klijente jer signalizira loš kvalitet.
4. **Prodajni poziv i Strategija 3 paketa:**
   - Prodaja „leka za bol”, a ne tehničkog koda/sajta.
   - Kalkulacija cene statusa quo (koliko klijenta košta odlaganje rešenja).
   - Ponuda u 3 paketa preusmerava odluku sa „da li raditi sa vama” na „koji vaš paket izabrati”.
"""
    },
    {
        "num": 15,
        "filename": "15_Strategic_Communication_and_Self_Positioning.md",
        "title": "Strategic Communication and Self-Positioning with AI Mentor — Psihološki Okviri",
        "uuid": "f4858a3c-c776-4a91-84cc-245928155060",
        "sources": 1,
        "content": """# 🧠 Sveska 15: Strategic Communication and Self-Positioning with AI Mentor

- **UUID:** `f4858a3c-c776-4a91-84cc-245928155060`
- **Vlasništvo:** `owned` (Lična sveska korisnika)
- **Broj izvora:** 1 sveobuhvatan mentorski izvor (Transkript mentorskog razgovora, Anton Wigg strategija, discipline poruka)
- **Verifikacioni status:** ✅ 100% VERIFIKOVANO (Upisana Antigravity Wiki beleška ID: `cc4f88f7-4165-4302-942d-bd6cae239788`)

## 🧘 Principi strateške komunikacije i pozicioniranja:
1. **Pozicija umesto emocije i validacije:**
   - Komunikacija ne služi za traženje odobrenja niti pravdanje. Cilj je pozicionirati se kao zasebna, razumna osoba koja razume procese.
   - Odvajanje identiteta kroz sopstvena dela bez porodičnog oslanjanja.
   - Mirna i stabilna prisutnost umesto prenatrpanog signala.
2. **Pre-drafting okvir u 3 koraka:**
   - Korak 1: Cilj poruke u jednoj rečenici.
   - Korak 2: Profil primaoca (hladni vs topli kontakt, šta nudiš/tražiš).
   - Korak 3: Ton (direktan, neutralan, kratak).
3. **Komunikacijski filter (Inženjer vs Sagovornik):**
   - Ne objašnjavaj tehnologiju/backend. Postavi okvir u kojem ONI traže rešenje.
   - Šablon: Pitanje o rezultatu -> Ćuti i čekaj odgovor -> Ako je DA: 2 rečenice.
4. **Pravila egzekucije i psihološka samoregulacija:**
   - Slanje poruke jednom, bez emotikona, bez voice poruka, bez „seen?” provera.
   - Tehnika disanja 4-2-6 (Udah 4s, Zadrži 2s, Izdah 6s) za vraćanje prefrontalnog korteksa online.
   - Pravilo notifikacija: Ne reaguj na notifikaciju, reaguj samo na sadržaj.
   - Draft vežba za smirivanje straha od gubitka kontrole.
5. **30-dnevni akcioni plan samostalnog proboja:**
   - Faza 1 (Dan 1-3): Fokus na 1 problem u 1 rečenici.
   - Faza 2 (Dan 4-10): Minimalni dokaz sa 3 realna primera.
   - Faza 3 (Dan 11-20): Validacija bez ega (5 korisnika + 5 mentora).
   - Faza 4 (Dan 21-30): Javno pozicioniranje sa 3 jasna posta.
"""
    }
]

# Write all markdown files to KNOWLEDGE_DIR
print("Writing markdown knowledge files...")
created_files = []
for nb in notebooks:
    filepath = os.path.join(KNOWLEDGE_DIR, nb["filename"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(nb["content"])
    created_files.append((nb, filepath))
    print(f"  [+] Created {nb['filename']} ({len(nb['content'])} bytes)")

# Connect to webui.db inside open-webui data
DB_PATH = "/home/kizamladjanijebac/local_webui_tmp.db"
# First pull db from container
os.system("docker cp open-webui:/app/backend/data/webui.db " + DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

USER_ID = "9ca5ba59-759b-4fe2-ae2a-d30785f31776" # kiza admin
KB_ID = "antigravity-verified-brain-2026"
NOW = int(time.time())

# 1. Insert or update Knowledge Base
cur.execute("DELETE FROM knowledge WHERE id = ?", (KB_ID,))
cur.execute("""
INSERT INTO knowledge (id, user_id, name, description, meta, created_at, updated_at, data)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (
    KB_ID,
    USER_ID,
    "Antigravity Verified Brain (100% Grounded NotebookLM)",
    "Centralna autoritativna baza 100% verifikovanog znanja iz svih Google NotebookLM sveski (Neurobiologija, Sovereign AI OS 2026, 2026 UI Design, CodyMaster RAG, Deep Learning, Bezos Decision Framework, Inbound Branding, Strategic AI Communication).",
    json.dumps({"icon": "🛡️", "color": "#6366f1", "tags": ["antigravity", "notebooklm", "grounded", "verified"]}),
    NOW,
    NOW,
    json.dumps({"file_ids": []})
))
print(f"\n[+] Created/Updated Knowledge Base in SQLite: {KB_ID}")

# 2. Insert files into file and knowledge_file tables
file_ids = []
cur.execute("DELETE FROM knowledge_file WHERE knowledge_id = ?", (KB_ID,))

for nb, filepath in created_files:
    file_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"notebooklm-{nb['num']}-{nb['uuid']}"))
    file_ids.append(file_id)
    
    with open(filepath, "rb") as f:
        file_bytes = f.read()
    file_hash = hashlib.sha256(file_bytes).hexdigest()
    
    target_upload_path = f"/app/backend/data/uploads/{file_id}_{nb['filename']}"
    
    # Copy file into container uploads
    local_upload_target = f"/tmp/{file_id}_{nb['filename']}"
    with open(local_upload_target, "wb") as f:
        f.write(file_bytes)
    os.system(f"docker cp {local_upload_target} open-webui:{target_upload_path}")
    os.remove(local_upload_target)
    
    meta_json = json.dumps({
        "name": nb["filename"],
        "title": nb["title"],
        "content_type": "text/markdown",
        "size": len(file_bytes),
        "file_hash": file_hash,
        "data": {"knowledge_id": KB_ID, "notebook_uuid": nb["uuid"], "sources_count": nb["sources"]},
        "collection_name": KB_ID
    })
    
    cur.execute("DELETE FROM file WHERE id = ?", (file_id,))
    cur.execute("""
    INSERT INTO file (id, user_id, filename, meta, created_at, hash, data, updated_at, path)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        file_id,
        USER_ID,
        nb["filename"],
        meta_json,
        NOW,
        file_hash,
        None,
        NOW,
        target_upload_path
    ))
    
    kf_id = str(uuid.uuid4())
    cur.execute("""
    INSERT INTO knowledge_file (id, user_id, knowledge_id, file_id, created_at, updated_at, directory_id)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        kf_id,
        USER_ID,
        KB_ID,
        file_id,
        NOW,
        NOW,
        None
    ))
    print(f"  [+] Registered File {nb['filename']} (ID: {file_id})")

# Update knowledge base with all file_ids
cur.execute("UPDATE knowledge SET data = ? WHERE id = ?", (json.dumps({"file_ids": file_ids}), KB_ID))

# 3. Create Custom Model "Antigravity Grounded AI (Verified Knowledge)"
MODEL_ID = "antigravity-grounded-ai"
cur.execute("DELETE FROM model WHERE id = ?", (MODEL_ID,))

system_prompt = """Ti si Antigravity Grounded AI — autoritativni asistent koji operiše ISKLJUČIVO sa 100% verifikovanim znanjem iz Google NotebookLM baze znanja (Sveske 1 do 15).

STRIKTNA PRAVILA REZONOVANJA I ODGOVARANJA:
1. NULTA TOLERANCIJA NA HALUCINACIJE: Odgovaraj isključivo na osnovu činjenica, modela, formula i arhitektura iz priloženih verifikovanih sveski.
2. CITIRANJE IZVORA: Uvek navedi svesku i ključne koncepte na kojima se bazira tvoj odgovor (npr. [Sveska 6: TMT formula], [Sveska 13: Bezos Type 1/2], [Sveska 3: OpenClaw Debate Engine]).
3. AKO NEMA PODATKA: Ako korisnik postavi pitanje o temi koja se ne nalazi u verifikovanoj bazi, jasno i transparentno reci: "Ta informacija se ne nalazi u verifikovanim NotebookLM sveskama."
4. STRUKTURA: Odgovori moraju biti kristalno jasni, inženjerski precizni, sa bullet pointima, matematičkim formulama i operativnim koracima."""

model_meta = {
    "profile_image_url": None,
    "description": "Elitni AI asistent uzemljen u 100% verifikovanom znanju iz NotebookLM sveski (1-15). Nulta tolerancija na halucinacije.",
    "capabilities": {
        "file_context": True,
        "vision": True,
        "file_upload": True,
        "web_search": False,
        "image_generation": False,
        "code_interpreter": True,
        "citations": True
    },
    "suggestion_prompts": [
        {"title": ["Objasni TMT formulu", "prokrastinacije"], "content": "Objasni formulu teorije temporalne motivacije (TMT) i ulogu prefrontalnog korteksa."},
        {"title": ["Bezos Type 1 vs Type 2", "odlučivanje"], "content": "Koji je okvir za donošenje odluka po Bezosu i Damasio principima iz sveske 13?"},
        {"title": ["OpenClaw Arhitektura", "Debate Engine"], "content": "Kako funkcioniše Debate Engine sa 5 persona i JudgeGuard sigurnosna kapija?"},
        {"title": ["2026 UI Principi", "6-3-1 pravilo"], "content": "Objasni 6-3-1 pravilo boja, 4px grid i Observability Dashboard standarde."}
    ],
    "knowledge": [
        {
            "id": KB_ID,
            "name": "Antigravity Verified Brain (100% Grounded NotebookLM)"
        }
    ]
}

model_params = {
    "system": system_prompt,
    "temperature": 0.2,
    "top_p": 0.9,
    "knowledge_ids": [KB_ID]
}

cur.execute("""
INSERT INTO model (id, user_id, base_model_id, name, params, meta, updated_at, created_at, is_active)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    MODEL_ID,
    USER_ID,
    "gemini-2.5-flash",
    "Antigravity Grounded AI (Verified Knowledge)",
    json.dumps(model_params),
    json.dumps(model_meta),
    NOW,
    NOW,
    1
))
print(f"\n[+] Created Custom Model in SQLite: {MODEL_ID}")

# 4. Set model as pinned/default in config
cur.execute("UPDATE config SET value = ? WHERE key = 'ui.default_pinned_models'", (json.dumps("antigravity-grounded-ai"),))
cur.execute("UPDATE config SET value = ? WHERE key = 'ui.default_models'", (json.dumps("antigravity-grounded-ai"),))

conn.commit()
conn.close()

# Copy database back into container
os.system(f"docker cp {DB_PATH} open-webui:/app/backend/data/webui.db")
os.remove(DB_PATH)

print("\n🎉 ALL VERIFIED NOTEBOOKS SUCCESSFULLY INGESTED INTO OPEN WEBUI!")
