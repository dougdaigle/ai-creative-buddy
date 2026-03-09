import streamlit as st
import random
import os

# --- 1. IPAD STYLING: REFINED HEADER & BUTTON LAYOUT ---
st.set_page_config(page_title="My Creative Buddy", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #00BFFF; }
    
    .kiosk-title {
        color: white;
        text-align: center;
        font-size: 50px !important;
        font-weight: 900;
        margin-top: 10px;
        margin-bottom: 35px;
        font-family: 'Arial Black', sans-serif;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
    }

    /* THE ICON BUTTON: Optimized for single-line text */
    .kiosk-link {
        display: flex;
        align-items: center;
        justify-content: flex-start; /* Align to the left for better spacing */
        background-color: white !important;
        color: black !important;
        text-decoration: none !important;
        padding: 0 40px; /* Side padding only */
        font-size: 42px !important; /* Slightly smaller to fit single line */
        font-weight: 900 !important;
        min-height: 140px !important; /* Slightly shorter to fit more buttons comfortably */
        width: 100% !important;
        border-radius: 40px;
        border: 8px solid #1a202c;
        margin-bottom: 25px;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.4);
        font-family: 'Arial Black', sans-serif;
        white-space: nowrap; /* FORCES SINGLE LINE */
        overflow: hidden;
    }

    .btn-icon {
        font-size: 65px; 
        margin-right: 30px;
        flex-shrink: 0;
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

    /* Worksheet Frame */
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

# --- 3. MAIN MENU (HOME PAGE) ---
if st.session_state.mode is None:
    # Title updated as requested
    st.markdown('<div class="kiosk-title">Current choice:</div>', unsafe_allow_html=True)
    
    # HTML Buttons with Giant Icons and single-line enforcement
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
        st.markdown('<div class="instruction-text">Pick an animal!</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.image("http://googleusercontent.com/image_collection/image_retrieval/379734712510393884_0", use_container_width=True)
            if st.button("Lion", use_container_width=True): st.success("Printing..."); st.rerun()
        with col2:
            st.image("http://googleusercontent.com/image_collection/image_retrieval/379734712510393884_2", use_container_width=True)
            if st.button("Elephant", use_container_width=True): st.success("Printing..."); st.rerun()

    elif st.session_state.mode == "puzzle":
        st.markdown('<div class="instruction-text">Today\'s Riddle</div>', unsafe_allow_html=True)
        st.info("I have hands but cannot clap. \n\n**Answer:** A Clock! ⏰")

    st.write("---")
    if st.button("🏠 BACK TO MENU", use_container_width=True):
        st.session_state.mode = None
        st.rerun()
