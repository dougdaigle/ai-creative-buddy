import streamlit as st
import random
import os

# --- 1. IPAD STYLING: HIGH-CONTRAST FORCED TEXT ---
st.set_page_config(page_title="My Creative Buddy", layout="centered")

st.markdown("""
    <style>
    /* Sky Blue Background from your reference */
    .stApp { 
        background-color: #00BFFF; 
    }
    
    /* Clean Title */
    .menu-title {
        color: white;
        text-align: center;
        font-size: 55px !important;
        font-weight: 900;
        margin-top: 10px;
        margin-bottom: 30px;
        font-family: 'Arial Black', sans-serif;
    }

    /* THE FIX: Custom HTML Button Styling */
    .kiosk-button {
        display: block;
        background-color: white !important;
        color: black !important; /* Forced Black Text */
        text-decoration: none !important;
        text-align: center;
        line-height: 180px; /* Vertically centers the text */
        font-size: 65px !important; /* Giant Font */
        font-weight: 900 !important;
        height: 180px !important;
        width: 100% !important;
        border-radius: 40px;
        border: 8px solid #1a202c;
        margin-bottom: 35px;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.4);
        font-family: 'Arial Black', sans-serif;
    }

    .kiosk-button:active {
        background-color: #E0E0E0 !important;
        transform: scale(0.98);
    }
    
    /* Hide all standard Streamlit clutter */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    [data-testid="stHeader"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if 'mode' not in st.session_state: st.session_state.mode = None

# --- 3. MAIN MENU ---
if st.session_state.mode is None:
    st.markdown('<div class="menu-title">Current Choice:</div>', unsafe_allow_html=True)
    
    # We use st.columns and custom HTML to ensure the text is 100% visible
    # These act exactly like buttons once clicked
    if st.markdown('<a href="/?mode=coloring" class="kiosk-button" target="_self">A. Coloring Sheet</a>', unsafe_allow_html=True):
        pass
        
    if st.markdown('<a href="/?mode=puzzle" class="kiosk-button" target="_self">B. Today\'s Puzzle</a>', unsafe_allow_html=True):
        pass
        
    if st.markdown('<a href="/?mode=fact" class="kiosk-button" target="_self">C. Fun Fact</a>', unsafe_allow_html=True):
        pass
        
    if st.markdown('<a href="/?mode=math" class="kiosk-button" target="_self">D. Math Magic</a>', unsafe_allow_html=True):
        pass

    # URL-based navigation check for the demo
    params = st.query_params
    if "mode" in params:
        st.session_state.mode = params["mode"]
        st.rerun()

# --- 4. SIMPLE DEMO RESPONSES ---
elif st.session_state.mode == "coloring":
    st.write("# 🎨 Pick a Dino!")
    if st.button("🦖 DINOSAUR", use_container_width=True):
        st.image("https://img.icons8.com/ios/500/dinosaur.png")

elif st.session_state.mode == "puzzle":
    st.info("### Riddle: What has hands but no feet? \n\n**Answer:** A Clock! ⏰")

elif st.session_state.mode == "fact":
    st.success("### Fact: Honey never spoils! 🍯")

elif st.session_state.mode == "math":
    st.write("# 10 + 5 = ?")
    st.success("### 15! 🌟")

# --- 5. BACK BUTTON ---
if st.session_state.mode:
    st.write("---")
    if st.button("🏠 BACK TO MENU", use_container_width=True):
        st.query_params.clear()
        st.session_state.mode = None
        st.rerun()
