import streamlit as st
import google.generativeai as genai
from PIL import Image

# Setup Page
st.set_page_config(
    page_title="RoastMyProfile - Carica e Roasta",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS & HEAD INJECTION ---
st.markdown("""
    <!-- Tailwind & Fonts -->
    <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet" />
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;700&family=VT323&display=swap" rel="stylesheet" />
    
    <script>
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    colors: {
                        "primary": "#38ff14", /* Electric Lime */
                        "secondary": "#ff00ff", /* Magenta */
                        "accent": "#00ffff", /* Cyan */
                        "danger": "#ff3333", /* Warning Red */
                        "background-light": "#f0f0f0", 
                        "background-dark": "#1a0b2e", /* Deep Void Purple */
                        "surface": "#2d1b4e",
                    },
                    fontFamily: {
                        "display": ["Space Grotesk", "sans-serif"],
                        "mono": ["VT323", "monospace"],
                    },
                    boxShadow: {
                        'neo': '4px 4px 0px 0px #000000',
                        'neo-sm': '2px 2px 0px 0px #000000',
                        'neo-lg': '8px 8px 0px 0px #000000',
                        'glow': '0 0 10px #38ff14, 0 0 20px #38ff14',
                    },
                    animation: {
                        'pulse-fast': 'pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                        'marquee': 'marquee 10s linear infinite',
                        'shake': 'shake 0.5s cubic-bezier(.36,.07,.19,.97) both',
                    },
                    keyframes: {
                        marquee: {
                            '0%': { transform: 'translateX(100%)' },
                            '100%': { transform: 'translateX(-100%)' }
                        },
                        shake: {
                            '10%, 90%': { transform: 'translate3d(-1px, 0, 0)' },
                            '20%, 80%': { transform: 'translate3d(2px, 0, 0)' },
                            '30%, 50%, 70%': { transform: 'translate3d(-4px, 0, 0)' },
                            '40%, 60%': { transform: 'translate3d(4px, 0, 0)' }
                        }
                    }
                },
            },
        }
    </script>

    <style>
        /* FORCE MOBILE LAYOUT */
        .block-container {
            max-width: 420px !important;
            padding: 0 !important;
            margin: 0 auto !important;
            background-color: #1a0b2e;
            min-height: 100vh;
            border-left: 1px solid #333;
            border-right: 1px solid #333;
        }

        /* Background Pattern */
        .stApp {
            background-color: #000; /* Dark background outside phone */
            background-image: radial-gradient(#1a0b2e 1px, #000 1px);
            background-size: 20px 20px;
        }

        /* Hide standard Streamlit elements */
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* FILE UPLOADER STYLING */
        [data-testid="stFileUploader"] {
            padding: 2rem;
            border: 4px dashed #38ff14 !important; /* Neon Green */
            background-color: rgba(0,0,0,0.3);
            border-radius: 12px;
            text-align: center;
        }
        [data-testid="stFileUploader"] section {
            background-color: transparent !important;
        }
        [data-testid="stFileUploader"] button {
            display: none; /* Hide the default button if possible, or style it */
        }
        /* Style the 'Browse files' button inside uploader if visible */
        [data-testid="stFileUploader"] button {
            background-color: #38ff14 !important;
            color: black !important;
            border: none !important;
            font-weight: bold !important;
        }

        /* BUTTON STYLING */
        /* Primary Button (Ne voglio ancora) */
        button[kind="primary"] {
            background-color: #38ff14 !important;
            color: black !important;
            border: 2px solid black !important;
            border-bottom: 6px solid black !important;
            border-right: 6px solid black !important;
            border-radius: 8px !important;
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 900 !important;
            text-transform: uppercase;
            font-size: 1.1rem !important;
            transition: all 0.1s;
        }
        button[kind="primary"]:active {
            transform: translate(4px, 4px);
            border-bottom: 2px solid black !important;
            border-right: 2px solid black !important;
        }

        /* Secondary Button (Condividi) */
        button[kind="secondary"] {
            background: linear-gradient(135deg, #ff00ff, #00ffff) !important;
            color: white !important;
            border: 2px solid black !important;
            border-bottom: 6px solid black !important;
            border-right: 6px solid black !important;
            border-radius: 8px !important;
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 900 !important;
            text-transform: uppercase;
            font-size: 1.1rem !important;
            text-shadow: 1px 1px 0 #000;
        }
        button[kind="secondary"]:active {
            transform: translate(4px, 4px);
            border-bottom: 2px solid black !important;
            border-right: 2px solid black !important;
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #1a0b2e;
        }
        ::-webkit-scrollbar-thumb {
            background: #38ff14;
            border-radius: 4px;
        }
    </style>
""", unsafe_allow_html=True)

# --- LAYOUT STRUCTURE ---

# Background Grid
st.markdown('<div class="fixed inset-0 pointer-events-none opacity-20 bg-grid-pattern z-0"></div>', unsafe_allow_html=True)

# Wrapper for the "Phone/App" view
st.markdown("""
<div class="relative z-10 flex flex-col min-h-screen max-w-md mx-auto border-x-0 sm:border-x-2 border-black dark:border-white/10 bg-background-light dark:bg-[#120821] shadow-2xl">
""", unsafe_allow_html=True)

# 1. HEADER
st.markdown("""
<header class="bg-[#120821] p-4 border-b-4 border-primary">
<div class="flex items-center justify-between">
<span class="material-symbols-outlined text-primary text-3xl animate-pulse">skull</span>
<h1 class="text-3xl font-black tracking-tighter text-white italic glitch-text" data-text="ROASTAMI 💀">
ROASTAMI 💀
</h1>
<div class="w-8"></div>
</div>
</header>
""", unsafe_allow_html=True)

# 2. MARQUEE
st.markdown("""
<div class="bg-primary border-b-4 border-black overflow-hidden py-2 whitespace-nowrap relative">
<div class="animate-marquee inline-block">
<span class="text-black font-mono font-bold text-xl px-4 uppercase tracking-widest">
⚠️ ATTENZIONE: DANNO EMOTIVO IMMINENTE ⚠️ NON APRIRE SE SEI SENSIBILE ⚠️ CRINGE LEVEL: CRITICAL ⚠️
</span>
</div>
</div>
""", unsafe_allow_html=True)

# 3. MAIN CONTENT START
st.markdown('<main class="flex-1 flex flex-col p-4 gap-6">', unsafe_allow_html=True)

# 4. HERO UPLOAD ZONE (Visual) + Functional Uploader
st.markdown("""
<div class="relative group mt-2">
<div class="absolute -top-3 -right-3 z-20 transform rotate-12 text-4xl drop-shadow-md">😂</div>
<div class="absolute -bottom-4 -left-2 z-20 transform -rotate-12 text-4xl drop-shadow-md">🔥</div>
<div class="text-center mb-4">
<h2 class="text-white font-black text-2xl uppercase tracking-tight mb-1 drop-shadow-md">
Carica qui il tuo<br><span class="text-primary text-3xl italic">PROFILO CRINGE</span>
</h2>
<p class="text-gray-300 font-mono text-sm mt-2 bg-black/50 inline-block px-2 py-1 rounded">
Scanner radioattivo pronto.
</p>
</div>
</div>
""", unsafe_allow_html=True)

# --- API KEY HANDLING ---
api_key = None
with st.expander("⚙️ Configurazione Avanzata", expanded=False):
    model_name = st.selectbox(
        "Seleziona Modello AI", 
        [
            "gemini-2.0-flash", 
            "gemini-2.0-flash-exp", 
            "gemini-exp-1206",
            "gemini-1.5-pro",
            "gemini-pro-latest",
            "gemini-1.5-flash",
            "gemini-1.5-flash-8b"
        ],
        index=0
    )
    user_api_key = st.text_input("Inserisci la tua Google Gemini API Key (opzionale se già configurata):", type="password")
    if user_api_key:
        api_key = user_api_key
    elif "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]

import time

# Streamlit Uploader
uploaded_file = st.file_uploader("Scegli un'immagine", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed", key="img_uploader")

if uploaded_file is not None:
    if not api_key:
        st.error("⚠️ Inserisci una API Key per procedere!")
    else:
        # 5. LOADING STATE (Simulated Visual)
        loading_placeholder = st.empty()
        loading_placeholder.markdown("""
<div class="flex flex-col gap-2 mt-4">
<div class="flex justify-between items-end">
<label class="text-white font-mono text-lg animate-pulse">STO CUCINANDO... 🔥</label>
<span class="text-primary font-mono text-xl">0%</span>
</div>
<div class="h-6 w-full bg-black border-2 border-white/20 rounded-none relative overflow-hidden">
<div class="absolute top-0 left-0 h-full bg-gradient-to-r from-primary via-yellow-400 to-red-500 w-[10%] border-r-2 border-white shadow-[0_0_10px_rgba(56,255,20,0.8)]">
<div class="w-full h-full bg-[linear-gradient(45deg,rgba(0,0,0,0.1)_25%,transparent_25%,transparent_50%,rgba(0,0,0,0.1)_50%,rgba(0,0,0,0.1)_75%,transparent_75%,transparent)] bg-[length:20px_20px]"></div>
</div>
</div>
<p class="text-xs text-accent font-mono text-right">Inizializzazione...</p>
</div>
""", unsafe_allow_html=True)

        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_name)
            
            # Load Image
            image = Image.open(uploaded_file)
            
            # Update Loading
            loading_placeholder.markdown("""
<div class="flex flex-col gap-2 mt-4">
<div class="flex justify-between items-end">
<label class="text-white font-mono text-lg animate-pulse">ANALISI CRINGE... ☢️</label>
<span class="text-primary font-mono text-xl">65%</span>
</div>
<div class="h-6 w-full bg-black border-2 border-white/20 rounded-none relative overflow-hidden">
<div class="absolute top-0 left-0 h-full bg-gradient-to-r from-primary via-yellow-400 to-red-500 w-[65%] border-r-2 border-white shadow-[0_0_10px_rgba(56,255,20,0.8)]">
<div class="w-full h-full bg-[linear-gradient(45deg,rgba(0,0,0,0.1)_25%,transparent_25%,transparent_50%,rgba(0,0,0,0.1)_50%,rgba(0,0,0,0.1)_75%,transparent_75%,transparent)] bg-[length:20px_20px]"></div>
</div>
</div>
<p class="text-xs text-accent font-mono text-right">Giudicando le tue scelte di vita...</p>
</div>
""", unsafe_allow_html=True)

            # Generate Roast with Retry Logic
            prompt = "Sei un comico della Gen Z. Analizza la foto profilo e fai un roast (insulto divertente) breve e brutale in italiano slang."
            
            retry_count = 0
            max_retries = 3
            roast_text = ""
            
            while retry_count < max_retries:
                try:
                    response = model.generate_content([prompt, image])
                    roast_text = response.text
                    break
                except Exception as e:
                    if "429" in str(e):
                        retry_count += 1
                        time.sleep(2 ** retry_count) # Exponential backoff: 2s, 4s, 8s
                        if retry_count == max_retries:
                            raise e
                    else:
                        raise e
            
            # Final Loading State
            loading_placeholder.empty() # Remove loading bar

            # 6. RESULT BOX
            st.markdown(f"""
<div class="relative mt-4">
<!-- Windows 95 Header -->
<div class="bg-gray-300 border-2 border-b-0 border-white border-r-gray-600 border-b-gray-600 border-l-white flex justify-between items-center px-2 py-1 select-none">
<div class="flex items-center gap-2">
<span class="material-symbols-outlined text-red-600 text-sm font-bold">error</span>
<span class="text-black font-bold font-sans text-xs tracking-wide">system_error.exe</span>
</div>
<div class="flex gap-1">
<div class="w-3 h-3 bg-gray-300 border border-gray-500 shadow-sm flex items-center justify-center text-[8px] font-bold pb-1 text-black">_</div>
<div class="w-3 h-3 bg-gray-300 border border-gray-500 shadow-sm flex items-center justify-center text-[8px] font-bold pb-1 text-black">□</div>
<div class="w-3 h-3 bg-red-600 border border-gray-500 shadow-sm flex items-center justify-center text-[8px] font-bold text-white leading-none">×</div>
</div>
</div>
<!-- Windows 95 Body -->
<div class="bg-gray-200 border-2 border-t-0 border-white border-l-gray-400 border-r-black border-b-black p-4 relative overflow-hidden group">
<div class="absolute inset-0 border-4 border-danger pointer-events-none opacity-50 mix-blend-multiply"></div>
<div class="relative z-10 flex flex-col gap-4">
<div class="bg-white border-2 border-gray-400 border-t-black border-l-black p-4 font-mono text-lg leading-snug text-black">
<span class="bg-red-600 text-white px-1 font-bold text-sm mb-2 inline-block">CRITICO</span>
<p>
{roast_text}
<br><br>
&gt; Suggerimento: <span class="text-red-600 font-bold">Cancella l'account.</span>
</p>
</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)
            
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg:
                st.error(f"⚠️ Errore 404: Il modello '{model_name}' non è stato trovato o non è supportato. Prova a selezionare un altro modello dal menu 'Configurazione Avanzata'.")
            elif "429" in error_msg:
                st.error("⚠️ Errore 429: Hai superato il limite di richieste. Prova a cambiare modello o attendi qualche minuto.")
            else:
                st.error(f"Errore durante il roast: {e}")

# Action Buttons (Always visible at bottom)
# Action Buttons (Functional)
col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 NE VOGLIO ANCORA", use_container_width=True, type="primary"):
        # Clear the uploader state to reset the app
        if "img_uploader" in st.session_state:
            st.session_state["img_uploader"] = None
        st.rerun()

with col2:
    if st.button("📤 CONDIVIDI", use_container_width=True):
        st.toast("🔥 Screenshotta e umiliati su Instagram!", icon="📸")


# Close Main and Wrapper
st.markdown("</main></div>", unsafe_allow_html=True)
