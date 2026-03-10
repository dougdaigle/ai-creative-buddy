import streamlit as st
import random
import time

# --- 1. IPAD STYLING: STABLE THEME & FLOATING BACK ---
st.set_page_config(page_title="My Creative Buddy", layout="centered")

st.markdown("""
    <style>
    /* Full Sky Blue Background */
    .stApp { background-color: #00BFFF; }
    
    /* THE FLOATING BACK BUTTON: Styled Streamlit Button */
    .floating-back-container {
        position: fixed;
        top: 20px;
        left: 20px;
        z-index: 9999;
    }
    
    .floating-back-container div.stButton > button {
        background-color: white !important;
        color: black !important;
        padding: 10px 20px !important;
        font-size: 25px !important;
        height: auto !important;
        min-height: 60px !important;
        width: auto !important;
        border-radius: 15px !important;
        border: 4px solid #1a202c !important;
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

    /* THE UNIVERSAL KIOSK BUTTON: White Box, Black Text */
    div.stButton > button {
        background-color: white !important;
        color: black !important;
        border-radius: 40px !important;
        border: 8px solid #1a202c !important;
        font-size: 42px !important;
        font-weight: 900 !important;
        min-height: 140px !important;
        width: 100% !important;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.4) !important;
        font-family: 'Arial Black', sans-serif !important;
        display: flex;
        justify-content: flex-start;
        padding-left: 40px !important;
        margin-bottom: 25px !important;
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

    .worksheet-preview {
        background-color: white;
        padding: 30px;
        border-radius: 10px;
        border: 8px solid #1a202c;
        margin-bottom: 30px;
        box-shadow: 0px 15px 30px rgba(0,0,0,0.5);
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

# --- 2. SESSION STATE (The Navigation Brain) ---
if 'mode' not in st.session_state: st.session_state.mode = None
if 'animal' not in st.session_state: st.session_state.animal = None
if 'reveal' not in st.session_state: st.session_state.reveal = False

# --- 3. FLOATING BACK BUTTON (Now a real functional button) ---
if st.session_state.mode:
    st.markdown('<div class="floating-back-container">', unsafe_allow_html=True)
    if st.button("🏠 BACK"):
        st.session_state.mode = None
        st.session_state.animal = None
        st.session_state.reveal = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. HOME PAGE ---
if st.session_state.mode is None:
    st.markdown('<div class="kiosk-title">Current choice:</div>', unsafe_allow_html=True)
    if st.button("🎨 A. Color Sheet Maker"):
        st.session_state.mode = "coloring"; st.rerun()
    if st.button("🧩 B. Today's Puzzle"):
        st.session_state.mode = "puzzle"; st.rerun()
    if st.button("💡 C. Fun Fact"):
        st.session_state.mode = "fact"; st.rerun()
    if st.button("➕ D. Math Magic"):
        st.session_state.mode = "math"; st.rerun()

# --- 5. OPTION A: COLOR SHEET MAKER ---
elif st.session_state.mode == "coloring":
    if not st.session_state.animal:
        st.markdown('<div class="instruction-text">Pick an animal!</div>', unsafe_allow_html=True)
        if st.button("🦁 LION"): st.session_state.animal = "Lion"; st.rerun()
        if st.button("🐘 ELEPHANT"): st.session_state.animal = "Elephant"; st.rerun()
        if st.button("🦒 GIRAFFE"): st.session_state.animal = "Giraffe"; st.rerun()
        if st.button("🦓 ZEBRA"): st.session_state.animal = "Zebra"; st.rerun()
        if st.button("🐒 MONKEY"): st.session_state.animal = "Monkey"; st.rerun()
    else:
        st.markdown(f'<div class="instruction-text">{st.session_state.animal} Color Sheet</div>', unsafe_allow_html=True)
        
        animal_imgs = {
            "Lion": "https://img.icons8.com/ios/500/lion.png",
            "Elephant": "https://img.icons8.com/ios/500/elephant.png",
            "Giraffe": "https://img.icons8.com/ios/500/giraffe.png",
            "Zebra": "https://img.icons8.com/ios/500/zebra.png",
            "Monkey": "https://img.icons8.com/ios/500/monkey.png"
        }
        
        st.markdown('<div class="worksheet-preview">', unsafe_allow_html=True)
        st.image(animal_imgs.get(st.session_state.animal, ""), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🖨️ PRINT NOW"):
            st.toast("🖨️ Printing...", icon="🤖")

# --- 6. OPTION B: TODAY'S PUZZLE ---
elif st.session_state.mode == "puzzle":
    st.markdown('<div class="instruction-text">🧩 Today\'s Riddle</div>', unsafe_allow_html=True)
    st.markdown('<div class="answer-box">What has hands but cannot clap?</div>', unsafe_allow_html=True)
    if st.session_state.reveal:
        st.markdown('<div class="answer-box" style="background-color:#FFD700;">Answer: A Clock! ⏰</div>', unsafe_allow_html=True)
    else:
        if st.button("🔍 SHOW ANSWER"):
            st.session_state.reveal = True; st.rerun()

# --- 7. OPTION D: MATH MAGIC ---
elif st.session_state.mode == "math":
    st.markdown('<div class="instruction-text">➕ Math Magic!</div>', unsafe_allow_html=True)
    st.markdown('<div class="answer-box" style="font-size:80px !important;">5 + 5 = ?</div>', unsafe_allow_html=True)
    if st.session_state.reveal:
        st.markdown('<div class="answer-box" style="background-color:#FFD700; font-size:80px !important;">10! 🌟</div>', unsafe_allow_html=True)
    else:
        if st.button("🤔 CHECK ANSWER"):
            st.session_state.reveal = True; st.rerun()

# --- 8. OPTION C: FUN FACT ---
elif st.session_state.mode == "fact":
    st.markdown('<div class="instruction-text">💡 Fun Fact!</div>', unsafe_allow_html=True)
    st.markdown('<div class="answer-box">Octopuses have three hearts and blue blood! 🐙</div>', unsafe_allow_html=True)
