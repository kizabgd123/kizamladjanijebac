# 🤖 Sveska 12: Duboko učenje i veštačka inteligencija: Vodič

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
