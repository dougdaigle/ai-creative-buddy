import streamlit as st
import random
import time

# --- 1. IPAD STYLING: REVERTED TO EXACT HTML LINK LOOK ---
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

    /* THE UNIVERSAL KIOSK BUTTON: Reverted to your preferred HTML style */
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

    /* Small hack to make standard Streamlit buttons look like the floating back button */
    .floating-back-btn div.stButton > button {
        background-color: white !important;
        color: black !important;
        border-radius: 20px !important;
        border: 5px solid #1a202c !important;
        font-size: 25px !important;
        font-weight: 900 !important;
        height: 70px !important;
        padding: 0 25px !important;
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
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE (The Brain) ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'animal' not in st.session_state: st.session_state.animal = None

# --- 3. FLOATING BACK BUTTON ---
if st.session_state.page != "home":
    st.markdown('<div class="floating-back-btn">', unsafe_allow_html=True)
    if st.button("🏠 BACK", key="global_back"):
        st.session_state.page = "home"
        st.session_state.animal = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. NAVIGATION PAGES ---

# --- HOME PAGE ---
if st.session_state.page == "home":
    st.markdown('<div class="kiosk-title">Current choice:</div>', unsafe_allow_html=True)
    
    # We use st.button but style it to look EXACTLY like your HTML links
    if st.button("🎨 A. Color Sheet Maker", key="btn_a"):
        st.session_state.page = "coloring"; st.rerun()
    if st.button("🧩 B. Today's Puzzle", key="btn_b"):
        st.session_state.page = "puzzle"; st.rerun()
    if st.button("💡 C. Fun Fact", key="btn_c"):
        st.session_state.page = "fact"; st.rerun()
    if st.button("➕ D. Math Magic", key="btn_d"):
        st.session_state.page = "math"; st.rerun()

    # CSS to force the st.button to use the kiosk-link style
    st.markdown("""
        <style>
        div.stButton > button {
            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;
            background-color: white !important;
            color: black !important;
            font-size: 42px !important;
            font-weight: 900 !important;
            min-height: 140px !important;
            border-radius: 40px !important;
            border: 8px solid #1a202c !important;
            margin-bottom: 25px !important;
            padding-left: 40px !important;
            font-family: 'Arial Black', sans-serif !important;
        }
        </style>
        """, unsafe_allow_html=True)

# --- OPTION A: COLOR SHEET MAKER ---
elif st.session_state.page == "coloring":
    if st.session_state.animal is None:
        st.markdown('<div class="instruction-text">Pick an animal!</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        animals = [
            ("🦁 LION", "Lion"), ("🐘 ELEPHANT", "Elephant"), 
            ("🦒 GIRAFFE", "Giraffe"), ("🦓 ZEBRA", "Zebra"), 
            ("🐒 MONKEY", "Monkey"), ("🐯 TIGER", "Tiger"),
            ("🐻 BEAR", "Bear"), ("🦛 HIPPO", "Hippo")
        ]
        
        for i, (label, name) in enumerate(animals):
            target_col = col1 if i % 2 == 0 else col2
            if target_col.button(label):
                st.session_state.animal = name
                st.rerun()
    else:
        st.markdown(f'<div class="instruction-text">{st.session_state.animal} Color Sheet</div>', unsafe_allow_html=True)
        
        # Worksheet Frame
        st.markdown('<div class="worksheet-preview">', unsafe_allow_html=True)
        # Using icons8 as a reliable source for the black-and-white images
        img_url = f"https://img.icons8.com/ios/500/{st.session_state.animal.lower()}.png"
        st.image(img_url, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🖨️ PRINT NOW"):
            st.toast("Sending to printer...")

# (Other pages would follow the same pattern)
