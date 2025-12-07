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
                "primary": "#38ff14","secondary": "#ff00ff","accent": "#00ffff","danger": "#ff3333","background-light": "#f0f0f0",
                "background-dark": "#1a0b2e","surface": "#2d1b4e",
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
                'glow-danger': '0 0 12px #ff3333, 0 0 24px #ff3333, 0 0 36px #ff00ff',
            },
            animation: {
                'pulse-fast': 'pulse 1s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'marquee': 'marquee 8s linear infinite',
                'shake': 'shake 0.4s cubic-bezier(.36,.07,.19,.97) both infinite',
                'glitch-scan': 'glitch-scan 2s steps(4, end) infinite',
                'fire-flicker': 'fire-flicker 1s linear infinite',
                'strobe': 'strobe 0.5s linear infinite',
                'typewriter': 'typewriter 4s steps(40, end)',
                'bounce-in': 'bounce-in 0.5s ease',
                'shake-hover': 'shake-hover 0.5s cubic-bezier(.36,.07,.19,.97) both',
            },
            keyframes: {
                marquee: {
                    '0%': { transform: 'translateX(100%)' },
                    '100%': { transform: 'translateX(-120%)' }
                },
                shake: {
                    '10%, 90%': { transform: 'translate3d(-1px, 0, 0) skewX(-2deg)' },
                    '20%, 80%': { transform: 'translate3d(2px, 0, 0) skewX(2deg)' },
                    '30%, 50%, 70%': { transform: 'translate3d(-4px, 0, 0) skewX(-1deg)' },
                    '40%, 60%': { transform: 'translate3d(4px, 0, 0) skewX(1deg)' }
                },
                "glitch-scan": {
                    "0%": { transform: "translate(0)" },
                    "10%": { transform: "translate(-5px, 5px) skewX(5deg)" },
                    "20%": { transform: "translate(5px, -5px) skewY(-5deg)" },
                    "30%": { transform: "translate(0)" },
                    "100%": { transform: "translate(0)" }
                },
                "fire-flicker": {
                    '0%, 100%': { opacity: 1, transform: 'scale(1)' },
                    '50%': { opacity: 0.8, transform: 'scale(1.05)' },
                },
                "strobe": {
                    '0%, 100%': { opacity: 1 },
                    '50%': { opacity: 0.2 },
                },
                "typewriter": {
                    from: { width: '0' },
                    to: { width: '100%' }
                },
                "bounce-in": {
                  '0%': { transform: 'scale(0.5)', opacity: '0'},
                  '50%': { transform: 'scale(1.1)'},
                  '100%': { transform: 'scale(1)', opacity: '1'}
                },
                'shake-hover': {
                    '10%, 90%': { transform: 'translate3d(-2px, 0, 0) rotate(-1deg)' },
                    '20%, 80%': { transform: 'translate3d(3px, 0, 0) rotate(1deg)' },
                    '30%, 50%, 70%': { transform: 'translate3d(-5px, 0, 0) rotate(2deg)' },
                    '40%, 60%': { transform: 'translate3d(5px, 0, 0) rotate(-2deg)' }
                },
            }
        },
    },
}
</script>

<style>
    /* FORCE MOBILE LAYOUT & WRAPPER STYLING */
    .block-container {
        max-width: 420px !important;
        padding: 0 !important;
        margin: 0 auto !important;
        background-color: #f0f0f0; /* background-light */
        min-height: 100vh;
        border-left: 2px solid black;
        border-right: 2px solid black;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); /* shadow-2xl */
        position: relative;
        z-index: 10;
    }
    
    /* Dark Mode Override for Wrapper */
    @media (prefers-color-scheme: dark) {
        .block-container {
            background-color: #120821;
            border-color: rgba(255, 255, 255, 0.1);
        }
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
    
    /* Custom Classes */
    .scrollbar-hide::-webkit-scrollbar { display: none; }
    .text-stroke { -webkit-text-stroke: 1px black; }
    .text-stroke-sm { -webkit-text-stroke: 0.5px black; }
    .bg-grid-pattern {
        background-image: radial-gradient(#4a3b69 1px, transparent 1px);
        background-size: 20px 20px;
    }
    .glitch-text { position: relative; animation: shake 0.3s steps(4, end) infinite; text-shadow: 0 0 5px #ff00ff, 0 0 10px #00ffff;}
    .glitch-text::before, .glitch-text::after {
        content: attr(data-text); position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    }
    .glitch-text::before {
        left: 2px; text-shadow: -2px 0 #ff00ff; clip: rect(44px, 450px, 56px, 0);
        animation: glitch-anim 2s infinite linear alternate-reverse;
    }
    .glitch-text::after {
        left: -2px; text-shadow: -2px 0 #00ffff; clip: rect(44px, 450px, 56px, 0);
        animation: glitch-anim2 3s infinite linear alternate-reverse;
    }
    @keyframes glitch-anim {
        0% { clip: rect(33px, 9999px, 11px, 0); transform: skew(0.5deg); }
        20% { clip: rect(89px, 9999px, 93px, 0); } 40% { clip: rect(12px, 9999px, 49px, 0); }
        60% { clip: rect(55px, 9999px, 18px, 0); transform: skew(-0.5deg); }
        80% { clip: rect(6px, 9999px, 34px, 0); } 100% { clip: rect(22px, 9999px, 67px, 0); }
    }
    @keyframes glitch-anim2 {
        0% { clip: rect(2px, 9999px, 86px, 0); } 20% { clip: rect(15px, 9999px, 2px, 0); }
        40% { clip: rect(54px, 9999px, 29px, 0); transform: skew(0.2deg); }
        60% { clip: rect(9px, 9999px, 98px, 0); } 80% { clip: rect(76px, 9999px, 12px, 0); }
        100% { clip: rect(34px, 9999px, 54px, 0); transform: skew(-0.2deg); }
    }
    .jagged-border { clip-path: polygon(0% 5%, 5% 0%, 12% 8%, 22% 2%, 30% 10%, 42% 4%, 50% 12%, 60% 3%, 70% 9%, 80% 1%, 90% 11%, 95% 4%, 100% 8%, 100% 95%, 94% 100%, 88% 94%, 78% 99%, 70% 91%, 58% 97%, 50% 90%, 40% 98%, 30% 90%, 20% 99%, 10% 93%, 5% 98%, 0% 94%);}
    .typewriter-text { overflow: hidden; white-space: nowrap; animation: typewriter 2.5s steps(60, end) 0.5s 1 normal both, blink-caret .75s step-end infinite;}
    @keyframes blink-caret { from, to { border-color: transparent } 50% { border-color: black; } }

    /* BUTTON STYLING OVERRIDES FOR STREAMLIT */
    button[kind="primary"] {
        clip-path: polygon(0% 5%, 5% 0%, 12% 8%, 22% 2%, 30% 10%, 42% 4%, 50% 12%, 60% 3%, 70% 9%, 80% 1%, 90% 11%, 95% 4%, 100% 8%, 100% 95%, 94% 100%, 88% 94%, 78% 99%, 70% 91%, 58% 97%, 50% 90%, 40% 98%, 30% 90%, 20% 99%, 10% 93%, 5% 98%, 0% 94%);
        background-color: #38ff14 !important;
        color: black !important;
        border: 2px solid black !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 900 !important;
        text-transform: uppercase;
        font-size: 1.2rem !important;
        padding: 1rem !important;
        transition: all 0.3s;
    }
    button[kind="primary"]:hover {
        transform: rotate(-1deg) scale(1.02);
    }
    
    button[kind="secondary"] {
        clip-path: polygon(0% 5%, 5% 0%, 12% 8%, 22% 2%, 30% 10%, 42% 4%, 50% 12%, 60% 3%, 70% 9%, 80% 1%, 90% 11%, 95% 4%, 100% 8%, 100% 95%, 94% 100%, 88% 94%, 78% 99%, 70% 91%, 58% 97%, 50% 90%, 40% 98%, 30% 90%, 20% 99%, 10% 93%, 5% 98%, 0% 94%);
        background: linear-gradient(135deg, #ff00ff, #00ffff) !important;
        color: white !important;
        border: 2px solid black !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 900 !important;
        text-transform: uppercase;
        font-size: 1.2rem !important;
        padding: 1rem !important;
        text-shadow: 1px 1px 0 #000;
    }
    button[kind="secondary"]:hover {
        transform: rotate(1deg) scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# --- LAYOUT STRUCTURE ---

# Background Grid
st.markdown('<div class="fixed inset-0 pointer-events-none opacity-20 bg-grid-pattern z-0"></div>', unsafe_allow_html=True)

# HEADER & MARQUEE (Consolidated)
st.markdown("""
<header class="bg-[#120821] p-4 border-b-4 border-primary">
<div class="flex items-center justify-center">
<h1 class="text-4xl font-black tracking-tighter text-white italic glitch-text" data-text="ROASTAMI 💀">ROASTAMI 💀</h1>
</div>
</header>
<div class="bg-primary border-b-4 border-black overflow-hidden py-2 whitespace-nowrap relative">
<div class="animate-marquee inline-block">
<span class="text-black font-mono font-bold text-2xl px-4 uppercase tracking-widest text-stroke-sm" style="text-shadow: 2px 2px 0 #ff00ff, -2px -2px 0 #00ffff;">⚠️ ATTENZIONE: DANNO EMOTIVO IMMINENTE ⚠️</span>
</div>
<div aria-hidden="true" class="animate-marquee inline-block">
<span class="text-black font-mono font-bold text-2xl px-4 uppercase tracking-widest text-stroke-sm" style="text-shadow: 2px 2px 0 #ff00ff, -2px -2px 0 #00ffff;">⚠️ CRINGE LEVEL: CRITICAL ⚠️</span>
</div>
</div>
""", unsafe_allow_html=True)

# 4. HERO UPLOAD ZONE (Visual + Functional Overlay)
# 4. HERO UPLOAD ZONE (Visual + Functional Overlay)
st.markdown("""
<style>
/* Container for the custom design */
.upload-container {
position: relative;
width: 100%;
height: 350px; /* Increased height for new design */
margin-bottom: -350px; /* Pull the next element (uploader) up */
z-index: 1;
}

/* Make the Streamlit uploader invisible but clickable */
[data-testid="stFileUploader"] {
position: relative;
z-index: 99;
opacity: 0;
height: 350px;
}
[data-testid="stFileUploader"] section {
height: 350px;
padding: 0;
}
[data-testid="stFileUploader"] div[role="button"] {
height: 350px;
width: 100%;
}
</style>

<div class="upload-container">
<!-- Custom Design from code.html -->
<div class="relative group mt-2 h-full">
<div class="absolute -top-6 -right-5 z-20 transform rotate-12 text-5xl animate-bounce-in drop-shadow-lg">😂</div>
<div class="absolute top-24 -left-6 z-20 transform -rotate-12 text-5xl animate-bounce-in drop-shadow-lg [animation-delay:0.2s]">☣️</div>
<div class="absolute -bottom-6 -left-4 z-20 transform rotate-6 text-5xl animate-bounce-in drop-shadow-lg [animation-delay:0.4s]">🤡</div>
<div class="absolute bottom-20 -right-7 z-20 transform -rotate-12 text-5xl animate-bounce-in drop-shadow-lg [animation-delay:0.6s]">🔥</div>

<div class="relative bg-black/20 dark:bg-black/40 border-8 border-dashed border-primary hover:border-secondary transition-colors duration-300 rounded-xl p-8 flex flex-col items-center justify-center gap-4 cursor-pointer overflow-hidden shadow-glow hover:shadow-[0_0_40px_rgba(255,0,255,0.8)] animate-pulse-fast h-full">
<div class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/diagmonds-light.png')] opacity-10 pointer-events-none animate-strobe"></div>

<div class="bg-surface rounded-full p-4 border-4 border-primary shadow-glow">
<span class="material-symbols-outlined text-primary text-6xl">cloud_upload</span>
</div>

<div class="text-center z-10">
<h2 class="text-white font-black text-3xl uppercase tracking-tight mb-1 drop-shadow-md text-stroke">Carica qui il tuo<br/><span class="text-primary text-4xl italic">PROFILO CRINGE</span></h2>
<p class="text-gray-300 font-mono text-base mt-2 bg-black/50 inline-block px-2 py-1 rounded">Scanner radioattivo pronto.</p>
</div>
</div>
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
<div class="h-8 w-full bg-black border-2 border-white/20 rounded-none relative overflow-hidden">
<div class="absolute inset-0 bg-gradient-to-t from-red-900/50 via-transparent to-transparent"></div>
<div class="absolute top-0 left-0 h-full bg-gradient-to-r from-yellow-400 via-orange-500 to-red-600 w-[10%] transition-all duration-1000 shadow-[0_0_15px_rgba(255,100,0,0.8)] animate-fire-flicker">
<div class="absolute -right-2 top-[-16px] text-4xl animate-fire-flicker">🔥</div>
<div class="w-full h-full bg-[linear-gradient(45deg,rgba(255,255,255,0.1)_25%,transparent_25%,transparent_50%,rgba(255,255,255,0.1)_50%,rgba(255,255,255,0.1)_75%,transparent_75%,transparent)] bg-[length:30px_30px] opacity-50"></div>
</div>
<div class="absolute inset-0" style="background-image: repeating-linear-gradient(0deg, transparent, transparent 1px, rgba(0,0,0,0.5) 1px, rgba(0,0,0,0.5) 2px);"></div>
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
<div class="h-8 w-full bg-black border-2 border-white/20 rounded-none relative overflow-hidden">
<div class="absolute inset-0 bg-gradient-to-t from-red-900/50 via-transparent to-transparent"></div>
<div class="absolute top-0 left-0 h-full bg-gradient-to-r from-yellow-400 via-orange-500 to-red-600 w-[65%] transition-all duration-1000 shadow-[0_0_15px_rgba(255,100,0,0.8)] animate-fire-flicker">
<div class="absolute -right-2 top-[-16px] text-4xl animate-fire-flicker">🔥</div>
<div class="w-full h-full bg-[linear-gradient(45deg,rgba(255,255,255,0.1)_25%,transparent_25%,transparent_50%,rgba(255,255,255,0.1)_50%,rgba(255,255,255,0.1)_75%,transparent_75%,transparent)] bg-[length:30px_30px] opacity-50"></div>
</div>
<div class="absolute inset-0" style="background-image: repeating-linear-gradient(0deg, transparent, transparent 1px, rgba(0,0,0,0.5) 1px, rgba(0,0,0,0.5) 2px);"></div>
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
<div class="relative mt-2 animate-shake">
<div class="absolute inset-0 border-8 border-danger pointer-events-none shadow-glow-danger rounded-sm"></div>
<div class="bg-gray-300 border-2 border-b-0 border-white border-r-gray-600 border-b-gray-600 border-l-white flex justify-between items-center px-2 py-1 select-none">
<div class="flex items-center gap-2">
<span class="material-symbols-outlined text-red-600 text-sm font-bold">error</span>
<span class="text-black font-bold font-sans text-xs tracking-wide">system_error.exe</span>
</div>
<div class="flex gap-1">
<div class="w-4 h-4 bg-gray-300 border border-gray-500 shadow-sm flex items-center justify-center text-xs font-bold pb-1 text-black">_</div>
<div class="w-4 h-4 bg-gray-300 border border-gray-500 shadow-sm flex items-center justify-center text-xs font-bold pb-1 text-black">□</div>
<div class="w-4 h-4 bg-red-600 border border-gray-500 shadow-sm flex items-center justify-center text-xs font-bold text-white leading-none">×</div>
</div>
</div>
<div class="bg-gray-200 border-2 border-t-0 border-white border-l-gray-400 border-r-black border-b-black p-4 relative overflow-hidden group">
<div class="relative z-10 flex flex-col gap-4">
<div class="bg-white border-2 border-gray-400 border-t-black border-l-black p-4 font-mono text-xl leading-snug text-black min-h-[160px]">
<span class="bg-red-600 text-white px-1 font-bold text-base mb-2 inline-block">CRITICO</span>
<p class="typewriter-text border-r-2 border-black">{roast_text} <br/><br/> &gt; Suggerimento: <span class="text-red-600 font-bold">Cancella l'account.</span></p>
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
# Close Main and Wrapper
# st.markdown("</main></div>", unsafe_allow_html=True) # Removed as we are not using open tags anymore
