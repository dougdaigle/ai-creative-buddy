import streamlit as st
import random

# --- 1. IPAD STYLING: PERSISTENT KIOSK THEME ---
st.set_page_config(page_title="My Creative Buddy", layout="centered")

st.markdown("""
    <style>
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

    /* THE UNIVERSAL KIOSK BUTTON */
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
        margin-bottom: 20px !important;
    }

    /* CLEANUP */
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

# --- 2. SESSION STATE (The Brain) ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'animal' not in st.session_state: st.session_state.animal = None
if 'reveal' not in st.session_state: st.session_state.reveal = False

# --- 3. FLOATING BACK BUTTON ---
if st.session_state.page != "home":
    with st.container():
        st.markdown('<div class="floating-back-btn">', unsafe_allow_html=True)
        if st.button("🏠 BACK", key="global_back"):
            st.session_state.page = "home"
            st.session_state.animal = None
            st.session_state.reveal = False
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
        if st.button("🦁 LION"): st.session_state.animal = "Lion"; st.rerun()
        if st.button("🐘 ELEPHANT"): st.session_state.animal = "Elephant"; st.rerun()
        if st.button("🦒 GIRAFFE"): st.session_state.animal = "Giraffe"; st.rerun()
        if st.button("🦓 ZEBRA"): st.session_state.animal = "Zebra"; st.rerun()
        if st.button("🐒 MONKEY"): st.session_state.animal = "Monkey"; st.rerun()
        if st.button("🐯 TIGER"): st.session_state.animal = "Tiger"; st.rerun()
    else:
        st.markdown(f'<div class="instruction-text">{st.session_state.animal} Color Sheet</div>', unsafe_allow_html=True)
        
        # Using reliable static URLs for the demo
        animal_imgs = {
            "Lion": "https://img.icons8.com/ios/500/lion.png",
            "Elephant": "https://img.icons8.com/ios/500/elephant.png",
            "Giraffe": "https://img.icons8.com/ios/500/giraffe.png",
            "Zebra": "https://img.icons8.com/ios/500/zebra.png",
            "Monkey": "https://img.icons8.com/ios/500/monkey.png",
            "Tiger": "https://img.icons8.com/ios/500/tiger-side-view.png"
        }
        
        st.markdown('<div class="worksheet-preview">', unsafe_allow_html=True)
        st.image(animal_imgs[st.session_state.animal], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🖨️ PRINT NOW"):
            st.balloons()
            st.toast("Sending to printer...")

# --- TODAY'S PUZZLE ---
elif st.session_state.page == "puzzle":
    st.markdown('<div class="instruction-text">🧩 Today\'s Riddle</div>', unsafe_allow_html=True)
    st.markdown('<div class="answer-box">What has a face and two hands but no arms or legs?</div>', unsafe_allow_html=True)
    if st.session_state.reveal:
        st.markdown('<div class="answer-box" style="background-color:#FFD700;">Answer: A Clock! ⏰</div>', unsafe_allow_html=True)
    else:
        if st.button("🔍 SHOW ANSWER"):
            st.session_state.reveal = True; st.rerun()

# --- MATH MAGIC ---
elif st.session_state.page == "math":
    st.markdown('<div class="instruction-text">➕ Math Magic!</div>', unsafe_allow_html=True)
    st.markdown('<div class="answer-box" style="font-size:80px !important;">7 + 3 = ?</div>', unsafe_allow_html=True)
    if st.session_state.reveal:
        st.markdown('<div class="answer-box" style="background-color:#FFD700; font-size:80px !important;">10! 🌟</div>', unsafe_allow_html=True)
    else:
        if st.button("🤔 CHECK ANSWER"):
            st.session_state.reveal = True; st.rerun()

# --- FUN FACT ---
elif st.session_state.page == "fact":
    st.markdown('<div class="instruction-text">💡 Fun Fact!</div>', unsafe_allow_html=True)
    st.markdown('<div class="answer-box">A shrimp\'s heart is in its head! 🦐</div>', unsafe_allow_html=True)
