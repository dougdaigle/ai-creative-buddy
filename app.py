import streamlit as st
import random

# --- 1. IPAD STYLING: REVERTED TO SKY BLUE & GIANT BLACK TEXT ---
st.set_page_config(page_title="My Creative Buddy", layout="centered")

st.markdown("""
    <style>
    /* Full Sky Blue Background */
    .stApp { background-color: #00BFFF; }
    
    /* THE FLOATING BACK BUTTON: Fixed to Top-Left */
    .floating-back-btn {
        position: fixed;
        top: 20px;
        left: 20px;
        z-index: 99999;
    }

    .kiosk-title {
        color: white;
        text-align: center;
        font-size: 50px !important;
        font-weight: 900;
        margin-top: 10px;
        margin-bottom: 35px;
        font-family: 'Arial Black', sans-serif;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
    }

    /* THE UNIVERSAL KIOSK BUTTON: White Box, Black Text, Giant Font */
    div.stButton > button {
        background-color: white !important;
        color: black !important;
        border-radius: 40px !important;
        border: 8px solid #1a202c !important;
        font-size: 45px !important;
        font-weight: 900 !important;
        min-height: 140px !important;
        width: 100% !important;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.4) !important;
        font-family: 'Arial Black', sans-serif !important;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px !important;
    }

    /* Floating Back Button Specific Style */
    .floating-back-btn div.stButton > button {
        min-height: 80px !important;
        font-size: 30px !important;
        padding: 0 30px !important;
        border: 5px solid #1a202c !important;
        width: auto !important;
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

    /* WORKSHEET PREVIEW BOX */
    .worksheet-preview {
        background-color: white;
        padding: 30px;
        border-radius: 20px;
        border: 10px solid #1a202c;
        margin-bottom: 25px;
        box-shadow: 0px 15px 30px rgba(0,0,0,0.5);
    }
    
    .answer-box {
        background-color: white;
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

# --- 2. SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'animal' not in st.session_state: st.session_state.animal = None
if 'reveal' not in st.session_state: st.session_state.reveal = False

# --- 3. FLOATING BACK BUTTON ---
if st.session_state.page != "home":
    st.markdown('<div class="floating-back-btn">', unsafe_allow_html=True)
    if st.button("🏠 BACK", key="global_back"):
        st.session_state.page = "home"
        st.session_state.animal = None
        st.session_state.reveal = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. NAVIGATION ---

# HOME PAGE
if st.session_state.page == "home":
    st.markdown('<div class="kiosk-title">Current choice:</div>', unsafe_allow_html=True)
    if st.button("🎨 A. Color Sheet Maker"):
        st.session_state.page = "coloring"; st.rerun()
    if st.button("🧩 B. Today's Puzzle"):
        st.session_state.page = "puzzle"; st.rerun()
    if st.button("💡 C. Fun Fact"):
        st.session_state.page = "fact"; st.rerun()
    if st.button("➕ D. Math Magic"):
        st.session_state.page = "math"; st.rerun()

# COLOR SHEET MAKER
elif st.session_state.page == "coloring":
    if st.session_state.animal is None:
        st.markdown('<div class="instruction-text">Pick an animal!</div>', unsafe_allow_html=True)
        
        # Expanded Animal List in Two Columns
        animals = [
            ("🦁 LION", "LION"), ("🐘 ELEPHANT", "ELEPHANT"), 
            ("🦒 GIRAFFE", "GIRAFFE"), ("🦓 ZEBRA", "ZEBRA"), 
            ("🐒 MONKEY", "MONKEY"), ("🐯 TIGER", "TIGER"),
            ("🐻 BEAR", "BEAR"), ("🦛 HIPPO", "HIPPO"),
            ("🐊 CROC", "CROC"), ("🦘 KANGO", "KANGO")
        ]
        
        col1, col2 = st.columns(2)
        for i, (label, name) in enumerate(animals):
            target_col = col1 if i % 2 == 0 else col2
            if target_col.button(label, key=f"btn_{name}"):
                st.session_state.animal = name
                st.rerun()
    else:
        # Title: [Animal Name] Color Sheet
        st.markdown(f'<div class="instruction-text">{st.session_state.animal} Color Sheet</div>', unsafe_allow_html=True)
        
        # Reliable images for preview
        st.markdown('<div class="worksheet-preview">', unsafe_allow_html=True)
        # Using a reliable placeholder for all animals in the demo
        st.image(f"https://img.icons8.com/ios/500/{st.session_state.animal.lower()}.png", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🖨️ PRINT NOW"):
            st.success("Success! Pick up your page at the desk.")

# PUZZLE PAGE
elif st.session_state.page == "puzzle":
    st.markdown('<div class="instruction-text">🧩 Today\'s Riddle</div>', unsafe_allow_html=True)
    st.markdown('<div class="answer-box">What has hands but cannot clap?</div>', unsafe_allow_html=True)
    if st.session_state.reveal:
        st.markdown('<div class="answer-box" style="background-color:#FFD700;">Answer: A Clock! ⏰</div>', unsafe_allow_html=True)
    else:
        if st.button("🔍 SHOW ANSWER"):
            st.session_state.reveal = True; st.rerun()

# MATH MAGIC
elif st.session_state.page == "math":
    st.markdown('<div class="instruction-text">➕ Math Magic!</div>', unsafe_allow_html=True)
    st.markdown('<div class="answer-box" style="font-size:80px !important;">5 + 5 = ?</div>', unsafe_allow_html=True)
    if st.session_state.reveal:
        st.markdown('<div class="answer-box" style="background-color:#FFD700; font-size:80px !important;">10! 🌟</div>', unsafe_allow_html=True)
    else:
        if st.button("🤔 CHECK"):
            st.session_state.reveal = True; st.rerun()

# FUN FACT
elif st.session_state.page == "fact":
    st.markdown('<div class="instruction-text">💡 Fun Fact!</div>', unsafe_allow_html=True)
    st.markdown('<div class="answer-box">Octopuses have three hearts! 🐙</div>', unsafe_allow_html=True)
