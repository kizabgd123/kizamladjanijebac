# ❓ Sveska 9: Pomoć i Povratne Informacije za NotebookLM

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
