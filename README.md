# 🚀 Nexus Multi-Agent RAG Studio v2.0

> **Google Standard Autonomous AI Application**  
> Powered by Multi-Agent Orchestration, Live NotebookLM RAG Engine, ML Predictive Analytics, and Auto-App Configurator. Zero mock data – 100% End-to-End Real-Time Execution.

[![Build and Verify](https://github.com/kizabgd123/kizamladjanijebac/actions/workflows/publish.yml/badge.svg)](https://github.com/kizabgd123/kizamladjanijebac/actions/workflows/publish.yml)
[![Node.js Version](https://img.shields.io/badge/Node.js-%3E%3D18.0.0-brightgreen.svg)](https://nodejs.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## 📌 Pregled Projekta (Overview)

**Nexus Multi-Agent RAG Studio** je napredna web aplikacija izgrađena po najvišim Google inženjerskim standardima. Omogućava autonomnu orkestraciju više AI agenata i direktnu integraciju sa **Google NotebookLM** bazama znanja putem komandne linije (`nlm` CLI).

### Ključne Funkcionalnosti:
- 🤖 **Multi-Agent Orchestration Engine**: Četvoroslojni sistem agenata (Coordinator → RAG Engine → ML Classifier → Synthesizer) koji automatski analizira nameru korisnika, vrši pretragu i sastavlja odgovore.
- 📚 **Live NotebookLM RAG**: Odgovori se dobavljaju uživo iz više od 200 naučnih i stručnih izvora sa tačnim citatima i referencama (`[1]`, `[2]`, ...).
- 🧠 **Intent-Based Notebook Selection**: Pametna automatska selekcija najbolje sveske u zavisnosti od teme upita (Machine Learning, Agentic AI, NLP, Zavisnost).
- ⚡ **Auto-App & Chatbot Configurator**: Generiše i aktivira kognitivne četbot module u realnom vremenu na osnovu korisničkih zahteva.
- 📊 **Predictive Analytics**: Vizuelna analitika tačnosti sinhronizacije i latencije agenata pomoću Recharts grafikona.
- 📦 **Jedinstveni Produkcioni Start (`start.sh`)**: Jedna komanda za automatski build klijenta i pokretanje Node.js servera na portu `5000`.

---

## 🛠️ Zahtevi Sistema (Prerequisites)

Pre pokretanja na bilo kom računaru (Linux, macOS, Windows/WSL), proverite da li imate instalirano:

1. **Node.js**: `v18.0.0` ili noviji (`node -v`)
2. **npm**: `v9.0.0` ili noviji (`npm -v`)
3. **Python & uv** (Opciono za NotebookLM RAG):
   - Za uživo upite ka NotebookLM sveskama preporučuje se `notebooklm-mcp-cli`:
     ```bash
     pip install uv
     uv tool install notebooklm-mcp-cli
     nlm login
     ```
   - *Napomena:* Ukoliko `nlm` CLI nije instaliran ili prijavljen, server automatski prelazi na stabilan fallback sa ugrađenim modulima.

---

## 🚀 Uputstvo za Pokretanje sa Bilo Kog Računara

### 1. Klonirajte Repozitorijum

```bash
git clone https://github.com/kizabgd123/kizamladjanijebac.git
cd kizamladjanijebac
```

### 2. Instalirajte Zavisnosti

```bash
npm install
```

### 3. Pokrenite Aplikaciju (Jedna Komanda)

Izvršite pripremljenu pokretačku skriptu:

```bash
./start.sh
```

**Šta ova komanda automatski radi:**
1. Proverava i kompajlira produkcioni frontend bundle (`npm run build`).
2. Oslobađa port `5000` ukoliko je bio zauzet.
3. Pokreće Express Node.js backend koji istovremeno servira i API i statički web interfejs.

### 4. Otvorite u Pretraživaču

Otvorite veb pretraživač i idite na:

👉 **`http://localhost:5000`**

---

## 📂 Arhitektura Projekta (Project Structure)

```
.
├── .github/
│   └── workflows/
│       └── publish.yml      # GitHub Actions CI/CD pipeline za automatski build i verifikaciju
├── src/
│   ├── App.jsx              # Glavna React SPA aplikacija (Conversational AI, RAG Hub, ML, Configurator)
│   ├── main.jsx             # React entrypoint
│   └── index.css            # Tailwind CSS i moderni stilovi (Dark mode, Glassmorphism)
├── server.js                # Express backend & Multi-Agent Orchestrator (NLM CLI integracija)
├── start.sh                 # Produkciona skripta za automatsko pokretanje (chmod +x)
├── package.json             # Zavisnosti i npm skripte
├── vite.config.js           # Vite konfiguracija
├── tailwind.config.js       # Tailwind CSS konfiguracija
├── judge_guard.py           # Pre-Action verification guard (CodyMaster Orchestration Rule)
└── README.md                # Uputstvo i dokumentacija projekta
```

---

## 📡 API Dokumentacija (Endpoints)

| Metoda | Ruta | Opis |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Provera statusa sistema, verzije i NotebookLM CLI putanje |
| `GET` | `/api/user/profile` | Dobavljanje profila korisnika i istorije upita |
| `POST` | `/api/agents/orchestrate` | Glavni Multi-Agent RAG upit (izvršava `nlm notebook query -j`) |
| `GET` | `/api/notebooks` | Lista aktivnih NotebookLM svezaka |
| `POST` | `/api/notebooks/create` | Kreiranje nove NotebookLM sveske uživo |
| `GET` | `/api/modules` | Lista generisanih AI i četbot modula |
| `POST` | `/api/modules/:id/test` | Uživo testiranje specifičnog generisanog modula |
| `POST` | `/api/ml/predict` | Generisanje vremenskih serija i prediktivne analitike |

---

## 🤖 Multi-Agent Arhitektura (Kako Funkcioniše)

Sistem funkcioniše po **Reason → Act → Reflect → Verify (RARV)** principu:

```
[ Korisnički Upit ]
        │
        ▼
[ Agent-1: Coordinator ]  ──► Analizira kontekst i automatski bira bazu znanja
        │
        ▼
[ Agent-2: RAG Engine ]   ──► Poziva `nlm notebook query -j` na izabranoj svesci
        │
        ▼
[ Agent-3: ML Classifier ] ──► Prepoznaje nameru (npr. kreiranje četbota ili aplikacije)
        │
        ▼
[ Agent-4: Synthesizer ]  ──► Formira finalni strukturirani odgovor sa citatima
        │
        ▼
[ Odgovor + Integrisani Citati ]
```

---

## 🧪 Testiranje i Verifikacija (Quality Gate)

Možete ručno proveriti ispravnost koda i sintakse u bilo kom trenutku:

```bash
# Provera sintakse backend servera
npm test

# Provera build-a frontend aplikacije
npm run build
```

Svi `git push` komiti automatski pokreću **GitHub Actions** CI/CD pipeline koji verifikuje kompajliranje i generiše produkcione artefakte.

---

## 📜 Licenca i Standardi

Projekat je razvijen po **Google Agentic AI** standardima i **CodyMaster** sistemu kvaliteta (Zero-Stub Policy, Strict Verification Workflow).

*Autor:* [kizabgd123](https://github.com/kizabgd123)  
*Status:* **PRODUCTION READY (IT'S WORKING)** ✅
