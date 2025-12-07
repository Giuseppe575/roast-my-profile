# 💀 ROASTAMI - Development Report

## Panoramica Progetto
Web App virale dove gli utenti caricano screenshot dei loro profili e ricevono roast comici generati dall'AI in slang italiano Gen Z.

**Deploy:** Streamlit Cloud  
**Repository:** `roast-my-profile`  
**Modello AI:** `gemini-2.5-flash` (Google AI Studio API)

---

## Funzionalità Implementate

### 1. Design UI (Stile Cyberpunk/Y2K)
- Header con effetto glitch "ROASTAMI 💀"
- Marquee scorrevole con avvertimento
- Zona Upload con bordo verde neon tratteggiato
- Result Box stile Windows 95
- Layout mobile-first (max-width 420px)
- CSS inline per compatibilità Streamlit

### 2. Integrazione AI
- **Provider:** Google Generative AI (`google-generativeai`)
- **Modello:** `gemini-2.5-flash`
- **API Key:** In `.streamlit/secrets.toml`
- **Prompt:** Comico Gen Z con slang italiano

### 3. Funzione Condivisione
- `create_share_image(text)` genera PNG 600x400px
- Bordo rosso stile "Errore Critico"
- Pulsante download: "💾 SCARICA PER I SOCIAL" → `roast.png`

### 4. Pulsante Donazioni Ko-fi
- Pulsante giallo: "☕ OFFRIMI UN CAFFÈ"
- Link: [ko-fi.com/giuseppecodice](https://ko-fi.com/giuseppecodice)

---

## Struttura File
```
rosastami/
├── app.py              # Applicazione Streamlit
├── requirements.txt    # Dipendenze
├── .streamlit/
│   └── secrets.toml    # API Key (gitignored)
├── md/
│   ├── roastami_specs.md
│   └── verification_checklist.md
└── SPECIFICHE_APP.md   # Specifiche tecniche
```

## Dipendenze
```
streamlit
google-generativeai
Pillow
```

---

## Decisioni Tecniche

| Problema | Soluzione |
|----------|-----------|
| Tailwind CSS non funziona in Streamlit | Sostituito con CSS inline |
| Errore 503 Vertex AI su Streamlit Cloud | Tornato a API Key auth |
| Errori 404 modelli | Usato `gemini-2.5-flash` |
| Funzionalità condivisione | PIL image generation + download button |

---

## Configurazione

### Streamlit Cloud Secrets
```toml
GEMINI_API_KEY = "la-tua-api-key"
```

### Sviluppo Locale
1. Crea `.streamlit/secrets.toml` con API key
2. Esegui: `streamlit run app.py`

---

## Miglioramenti Futuri
- [ ] Più stili/personaggi per i roast
- [ ] Integrazione social media diretta
- [ ] Display rate limiting
- [ ] Supporto multilingua
