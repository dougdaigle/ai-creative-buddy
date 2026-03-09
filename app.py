import streamlit as st
import random
import os

# --- 1. IPAD STYLING: PERSISTENT SKY BLUE THEME ---
st.set_page_config(page_title="My Creative Buddy", layout="centered")

st.markdown("""
    <style>
    /* Sky Blue Background across all pages */
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

    /* THE KIOSK BUTTON: Black Text on White, Massive Font */
    div.stButton > button, .kiosk-link {
        display: block;
        background-color: white !important;
        color: black !important;
        text-decoration: none !important;
        text-align: center;
        line-height: 1.2;
        padding: 20px;
        font-size: 50px !important;
        font-weight: 900 !important;
        min-height: 160px !important;
        width: 100% !important;
        border-radius: 40px;
        border: 8px solid #1a202c;
        margin-bottom: 30px;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.4);
        font-family: 'Arial Black', sans-serif;
    }

    /* Smaller button override for sub-selections like "Dino" */
    .sub-btn div.stButton > button {
        min-height: 100px !important;
        font-size: 30px !important;
    }

    /* White text for activity labels/instructions */
    .instruction-text {
        color: white;
        text-align: center;
        font-size: 35px;
        font-weight: 900;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    /* Clean Kiosk UI */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    [data-testid="stHeader"] {display: none;}
    
    /* Center images on the blue background */
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
if 'math_problem' not in st.session_state: st.session_state.math_problem = None

# --- 3. MAIN MENU (HOME PAGE) ---
if st.session_state.mode is None:
    st.markdown('<div class="kiosk-title">Choose an activity:</div>', unsafe_allow_html=True)
    
    # Custom HTML buttons for the main menu to ensure black text visibility
    c1 = st.markdown('<a href="/?mode=coloring" class="kiosk-link" target="_self">A. Color Sheet Maker</a>', unsafe_allow_html=True)
    c2 = st.markdown('<a href="/?mode=puzzle" class="kiosk-link" target="_self">B. Today\'s Puzzle</a>', unsafe_allow_html=True)
    c3 = st.markdown('<a href="/?mode=fact" class="kiosk-link" target="_self">C. Fun Fact</a>', unsafe_allow_html=True)
    c4 = st.markdown('<a href="/?mode=math" class="kiosk-link" target="_self">D. Math Magic</a>', unsafe_allow_html=True)

    if "mode" in st.query_params:
        st.session_state.mode = st.query_params["mode"]
        st.query_params.clear()
        st.rerun()

# --- 4. ACTIVITY PAGES (SKY BLUE PERSISTENT) ---
else:
    # --- COLORING PAGE ---
    if st.session_state.mode == "coloring":
        if st.session_state.selected_char is None:
            st.markdown('<div class="instruction-text">1. Pick a Friend!</div>', unsafe_allow_html=True)
            st.markdown('<div class="sub-btn">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🦖 DINOSAUR", use_container_width=True): st.session_state.selected_char = "dinosaur"; st.rerun()
            with col2:
                if st.button("🚀 ASTRO", use_container_width=True): st.session_state.selected_char = "astronaut"; st.rerun()
            with col3:
                if st.button("🦄 MAGIC", use_container_width=True): st.session_state.selected_char = "unicorn"; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="instruction-text">Showing your {st.session_state.selected_char}!</div>', unsafe_allow_html=True)
            arts = {
                "dinosaur": ["https://img.icons8.com/ios/500/dinosaur.png", "https://img.icons8.com/ios-filled/500/dinosaur.png", "https://img.icons8.com/external-flatart-icons-outline-flatarticons/500/external-dinosaur-dinosaur-flatart-icons-outline-flatarticons.png"],
                "astronaut": ["https://img.icons8.com/ios/500/astronaut-helmet.png", "https://img.icons8.com/ios-filled/500/astronaut-helmet.png", "https://img.icons8.com/external-outline-juicy-fish/500/external-astronaut-space-exploration-outline-outline-juicy-fish.png"],
                "unicorn": ["https://img.icons8.com/ios/500/unicorn.png", "https://img.icons8.com/ios-filled/500/unicorn.png", "https://img.icons8.com/external-outline-lafs/500/external-unicorn-fantasy-and-magic-outline-lafs.png"]
            }
            st.image(random.choice(arts[st.session_state.selected_char]), use_container_width=True)
            if st.button("🖨️ PRINT NOW", use_container_width=True): st.success("Printing...")

    # --- TODAY'S PUZZLE ---
    elif st.session_state.mode == "puzzle":
        st.markdown('<div class="instruction-text">🧩 Today\'s Riddle</div>', unsafe_allow_html=True)
        riddles = [
            "What has hands but cannot clap? \n\n**Answer:** A Clock! ⏰",
            "What has to be broken before you can use it? \n\n**Answer:** An Egg! 🥚"
        ]
        st.info(random.choice(riddles))
        if st.button("🎲 NEW RIDDLE", use_container_width=True): st.rerun()

    # --- MATH MAGIC ---
    elif st.session_state.mode == "math":
        st.markdown('<div class="instruction-text">➕ Math Magic!</div>', unsafe_allow_html=True)
        if st.session_state.math_problem is None:
            n1, n2 = random.randint(1, 10), random.randint(1, 10)
            st.session_state.math_problem = {"q": f"{n1} + {n2} =", "a": n1 + n2}
        
        st.markdown(f'<div class="kiosk-title">{st.session_state.math_problem["q"]} ?</div>', unsafe_allow_html=True)
        if st.button("🌟 SHOW ANSWER", use_container_width=True):
            st.success(f"The answer is {st.session_state.math_problem['a']}! 🌟")

    # --- FUN FACT ---
    elif st.session_state.mode == "fact":
        st.markdown('<div class="instruction-text">💡 Fun Fact!</div>', unsafe_allow_html=True)
        facts = ["Octopuses have three hearts! 🐙", "Honey never spoils! 🍯"]
        st.success(random.choice(facts))
        if st.button("🌟 NEXT FACT", use_container_width=True): st.rerun()

    # --- UNIVERSAL BACK BUTTON ---
    st.write("---")
    if st.button("🏠 BACK TO MENU", use_container_width=True):
        st.session_state.mode = None
        st.session_state.selected_char = None
        st.session_state.math_problem = None
        st.rerun()
