# 💀 ROASTAMI PRO - Viral Web App Specification
> Documento tecnico per migrazione a Vertex AI (Produzione)

## 1. Obiettivo del Progetto
Trasformare l'attuale prototipo in una Web App di produzione stabile, eliminando i limiti di quota (Error 429). L'app deve analizzare foto profilo e generare "roast" (insulti comici) virali.

## 2. Architettura Tecnica (Vertex AI Migration)
L'app NON deve più usare `google.generativeai` (API Key gratuita).
Deve passare alla libreria professionale `vertexai` collegata al progetto Google Cloud.

* **Libreria Python:** `google-cloud-aiplatform` (importare come `vertexai`).
* **Modello:** `gemini-1.5-flash-001` (versione stabile su Vertex).
* **Regione:** `us-central1` (o `europe-west1` se preferito).
* **Autenticazione:** Utilizzare le credenziali di default di Google Cloud (`ADC`).

## 3. Design System (UI/UX) - "Gen Z Chaos"
Mantenere rigorosamente l'estetica virale esistente:
* **Tema:** Cyberpunk / Glitch / Y2K.
* **Colori:** Sfondo `#1A0B2E` (Viola scuro), Accenti `#39FF14` (Verde Neon) e `#FF00FF` (Magenta).
* **Elementi Chiave:**
    * Header con effetto glitch "ROASTAMI".
    * Marquee scorrevole di avvertimento.
    * Zona Upload stile "Scanner Radioattivo".
    * Box Risultato stile finestra di errore Windows 95.

## 4. Logica Funzionale (Step-by-Step)
1.  **Init:** Inizializzare Vertex AI all'avvio:
    ```python
    import vertexai
    from vertexai.generative_models import GenerativeModel
    # L'ID progetto verrà preso dall'ambiente o impostato manualmente
    vertexai.init(location="us-central1")
    ```
2.  **Input:** Utente carica foto (JPG/PNG).
3.  **Process:**
    * Mostrare barra di caricamento "STO CUCINANDO... 🔥".
    * Inviare l'immagine al modello `gemini-1.5-flash-001`.
4.  **Prompt di Sistema (Persona):**
    "Sei un comico crudele della Gen Z. Analizza la foto profilo. Fai un roast (insulto satirico) in italiano slang (bro, cringe, amo, red flag). Massimo 3 frasi taglienti. Voto finale da 1 a 10."
5.  **Output:** Mostrare il testo nel box grafico senza errori di quota.

## 5. Gestione Errori
* Se l'autenticazione fallisce, mostrare un messaggio chiaro: "Esegui 'gcloud auth application-default login' nel terminale".
* Bloccare file non immagine prima dell'invio.