import streamlit as st
import random
import time

# --- 1. IPAD STYLING: FLOATING BACK BUTTON & KIOSK THEME ---
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
        padding: 10px 20px;
        font-size: 35px !important;
        font-weight: 900 !important;
        border-radius: 20px;
        border: 5px solid #1a202c;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.3);
        z-index: 1000;
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
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
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
        white-space: nowrap;
    }

    .btn-icon {
        font-size: 65px; 
        margin-right: 30px;
        flex-shrink: 0;
    }

    /* UI Cleanup: Hiding everything standard */
    header, footer, #MainMenu, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    .instruction-text {
        color: white;
        text-align: center;
        font-size: 40px;
        font-weight: 900;
        margin-bottom: 30px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .worksheet-preview {
        background-color: white;
        padding: 15px;
        border-radius: 30px;
        border: 8px solid #1a202c;
        margin-bottom: 20px;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.3);
    }
    
    .answer-box {
        background-color: #FFF;
        color: #1E3A8A;
        padding: 25px;
        border-radius: 20px;
        font-size: 35px;
        font-weight: 900;
        border: 5px solid #1E3A8A;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. NAVIGATION LOGIC ---
params = st.query_params
mode = params.get("mode", None)
animal = params.get("animal", None)
action = params.get("action", None)

# --- 3. FLOATING BACK BUTTON (Shows only when NOT on Home) ---
if mode is not None:
    st.markdown('<a href="/" class="floating-back" target="_self">🏠 BACK</a>', unsafe_allow_html=True)

# --- 4. HOME PAGE ---
if mode is None:
    st.markdown('<div class="kiosk-title">Current choice:</div>', unsafe_allow_html=True)
    st.markdown('<a href="/?mode=coloring" class="kiosk-link" target="_self"><span class="btn-icon">🎨</span> A. Color Sheet Maker</a>', unsafe_allow_html=True)
    st.markdown('<a href="/?mode=puzzle" class="kiosk-link" target="_self"><span class="btn-icon">🧩</span> B. Today\'s Puzzle</a>', unsafe_allow_html=True)
    st.markdown('<a href="/?mode=fact" class="kiosk-link" target="_self"><span class="btn-icon">💡</span> C. Fun Fact</a>', unsafe_allow_html=True)
    st.markdown('<a href="/?mode=math" class="kiosk-link" target="_self"><span class="btn-icon">➕</span> D. Math Magic</a>', unsafe_allow_html=True)

# --- 5. OPTION A: COLOR SHEET MAKER ---
elif mode == "coloring":
    if animal is None:
        st.markdown('<div class="instruction-text">Pick an animal!</div>', unsafe_allow_html=True)
        st.markdown('<a href="/?mode=coloring&animal=Lion" class="kiosk-link" target="_self"><span class="btn-icon">🦁</span> LION</a>', unsafe_allow_html=True)
        st.markdown('<a href="/?mode=coloring&animal=Elephant" class="kiosk-link" target="_self"><span class="btn-icon">🐘</span> ELEPHANT</a>', unsafe_allow_html=True)
        st.markdown('<a href="/?mode=coloring&animal=Giraffe" class="kiosk-link" target="_self"><span class="btn-icon">🦒</span> GIRAFFE</a>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="instruction-text">{animal} Worksheet</div>', unsafe_allow_html=True)
        animal_imgs = {
            "Lion": "http://googleusercontent.com/image_collection/image_retrieval/379734712510393884_0",
            "Elephant": "http://googleusercontent.com/image_collection/image_retrieval/379734712510393884_2",
            "Giraffe": "https://img.icons8.com/ios/500/giraffe.png"
        }
        st.markdown('<div class="worksheet-preview">', unsafe_allow_html=True)
        st.image(animal_imgs[animal], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f'<a href="/?mode=coloring&animal={animal}&action=print" class="kiosk-link" target="_self"><span class="btn-icon">🖨️</span> PRINT NOW</a>', unsafe_allow_html=True)
        if action == "print":
            st.toast("🖨️ Sending to printer...", icon="🤖")

# --- 6. OPTION B: TODAY'S PUZZLE ---
elif mode == "puzzle":
    st.markdown('<div class="instruction-text">🧩 Today\'s Riddle</div>', unsafe_allow_html=True)
    riddle_text = "What has hands but cannot clap?"
    answer_text = "Answer: A Clock! ⏰"
    st.markdown(f'<div class="answer-box">{riddle_text}</div>', unsafe_allow_html=True)
    if action == "reveal":
        st.markdown(f'<div class="answer-box" style="background-color:#FFD700;">{answer_text}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<a href="/?mode=puzzle&action=reveal" class="kiosk-link" target="_self"><span class="btn-icon">🔍</span> SHOW ANSWER</a>', unsafe_allow_html=True)

# --- 7. OPTION D: MATH MAGIC ---
elif mode == "math":
    st.markdown('<div class="instruction-text">➕ Math Magic!</div>', unsafe_allow_html=True)
    st.markdown('<div class="kiosk-title" style="font-size:80px !important;">5 + 5 = ?</div>', unsafe_allow_html=True)
    if action == "reveal":
        st.markdown('<div class="kiosk-title" style="font-size:100px !important; color:#FFD700;">10! 🌟</div>', unsafe_allow_html=True)
    else:
        st.markdown('<a href="/?mode=math&action=reveal" class="kiosk-link" target="_self"><span class="btn-icon">🤔</span> CHECK ANSWER</a>', unsafe_allow_html=True)

# --- 8. OPTION C: FUN FACT ---
elif mode == "fact":
    st.markdown('<div class="instruction-text">💡 Fun Fact!</div>', unsafe_allow_html=True)
    st.markdown('<div class="answer-box">Octopuses have three hearts! 🐙</div>', unsafe_allow_html=True)
