import streamlit as st
import random
import os

# --- 1. IPAD STYLING: THE PERMANENT KIOSK LOOK ---
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

    /* THE ICON BUTTON: Identical across all pages */
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

    .kiosk-link:active {
        background-color: #E0E0E0 !important;
        transform: scale(0.98);
    }
    
    header, footer, #MainMenu, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    .instruction-text {
        color: white;
        text-align: center;
        font-size: 40px;
        font-weight: 900;
        margin-bottom: 30px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    /* Worksheet Preview Frame */
    .worksheet-preview {
        background-color: white;
        padding: 15px;
        border-radius: 30px;
        border: 5px solid #1a202c;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if 'mode' not in st.session_state: st.session_state.mode = None
if 'selected_animal' not in st.session_state: st.session_state.selected_animal = None

# --- 3. MAIN MENU (HOME PAGE) ---
if st.session_state.mode is None:
    st.markdown('<div class="kiosk-title">Current choice:</div>', unsafe_allow_html=True)
    
    st.markdown('<a href="/?mode=coloring" class="kiosk-link" target="_self"><span class="btn-icon">🎨</span> A. Color Sheet Maker</a>', unsafe_allow_html=True)
    st.markdown('<a href="/?mode=puzzle" class="kiosk-link" target="_self"><span class="btn-icon">🧩</span> B. Today\'s Puzzle</a>', unsafe_allow_html=True)
    st.markdown('<a href="/?mode=fact" class="kiosk-link" target="_self"><span class="btn-icon">💡</span> C. Fun Fact</a>', unsafe_allow_html=True)
    st.markdown('<a href="/?mode=math" class="kiosk-link" target="_self"><span class="btn-icon">➕</span> D. Math Magic</a>', unsafe_allow_html=True)

    if "mode" in st.query_params:
        st.session_state.mode = st.query_params["mode"]
        st.query_params.clear()
        st.rerun()

# --- 4. OPTION A: COLOR SHEET MAKER ---
elif st.session_state.mode == "coloring":
    if st.session_state.selected_animal is None:
        st.markdown('<div class="instruction-text">Pick an animal!</div>', unsafe_allow_html=True)
        
        # FORCED HTML BUTTONS (Identical to Home Page)
        st.markdown('<a href="/?mode=coloring&animal=Lion" class="kiosk-link" target="_self"><span class="btn-icon">🦁</span> LION</a>', unsafe_allow_html=True)
        st.markdown('<a href="/?mode=coloring&animal=Elephant" class="kiosk-link" target="_self"><span class="btn-icon">🐘</span> ELEPHANT</a>', unsafe_allow_html=True)
        st.markdown('<a href="/?mode=coloring&animal=Giraffe" class="kiosk-link" target="_self"><span class="btn-icon">🦒</span> GIRAFFE</a>', unsafe_allow_html=True)

        if "animal" in st.query_params:
            st.session_state.selected_animal = st.query_params["animal"]
            st.query_params.clear()
            st.rerun()
    else:
        st.markdown(f'<div class="instruction-text">{st.session_state.selected_animal} Worksheet</div>', unsafe_allow_html=True)
        
        animal_imgs = {
            "Lion": "http://googleusercontent.com/image_collection/image_retrieval/379734712510393884_0",
            "Elephant": "http://googleusercontent.com/image_collection/image_retrieval/379734712510393884_2",
            "Giraffe": "https://img.icons8.com/ios/500/giraffe.png"
        }
        
        st.markdown('<div class="worksheet-preview">', unsafe_allow_html=True)
        st.image(animal_imgs[st.session_state.selected_animal], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Back and Print buttons use the same kiosk style
        if st.markdown('<a href="/?mode=coloring&action=print" class="kiosk-link" target="_self"><span class="btn-icon">🖨️</span> PRINT NOW</a>', unsafe_allow_html=True):
             pass
        
        if "action" in st.query_params:
            st.success("Printing...")
            st.query_params.clear()

    # Universal Back Button
    st.write("---")
    st.markdown('<a href="/" class="kiosk-link" target="_self"><span class="btn-icon">🏠</span> BACK TO MENU</a>', unsafe_allow_html=True)
