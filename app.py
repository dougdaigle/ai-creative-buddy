import streamlit as st
import time

# --- 1. IPAD STYLING: PERMANENT SKY BLUE & FORCED BLACK TEXT ---
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

    /* THE UNIVERSAL KIOSK BUTTON: Solid Black Text on White */
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
        display: flex !important;
        justify-content: flex-start !important;
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

    /* WORKSHEET PREVIEW BOX */
    .worksheet-preview {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border: 8px solid #1a202c;
        margin-bottom: 30px;
        box-shadow: 0px 15px 30px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE (The Navigation Brain) ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'animal' not in st.session_state: st.session_state.animal = None

# --- 3. FLOATING BACK BUTTON ---
if st.session_state.page != "home":
    # Using a container and button for 100% reliability
    st.markdown('<div class="floating-back">', unsafe_allow_html=True)
    if st.button("🏠 BACK", key="global_back"):
        st.session_state.page = "home"
        st.session_state.animal = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. NAVIGATION PAGES ---

# --- HOME PAGE ---
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

# --- COLOR SHEET MAKER ---
elif st.session_state.page == "coloring":
    if st.session_state.animal is None:
        st.markdown('<div class="instruction-text">Pick an animal!</div>', unsafe_allow_html=True)
        # Using columns for the list
        c1, c2 = st.columns(2)
        if c1.button("🦖 DINO"): st.session_state.animal = "Dino"; st.rerun()
        if c2.button("🦁 LION"): st.session_state.animal = "Lion"; st.rerun()
        if c1.button("🐘 ELEPHANT"): st.session_state.animal = "Elephant"; st.rerun()
        if c2.button("🦒 GIRAFFE"): st.session_state.animal = "Giraffe"; st.rerun()
    else:
        st.markdown(f'<div class="instruction-text">{st.session_state.animal} Color Sheet</div>', unsafe_allow_html=True)
        
        # Mapping for coloring sheets
        animal_imgs = {
            "Dino": "https://raw.githubusercontent.com/username/repo/main/Dino_Adventure.jpg", # Replace with your actual image URL
            "Lion": "https://img.icons8.com/ios/500/lion.png",
            "Elephant": "https://img.icons8.com/ios/500/elephant.png",
            "Giraffe": "https://img.icons8.com/ios/500/giraffe.png"
        }
        
        # NOTE: For the local 'Dinosaur adventure' image, ensure it is in the same folder as the app
        # and replace the "Dino" URL above with "Dinosaur adventure in a prehistoric world.jpg"
        
        st.markdown('<div class="worksheet-preview">', unsafe_allow_html=True)
        # Use local file if it exists, otherwise use fallback
        try:
            st.image("Dinosaur adventure in a prehistoric world.jpg", use_container_width=True)
        except:
            st.image(animal_imgs.get(st.session_state.animal), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🖨️ PRINT NOW"):
            st.toast("🖨️ Sending to printer...", icon="🤖")

# (Other logic for Puzzle/Math/Fact remains here)
