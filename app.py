import streamlit as st
import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont
import io

# Setup Page
st.set_page_config(
    page_title="RoastMyProfile - Carica e Roasta",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- IMAGE GENERATION FUNCTION ---
def create_share_image(text):
    """Create a shareable image with the roast text"""
    # Image dimensions
    width, height = 600, 400
    
    # Create white background
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw red border (thick, "Critical Error" style)
    border_width = 15
    draw.rectangle([0, 0, width-1, height-1], outline='#dc2626', width=border_width)
    
    # Inner red line
    draw.rectangle([border_width+5, border_width+5, width-border_width-6, height-border_width-6], outline='#dc2626', width=3)
    
    # Title bar
    draw.rectangle([border_width+10, border_width+10, width-border_width-11, border_width+40], fill='#dc2626')
    
    # Try to use a monospace font, fallback to default
    try:
        title_font = ImageFont.truetype("arial.ttf", 16)
        text_font = ImageFont.truetype("arial.ttf", 18)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
    
    # Title text
    draw.text((border_width+20, border_width+15), "⚠️ ROASTAMI - CRITICO", fill='white', font=title_font)
    
    # Wrap text to fit
    max_chars_per_line = 40
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 <= max_chars_per_line:
            current_line += (" " if current_line else "") + word
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    
    # Draw roast text
    y_position = border_width + 60
    for line in lines[:8]:  # Max 8 lines
        draw.text((border_width+20, y_position), line, fill='black', font=text_font)
        y_position += 28
    
    # Footer
    draw.text((border_width+20, height-border_width-35), "> Suggerimento: Cancella l'account.", fill='#dc2626', font=text_font)
    
    # Convert to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes.getvalue()

# --- CSS & HEAD INJECTION ---
st.markdown("""
<!-- Tailwind & Fonts -->
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet" />
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;700&family=VT323&display=swap" rel="stylesheet" />

<!-- Force Dark Mode -->
<script>
document.documentElement.classList.add('dark');
</script>

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
    background-color: #120821 !important; /* FORCE dark background */
    min-height: 100vh;
    border-left: 2px solid rgba(255, 255, 255, 0.1);
    border-right: 2px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); /* shadow-2xl */
    position: relative;
    z-index: 10;
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

# HEADER & MARQUEE (With inline styles for Streamlit compatibility)
st.markdown("""
<header style="background-color: #120821; padding: 16px; border-bottom: 4px solid #38ff14;">
<div style="display: flex; align-items: center; justify-content: space-between;">
<span class="material-symbols-outlined" style="color: #38ff14; font-size: 2rem; animation: pulse 1.5s infinite;">skull</span>
<h1 style="font-size: 1.875rem; font-weight: 900; letter-spacing: -0.05em; color: white; font-style: italic; font-family: 'Space Grotesk', sans-serif;">ROASTAMI 💀</h1>
<div style="width: 32px;"></div>
</div>
</header>
<div style="background-color: #38ff14; border-bottom: 4px solid black; overflow: hidden; padding: 8px 0; white-space: nowrap; position: relative;">
<div style="display: inline-block; animation: marquee 10s linear infinite;">
<span style="color: black; font-family: 'VT323', monospace; font-weight: bold; font-size: 1.25rem; padding: 0 16px; text-transform: uppercase; letter-spacing: 0.1em;">⚠️ ATTENZIONE: DANNO EMOTIVO IMMINENTE ⚠️ NON APRIRE SE SEI SENSIBILE ⚠️ CRINGE LEVEL: CRITICAL ⚠️</span>
</div>
</div>
""", unsafe_allow_html=True)

# Main Content Wrapper
st.markdown('<main style="flex: 1; display: flex; flex-direction: column; padding: 16px; gap: 24px;">', unsafe_allow_html=True)

# HERO UPLOAD ZONE (With inline styles)
st.markdown("""
<style>
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
@keyframes marquee {
  0% { transform: translateX(100%); }
  100% { transform: translateX(-100%); }
}
.upload-container {
  position: relative;
  width: 100%;
  height: 280px;
  margin-bottom: -280px;
  z-index: 1;
  margin-top: 8px;
}
[data-testid="stFileUploader"] {
  position: relative;
  z-index: 99;
  opacity: 0;
  height: 280px;
}
[data-testid="stFileUploader"] section {
  height: 280px;
  padding: 0;
}
[data-testid="stFileUploader"] div[role="button"] {
  height: 280px;
  width: 100%;
}
</style>

<div class="upload-container">
<div style="position: relative; margin-top: 8px;">
<div style="position: absolute; top: -12px; right: -12px; z-index: 20; transform: rotate(12deg); font-size: 2rem; filter: drop-shadow(2px 2px 2px rgba(0,0,0,0.3));">😂</div>
<div style="position: absolute; bottom: -16px; left: -8px; z-index: 20; transform: rotate(-12deg); font-size: 2rem; filter: drop-shadow(2px 2px 2px rgba(0,0,0,0.3));">🔥</div>
<div style="position: relative; background-color: rgba(0,0,0,0.4); border: 4px dashed #38ff14; border-radius: 12px; padding: 32px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 16px; cursor: pointer; overflow: hidden; box-shadow: 0 0 15px rgba(56,255,20,0.2); height: 260px;">
<div style="position: absolute; inset: 0; background-image: url('https://www.transparenttextures.com/patterns/diagmonds-light.png'); opacity: 0.1; pointer-events: none;"></div>
<div style="background-color: #2d1b4e; border-radius: 9999px; padding: 16px; border: 2px solid #38ff14; box-shadow: 0 0 10px #38ff14, 0 0 20px #38ff14; animation: pulse 1.5s infinite;">
<span class="material-symbols-outlined" style="color: #38ff14; font-size: 3rem;">cloud_upload</span>
</div>
<div style="text-align: center; z-index: 10;">
<h2 style="color: white; font-weight: 900; font-size: 1.5rem; text-transform: uppercase; letter-spacing: -0.025em; margin-bottom: 4px; filter: drop-shadow(2px 2px 2px rgba(0,0,0,0.5)); font-family: 'Space Grotesk', sans-serif;">Carica qui il tuo<br/><span style="color: #38ff14; font-size: 1.875rem; font-style: italic;">PROFILO CRINGE</span></h2>
<p style="color: #d1d5db; font-family: 'VT323', monospace; font-size: 0.875rem; margin-top: 8px; background-color: rgba(0,0,0,0.5); display: inline-block; padding: 4px 8px; border-radius: 4px;">Scanner radioattivo pronto.</p>
</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

# --- GEMINI API CONFIG ---
MODEL_NAME = "gemini-2.5-flash"  # Modello disponibile

# Get API Key from secrets
if "GEMINI_API_KEY" not in st.secrets:
    st.error("🔐 API Key mancante! Aggiungi GEMINI_API_KEY in .streamlit/secrets.toml")
    st.stop()

api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel(MODEL_NAME)

# Streamlit Uploader
uploaded_file = st.file_uploader("Scegli un'immagine", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed", key="img_uploader")

if uploaded_file is not None:
    # 5. LOADING STATE (Simulated Visual)
    loading_placeholder = st.empty()
    loading_placeholder.markdown("""
<div style="display: flex; flex-direction: column; gap: 8px; margin-top: 16px;">
<div style="display: flex; justify-content: space-between; align-items: flex-end;">
<label style="color: white; font-family: 'VT323', monospace; font-size: 1.125rem; animation: pulse 1.5s infinite;">STO CUCINANDO... 🔥</label>
<span style="color: #38ff14; font-family: 'VT323', monospace; font-size: 1.25rem;">0%</span>
</div>
<div style="height: 32px; width: 100%; background-color: black; border: 2px solid rgba(255,255,255,0.2); position: relative; overflow: hidden;">
<div style="position: absolute; top: 0; left: 0; height: 100%; background: linear-gradient(to right, #facc15, #f97316, #dc2626); width: 10%; box-shadow: 0 0 15px rgba(255,100,0,0.8);"></div>
</div>
<p style="font-size: 0.75rem; color: #00ffff; font-family: 'VT323', monospace; text-align: right;">Inizializzazione...</p>
</div>
""", unsafe_allow_html=True)

    try:
        # Load Image
        image = Image.open(uploaded_file)
            
        # Update Loading
        loading_placeholder.markdown("""
<div style="display: flex; flex-direction: column; gap: 8px; margin-top: 16px;">
<div style="display: flex; justify-content: space-between; align-items: flex-end;">
<label style="color: white; font-family: 'VT323', monospace; font-size: 1.125rem; animation: pulse 1.5s infinite;">ANALISI CRINGE... ☢️</label>
<span style="color: #38ff14; font-family: 'VT323', monospace; font-size: 1.25rem;">65%</span>
</div>
<div style="height: 32px; width: 100%; background-color: black; border: 2px solid rgba(255,255,255,0.2); position: relative; overflow: hidden;">
<div style="position: absolute; top: 0; left: 0; height: 100%; background: linear-gradient(to right, #facc15, #f97316, #dc2626); width: 65%; box-shadow: 0 0 15px rgba(255,100,0,0.8);"></div>
</div>
<p style="font-size: 0.75rem; color: #00ffff; font-family: 'VT323', monospace; text-align: right;">Giudicando le tue scelte di vita...</p>
</div>
""", unsafe_allow_html=True)

        # Generate Roast with Gemini
        prompt = """Sei un comico crudele della Gen Z. Analizza la foto profilo. Fai un roast (insulto satirico) in italiano slang (bro, cringe, amo, red flag). Massimo 3 frasi taglienti. Voto finale da 1 a 10."""
        
        # Generate content
        response = model.generate_content([prompt, image])
        roast_text = response.text
        
        # Save to session state for download button
        st.session_state["last_roast"] = roast_text
        
        # Remove loading bar
        loading_placeholder.empty()

        # 6. RESULT BOX (Windows 95 style with inline CSS)
        st.markdown(f"""
<div style="position: relative; margin-top: 16px;">
<!-- Windows 95 Title Bar -->
<div style="background-color: #c0c0c0; border: 2px solid; border-color: #ffffff #808080 #808080 #ffffff; display: flex; justify-content: space-between; align-items: center; padding: 4px 8px;">
<div style="display: flex; align-items: center; gap: 8px;">
<span class="material-symbols-outlined" style="color: #dc2626; font-size: 14px; font-weight: bold;">error</span>
<span style="color: black; font-weight: bold; font-family: sans-serif; font-size: 12px;">system_error.exe</span>
</div>
<div style="display: flex; gap: 4px;">
<div style="width: 16px; height: 16px; background-color: #c0c0c0; border: 1px solid #808080; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: bold; color: black;">_</div>
<div style="width: 16px; height: 16px; background-color: #c0c0c0; border: 1px solid #808080; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: bold; color: black;">□</div>
<div style="width: 16px; height: 16px; background-color: #dc2626; border: 1px solid #808080; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: bold; color: white;">×</div>
</div>
</div>
<!-- Windows 95 Body -->
<div style="background-color: #e0e0e0; border: 2px solid; border-color: #808080 #ffffff #ffffff #808080; padding: 16px;">
<div style="background-color: white; border: 2px solid; border-color: #000000 #c0c0c0 #c0c0c0 #000000; padding: 16px; font-family: 'VT323', monospace; font-size: 1.25rem; line-height: 1.5; color: black; min-height: 120px;">
<span style="background-color: #dc2626; color: white; padding: 2px 6px; font-weight: bold; font-size: 14px; margin-bottom: 8px; display: inline-block;">⚠️ CRITICO</span>
<p style="margin-top: 12px;">{roast_text}</p>
<p style="margin-top: 16px; color: #666;">&gt; Suggerimento: <span style="color: #dc2626; font-weight: bold;">Cancella l'account.</span></p>
</div>
</div>
</div>
""", unsafe_allow_html=True)
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            st.error("🔥 Troppa gente vuole essere insultata! Riprova tra qualche secondo.")
        elif "404" in error_msg:
            st.error(f"⚠️ Errore 404: {error_msg}")
        else:
            st.error(f"Errore durante il roast: {e}")

# Action Buttons (Always visible at bottom)
col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 NE VOGLIO ANCORA", use_container_width=True, type="primary"):
        # Just rerun the app to reset
        st.rerun()

with col2:
    # Download button for sharing (only show if roast exists)
    if "last_roast" in st.session_state and st.session_state["last_roast"]:
        share_image = create_share_image(st.session_state["last_roast"])
        st.download_button(
            label="💾 SCARICA PER I SOCIAL",
            data=share_image,
            file_name="roast.png",
            mime="image/png",
            use_container_width=True
        )
    else:
        if st.button("📸 CONDIVIDI", use_container_width=True):
            st.toast("🔥 Carica prima un'immagine per generare un roast!", icon="⚠️")

# Ko-fi Donation Button
st.markdown("""
<div style="text-align: center; margin-top: 24px; padding: 16px;">
<a href="https://ko-fi.com/giuseppecodice" target="_blank" style="display: inline-block; background-color: #FFDD00; color: black; font-weight: bold; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-family: 'Space Grotesk', sans-serif; font-size: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.3); transition: transform 0.2s;">
☕ OFFRIMI UN CAFFÈ
</a>
<p style="color: #888; font-size: 0.75rem; margin-top: 8px;">Se ti ho fatto ridere, supporta il progetto!</p>
</div>
""", unsafe_allow_html=True)

# Close Main Wrapper
st.markdown('</main>', unsafe_allow_html=True)
