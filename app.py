import streamlit as st
import random
import time

# --- 1. IPAD STYLING: FLOATING BACK & WORKSHEET PREVIEW ---
st.set_page_config(page_title="My Creative Buddy", layout="centered")

st.markdown("""
    <style>
    /* Full Sky Blue Background */
    .stApp { background-color: #00BFFF; }
    
    /* THE FLOATING BACK BUTTON: Fixed to Top-Left */
    .floating-back {
        position: fixed;
        top: 20px;
        left: 20px;
        background-color: white !important;
        color: black !important;
        text-decoration: none !important;
        padding: 12px 24px;
        font-size: 30px !important;
        font-weight: 900 !important;
        border-radius: 20px;
        border: 5px solid #1a202c;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.3);
        z-index: 9999;
        font-family: 'Arial Black', sans-serif;
    }

    .kiosk-title {
        color: white;
        text-align: center;
        font-size: 50px !important;
        font-weight: 900;
        margin-top: 20px;
        margin-bottom: 35px;
        font-family: 'Arial Black', sans-serif;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
    }

    /* THE UNIVERSAL KIOSK BUTTON */
    .kiosk-link {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        background-color: white !important;
        color: black !important;
        text-decoration: none !important;
        padding: 0 40px;
        font-size: 42px !important;
        font-weight: 900 !important;
        min-height: 140px !important;
        width: 100% !important;
        border-radius: 40px;
        border: 8px solid #1a202c;
        margin-bottom: 25px;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.4);
        font-family: 'Arial Black', sans-serif;
    }

    .btn-icon {
        font-size: 65px; 
        margin-right: 30px;
        flex-shrink: 0;
    }

    /* UI Cleanup */
    header, footer, #MainMenu, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    .instruction-text {
        color: white;
        text-align: center;
        font-size: 45px;
        font-weight: 900;
        margin-bottom: 30px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    /* WORKSHEET PREVIEW FRAME */
    .worksheet-preview {
        background-color: white;
        padding: 30px;
        border-radius: 10px;
        border: 8px solid #1a202c;
        margin-bottom: 30px;
        box-shadow: 0px 15px 30px rgba(0,0,0,0.5);
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .answer-box {
        background-color: #FFF;
        color: black;
        padding: 30px;
        border-radius: 30px;
        font-size: 40px;
        font-weight: 900;
        border: 8px solid #1a202c;
        margin-bottom: 25px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. NAVIGATION LOGIC ---
params = st.query_params
mode = params.get("mode")
animal = params.get("animal")
action = params.get("action")

# --- 3. FLOATING BACK BUTTON ---
if mode:
    st.markdown('<a href="/" class="floating-back" target="_self">🏠 BACK</a>', unsafe_allow_html=True)

# --- 4. HOME PAGE ---
if not mode:
    st.markdown('<div class="kiosk-title">Current choice:</div>', unsafe_allow_html=True)
    st.markdown('<a href="/?mode=coloring" class="kiosk-link" target="_self"><span class="btn-icon">🎨</span> A. Color Sheet Maker</a>', unsafe_allow_html=True)
    st.markdown('<a href="/?mode=puzzle" class="kiosk-link" target="_self"><span class="btn-icon">🧩</span> B. Today\'s Puzzle</a>', unsafe_allow_html=True)
    st.markdown('<a href="/?mode=fact" class="kiosk-link" target="_self"><span class="btn-icon">💡</span> C. Fun Fact</a>', unsafe_allow_html=True)
    st.markdown('<a href="/?mode=math" class="kiosk-link" target="_self"><span class="btn-icon">➕</span> D. Math Magic</a>', unsafe_allow_html=True)

# --- 5. OPTION A: COLOR SHEET MAKER ---
elif mode == "coloring":
    if not animal:
        st.markdown('<div class="instruction-text">Pick an animal!</div>', unsafe_allow_html=True)
        # Expanded Animal List using your style
        st.markdown('<a href="/?mode=coloring&animal=Dino" class="kiosk-link" target="_self"><span class="btn-icon">🦖</span> Dino</a>', unsafe_allow_html=True)
        st.markdown('<a href="/?mode=coloring&animal=Lion" class="kiosk-link" target="_self"><span class="btn-icon">🦁</span> Lion</a>', unsafe_allow_html=True)
        st.markdown('<a href="/?mode=coloring&animal=Elephant" class="kiosk-link" target="_self"><span class="btn-icon">🐘</span> Elephant</a>', unsafe_allow_html=True)
        st.markdown('<a href="/?mode=coloring&animal=Giraffe" class="kiosk-link" target="_self"><span class="btn-icon">🦒</span> Giraffe</a>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="instruction-text">{animal} Color Sheet</div>', unsafe_allow_html=True)
        
        # Images for the preview
        animal_imgs = {
            "Dino": "Dinosaur adventure in a prehistoric world.jpg",
            "Lion": "https://img.icons8.com/ios/500/lion.png",
            "Elephant": "https://img.icons8.com/ios/500/elephant.png",
            "Giraffe": "https://img.icons8.com/ios/500/giraffe.png"
        }
        
        st.markdown('<div class="worksheet-preview">', unsafe_allow_html=True)
        st.image(animal_imgs.get(animal), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown(f'<a href="/?mode=coloring&animal={animal}&action=print" class="kiosk-link" target="_self"><span class="btn-icon">🖨️</span> PRINT NOW</a>', unsafe_allow_html=True)
        
        if action == "print":
            st.toast("🖨️ Sending to printer...", icon="🤖")
            st.success("Success! Pick up your page at the desk.")

# --- 6. OPTION B: TODAY'S PUZZLE ---
elif mode == "puzzle":
    st.markdown('<div class="instruction-text">🧩 Today\'s Riddle</div>', unsafe_allow_html=True)
    st.markdown('<div class="answer-box">What has hands but cannot clap?</div>', unsafe_allow_html=True)
    
    if action == "reveal":
        st.markdown('<div class="answer-box" style="background-color:#FFD700;">Answer: A Clock! ⏰</div>', unsafe_allow_html=True)
    else:
        st.markdown('<a href="/?mode=puzzle&action=reveal" class="kiosk-link" target="_self"><span class="btn-icon">🔍</span> SHOW ANSWER</a>', unsafe_allow_html=True)

# --- 7. OPTION D: MATH MAGIC ---
elif mode == "math":
    st.markdown('<div class="instruction-text">➕ Math Magic!</div>', unsafe_allow_html=True)
    st.markdown('<div class="answer-box" style="font-size:80px !important;">5 + 5 = ?</div>', unsafe_allow_html=True)
    
    if action == "reveal":
        st.markdown('<div class="answer-box" style="background-color:#FFD700; font-size:80px !important;">10! 🌟</div>', unsafe_allow_html=True)
    else:
        st.markdown('<a href="/?mode=math&action=reveal" class="kiosk-link" target="_self"><span class="btn-icon">🤔</span> CHECK ANSWER</a>', unsafe_allow_html=True)

# --- 8. OPTION C: FUN FACT ---
elif mode == "fact":
    st.markdown('<div class="instruction-text">💡 Fun Fact!</div>', unsafe_allow_html=True)
    st.markdown('<div class="answer-box">Octopuses have three hearts and blue blood! 🐙</div>', unsafe_allow_html=True)
