# 💀 ROASTAMI - Viral AI Roasting App
> Documento di Specifiche Tecniche e Design

## 1. Concept del Progetto
Una Web App mobile-first virale dove gli utenti caricano uno screenshot del loro profilo social (Instagram, Tinder, LinkedIn) e ricevono un "Roast" (insulto satirico/comico) brutale generato dall'AI.

**Target:** Gen Z, utenti TikTok/Reels.
**Vibe:** Caotico, Y2K, Glitch, Cyberpunk, "Cringe Level Critical".

---

## 2. Flusso Utente (User Flow)
1.  **Landing:** L'utente apre il sito. Vede un logo glitchato e un marquee (testo scorrevole) di avvertimento.
2.  **Upload:** Trascina o seleziona una foto nell'area "Scanner Radioattivo".
3.  **Loading:** Parte un'animazione ("STO CUCINANDO... 🔥") mentre l'AI elabora.
4.  **Result:** Appare un box stile "Errore Windows 95" con il testo del roast.
5.  **Loop:** L'utente può cliccare "Ne voglio ancora" (reset) o "Condividi" (non funzionale per ora, solo UI).

---

## 3. Specifiche Tecniche (Tech Stack)

### Frontend & Backend
* **Framework:** Python + Streamlit.
* **Librerie Chiave:** `streamlit`, `google-generativeai`.
* **Deploy:** Google Antigravity / Cloud Run.

### Configurazione AI (Cruciale per stabilità)
Per evitare errori 404/429, usare rigorosamente queste impostazioni:
* **Provider:** Google Gemini API.
* **Modello Primario:** `models/gemini-1.5-flash-001` (Stabile, Veloce).
* **Modello Fallback:** `models/gemini-1.5-pro-latest` (Se il flash fallisce).
* **Gestione Errori:** Implementare un blocco `try-except` che cattura errori di quota e mostra un messaggio amichevole ("Troppa gente vuole essere insultata, riprova tra 10 secondi!").

---

## 4. Design System (UI/UX)
L'interfaccia deve replicare lo stile generato da Stitch/Google Design Agent.

* **Colori:**
    * Background: Viola Scuro Profondo (`#1A0B2E`)
    * Accento 1: Verde Lime Neon (`#39FF14`) - Per bordi e pulsanti primari.
    * Accento 2: Magenta Hot (`#FF00FF`) - Per effetti glitch.
    * Accento 3: Rosso Errore (`#FF0000`) - Per il box del risultato.
* **Tipografia:**
    * Titoli: Font futuristici/Allungati.
    * Testo AI: Font Monospace (tipo "Courier" o "VT323") pixelato.
* **Componenti Chiave:**
    * **Marquee:** Testo scorrevole in cima `⚠️ ATTENZIONE: DANNO EMOTIVO IMMINENTE ⚠️`.
    * **Scanner:** Area di upload con bordo tratteggiato verde neon pulsante.
    * **Result Box:** Deve sembrare una finestra di sistema crashata.

---

## 5. Logica del "Cervello" AI (System Prompt)
Questo è il prompt esatto da passare al modello Gemini. Non deve essere gentile.

**System Instruction:**
```text
Sei un comico della Generazione Z, sarcastico, spietato ma divertente.
Il tuo compito è guardare la foto profilo fornita e fare un "ROAST" (presa in giro).
REGOLE:
1. Usa slang italiano corrente (bro, cringe, amo, red flag, boomer, NPC).
2. Sii breve (massimo 3 frasi taglienti).
3. Non fare prediche morali.
4. Concentrati su dettagli visivi: vestiti, espressione, sfondo, qualità della foto.
5. Chiudi con un voto da 1 a 10 (es: "Voto: -2/10").
```
