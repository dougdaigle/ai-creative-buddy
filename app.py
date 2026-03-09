import streamlit as st
import random
import os

# --- 1. IPAD STYLING: SKY BLUE & ICON BUTTONS ---
st.set_page_config(page_title="My Creative Buddy", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #00BFFF; }
    
    .kiosk-title {
        color: white;
        text-align: center;
        font-size: 55px !important;
        font-weight: 900;
        margin-top: 10px;
        margin-bottom: 30px;
        font-family: 'Arial Black', sans-serif;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
    }

    /* THE ICON BUTTON: Black Text, Giant Emojis, Massive Font */
    .kiosk-link {
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: white !important;
        color: black !important;
        text-decoration: none !important;
        padding: 20px;
        font-size: 48px !important; /* Large readable font */
        font-weight: 900 !important;
        min-height: 160px !important;
        width: 100% !important;
        border-radius: 45px;
        border: 8px solid #1a202c;
        margin-bottom: 30px;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.4);
        font-family: 'Arial Black', sans-serif;
    }

    /* Styling the Icon specifically to be extra large */
    .btn-icon {
        font-size: 75px; 
        margin-right: 25px;
    }

    .kiosk-link:active {
        background-color: #E0E0E0 !important;
        transform: scale(0.98);
    }
    
    header, footer, #MainMenu, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    .instruction-text {
        color: white;
        text-align: center;
        font-size: 35px;
        font-weight: 900;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    /* Frame for the coloring sheets */
    [data-testid="stImage"] {
        background-color: white;
        padding: 15px;
        border-radius: 30px;
        border: 5px solid #1a202c;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if 'mode' not in st.session_state: st.session_state.mode = None
if 'selected_char' not in st.session_state: st.session_state.selected_char = None

# --- 3. MAIN MENU (HOME PAGE) ---
if st.session_state.mode is None:
    st.markdown('<div class="kiosk-title">Choose an activity:</div>', unsafe_allow_html=True)
    
    # HTML Buttons with Giant Icons
    st.markdown('<a href="/?mode=coloring" class="kiosk-link" target="_self"><span class="btn-icon">🎨</span> A. Color Sheet Maker</a>', unsafe_allow_html=True)
    st.markdown('<a href="/?mode=puzzle" class="kiosk-link" target="_self"><span class="btn-icon">🧩</span> B. Today\'s Puzzle</a>', unsafe_allow_html=True)
    st.markdown('<a href="/?mode=fact" class="kiosk-link" target="_self"><span class="btn-icon">💡</span> C. Fun Fact</a>', unsafe_allow_html=True)
    st.markdown('<a href="/?mode=math" class="kiosk-link" target="_self"><span class="btn-icon">➕</span> D. Math Magic</a>', unsafe_allow_html=True)

    if "mode" in st.query_params:
        st.session_state.mode = st.query_params["mode"]
        st.query_params.clear()
        st.rerun()

# --- 4. ACTIVITY PAGES ---
else:
    if st.session_state.mode == "coloring":
        st.markdown('<div class="instruction-text">Pick an animal to color!</div>', unsafe_allow_html=True)
        # Animal Selection for Demo
        col1, col2 = st.columns(2)
        with col1:
            st.image("http://googleusercontent.com/image_collection/image_retrieval/379734712510393884_0", caption="Lion", use_container_width=True)
            if st.button("Choose Lion", use_container_width=True): st.success("Printing Lion Page..."); st.rerun()
        with col2:
            st.image("http://googleusercontent.com/image_collection/image_retrieval/379734712510393884_2", caption="Elephant", use_container_width=True)
            if st.button("Choose Elephant", use_container_width=True): st.success("Printing Elephant Page..."); st.rerun()

    elif st.session_state.mode == "puzzle":
        st.markdown('<div class="instruction-text">🧩 Today\'s Riddle</div>', unsafe_allow_html=True)
        st.info("What has hands but cannot clap? \n\n**Answer:** A Clock! ⏰")

    elif st.session_state.mode == "math":
        st.markdown('<div class="kiosk-title">5 + 5 = ?</div>', unsafe_allow_html=True)
        if st.button("🌟 SHOW ANSWER", use_container_width=True): st.success("The answer is 10! 🌟")

    elif st.session_state.mode == "fact":
        st.markdown('<div class="instruction-text">💡 Fun Fact!</div>', unsafe_allow_html=True)
        st.success("Octopuses have three hearts! 🐙")

    st.write("---")
    if st.button("🏠 BACK TO MENU", use_container_width=True):
        st.session_state.mode = None
        st.rerun()
