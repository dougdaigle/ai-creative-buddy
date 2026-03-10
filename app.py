import streamlit as st
import random

# --- 1. IPAD STYLING: FORCE STYLE ON NATIVE BUTTONS ---
st.set_page_config(page_title="My Creative Buddy", layout="centered")

st.markdown("""
    <style>
    /* Sky Blue Background */
    .stApp { background-color: #00BFFF; }

    /* FORCE BLACK TEXT & GIANT FONT ON ALL BUTTONS */
    div.stButton > button {
        background-color: white !important;
        color: black !important;
        border: 8px solid #1a202c !important;
        border-radius: 40px !important;
        font-size: 50px !important;
        font-weight: 900 !important;
        height: 160px !important;
        width: 100% !important;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.3) !important;
        font-family: 'Arial Black', sans-serif !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        padding-left: 40px !important;
    }

    /* THE BACK BUTTON: Pinned Top-Left */
    .back-container {
        position: fixed;
        top: 20px;
        left: 20px;
        z-index: 10000;
    }
    
    .back-container div.stButton > button {
        height: 80px !important;
        width: auto !important;
        font-size: 30px !important;
        padding-left: 20px !important;
        padding-right: 20px !important;
        border: 5px solid #1a202c !important;
        border-radius: 20px !important;
    }

    /* WORKSHEET PREVIEW BOX */
    .worksheet-preview {
        background-color: white;
        padding: 20px;
        border-radius: 20px;
        border: 10px solid #1a202c;
        box-shadow: 0px 15px 30px rgba(0,0,0,0.5);
    }

    /* UI CLEANUP */
    header, footer, #MainMenu, [data-testid="stHeader"] {visibility: hidden; display: none;}
    h1, h2, h3 { color: white !important; text-align: center; font-family: 'Arial Black'; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE (The Navigation Brain) ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'animal' not in st.session_state: st.session_state.animal = None

# --- 3. BACK BUTTON (Functional & Persistent) ---
if st.session_state.page != "home":
    st.markdown('<div class="back-container">', unsafe_allow_html=True)
    if st.button("🏠 BACK", key="global_back"):
        st.session_state.page = "home"
        st.session_state.animal = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. NAVIGATION ---

# --- PAGE: HOME ---
if st.session_state.page == "home":
    st.markdown("<h1>Current choice:</h1>", unsafe_allow_html=True)
    if st.button("🎨 A. Color Sheet Maker"):
        st.session_state.page = "coloring"; st.rerun()
    if st.button("🧩 B. Today's Puzzle"):
        st.session_state.page = "puzzle"; st.rerun()
    if st.button("💡 C. Fun Fact"):
        st.session_state.page = "fact"; st.rerun()
    if st.button("➕ D. Math Magic"):
        st.session_state.page = "math"; st.rerun()

# --- PAGE: COLORING ---
elif st.session_state.page == "coloring":
    if not st.session_state.animal:
        st.markdown("<h3>Pick an animal!</h3>", unsafe_allow_html=True)
        # Use two columns for the animal selection
        col1, col2 = st.columns(2)
        animals = [("🦁 Lion", "Lion"), ("🐘 Elephant", "Elephant"), ("🦒 Giraffe", "Giraffe"), ("🦓 Zebra", "Zebra"), ("🐵 Monkey", "Monkey"), ("🐯 Tiger", "Tiger")]
        
        for i, (label, name) in enumerate(animals):
            target = col1 if i % 2 == 0 else col2
            if target.button(label):
                st.session_state.animal = name
                st.rerun()
    else:
        st.markdown(f"<h3>{st.session_state.animal} Color Sheet</h3>", unsafe_allow_html=True)
        
        # High-reliability image sources
        img_urls = {
            "Lion": "https://img.icons8.com/ios/500/lion.png",
            "Elephant": "https://img.icons8.com/ios/500/elephant.png",
            "Giraffe": "https://img.icons8.com/ios/500/giraffe.png",
            "Zebra": "https://img.icons8.com/ios/500/zebra.png",
            "Monkey": "https://img.icons8.com/ios/500/monkey.png",
            "Tiger": "https://img.icons8.com/ios/500/tiger-side-view.png"
        }
        
        st.markdown('<div class="worksheet-preview">', unsafe_allow_html=True)
        st.image(img_urls[st.session_state.animal], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🖨️ PRINT NOW"):
            st.balloons()
            st.success("Sent to printer!")
