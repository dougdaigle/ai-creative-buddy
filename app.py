import streamlit as st
from google import genai
from google.genai import types
import random
import os

# --- 1. IPAD STYLING: Forced Visibility Kiosk Look ---
st.set_page_config(page_title="My Creative Buddy", layout="centered")

st.markdown("""
    <style>
    /* Sky Blue Home Page */
    .stApp { background-color: #00BFFF; }
    
    /* Activity Page Override (White background) */
    .activity-bg {
        background-color: white;
        padding: 20px;
        border-radius: 20px;
        color: black !important;
    }

    .menu-title {
        color: white;
        text-align: center;
        font-size: 55px !important;
        font-weight: 900;
        margin-top: 10px;
        margin-bottom: 30px;
        font-family: 'Arial Black', sans-serif;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
    }

    /* THE FIX: Custom HTML Button Styling for First Page */
    .kiosk-button {
        display: block;
        background-color: white !important;
        color: black !important;
        text-decoration: none !important;
        text-align: center;
        line-height: 160px;
        font-size: 50px !important;
        font-weight: 900 !important;
        height: 160px !important;
        width: 100% !important;
        border-radius: 40px;
        border: 8px solid #1a202c;
        margin-bottom: 30px;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.4);
        font-family: 'Arial Black', sans-serif;
    }

    .kiosk-button:active {
        background-color: #E0E0E0 !important;
        transform: scale(0.98);
    }
    
    /* Clean Kiosk UI */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    [data-testid="stHeader"] {display: none;}
    
    /* Ensure Activity text is readable */
    .stMarkdown, .stMarkdown p { color: inherit; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. AI CLIENT SETUP ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("🔑 API Key Missing!")
    st.stop()

# --- 3. SESSION STATE ---
if 'mode' not in st.session_state: st.session_state.mode = None
if 'selected_char' not in st.session_state: st.session_state.selected_char = None
if 'math_problem' not in st.session_state: st.session_state.math_problem = None

# --- 4. MAIN MENU (HOME PAGE) ---
if st.session_state.mode is None:
    st.markdown('<div class="menu-title">Current choice:</div>', unsafe_allow_html=True)
    
    # Using the Query Param trick to make HTML links act like Streamlit buttons
    if st.markdown('<a href="/?mode=coloring" class="kiosk-button" target="_self">A. Color Sheet Maker</a>', unsafe_allow_html=True): pass
    if st.markdown('<a href="/?mode=puzzle" class="kiosk-button" target="_self">B. Today\'s Puzzle</a>', unsafe_allow_html=True): pass
    if st.markdown('<a href="/?mode=fact" class="kiosk-button" target="_self">C. Fun Fact</a>', unsafe_allow_html=True): pass
    if st.markdown('<a href="/?mode=math" class="kiosk-button" target="_self">D. Math Magic</a>', unsafe_allow_html=True): pass

    # Catch the click
    if "mode" in st.query_params:
        st.session_state.mode = st.query_params["mode"]
        st.query_params.clear()
        st.rerun()

# --- 5. ACTIVITY PAGES (RESTORED LOGIC) ---
else:
    # Switch to white background for activities
    st.markdown('<style>.stApp { background-color: white !important; }</style>', unsafe_allow_html=True)
    
    with st.container():
        # --- COLORING PAGE ---
        if st.session_state.mode == "coloring":
            if st.session_state.selected_char is None:
                st.markdown("<h1 style='color:black;'>1. Pick a Friend!</h1>", unsafe_allow_html=True)
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.image("https://img.icons8.com/color/200/dinosaur.png")
                    if st.button("Dinosaur", use_container_width=True): st.session_state.selected_char = "dinosaur"; st.rerun()
                with c2:
                    st.image("https://img.icons8.com/color/200/astronaut-helmet.png")
                    if st.button("Astronaut", use_container_width=True): st.session_state.selected_char = "astronaut"; st.rerun()
                with c3:
                    st.image("https://img.icons8.com/color/200/unicorn.png")
                    if st.button("Unicorn", use_container_width=True): st.session_state.selected_char = "unicorn"; st.rerun()
            else:
                st.markdown(f"<h2 style='color:black;'>Making your {st.session_state.selected_char}!</h2>", unsafe_allow_html=True)
                if st.button("✨ SHOW DRAWING", use_container_width=True):
                    with st.spinner("Drawing..."):
                        # Reverting to the rotating static options for the demo
                        arts = {
                            "dinosaur": ["https://img.icons8.com/ios/500/dinosaur.png", "https://img.icons8.com/ios-filled/500/dinosaur.png", "https://img.icons8.com/external-flatart-icons-outline-flatarticons/500/external-dinosaur-dinosaur-flatart-icons-outline-flatarticons.png"],
                            "astronaut": ["https://img.icons8.com/ios/500/astronaut-helmet.png", "https://img.icons8.com/ios-filled/500/astronaut-helmet.png", "https://img.icons8.com/external-outline-juicy-fish/500/external-astronaut-space-exploration-outline-outline-juicy-fish.png"],
                            "unicorn": ["https://img.icons8.com/ios/500/unicorn.png", "https://img.icons8.com/ios-filled/500/unicorn.png", "https://img.icons8.com/external-outline-lafs/500/external-unicorn-fantasy-and-magic-outline-lafs.png"]
                        }
                        st.image(random.choice(arts[st.session_state.selected_char]), use_container_width=True)
                        st.button("🖨️ PRINT NOW", use_container_width=True)

        # --- TODAY'S PUZZLE ---
        elif st.session_state.mode == "puzzle":
            st.markdown("<h1 style='color:black;'>🧩 The Robot's Riddle</h1>", unsafe_allow_html=True)
            if st.button("🎲 GET A RIDDLE", use_container_width=True):
                riddles = [
                    "I have keys, but no locks. I have a space, but no room. **Answer:** A Keyboard! ⌨️",
                    "What has hands but cannot clap? **Answer:** A Clock! ⏰",
                    "What has to be broken before you can use it? **Answer:** An Egg! 🥚"
                ]
                st.info(random.choice(riddles))
                st.button("🖨️ PRINT RIDDLE", use_container_width=True)

        # --- MATH MAGIC ---
        elif st.session_state.mode == "math":
            st.markdown("<h1 style='color:black;'>➕ Math Magic!</h1>", unsafe_allow_html=True)
            if st.button("📝 NEW PROBLEM", use_container_width=True):
                n1, n2 = random.randint(1, 10), random.randint(1, 10)
                st.session_state.math_problem = {"q": f"{n1} + {n2} =", "a": n1 + n2}
            if st.session_state.math_problem:
                st.markdown(f"<h2 style='color:black;'>{st.session_state.math_problem['q']}</h2>", unsafe_allow_html=True)
                ans = st.number_input("Answer:", min_value=0, step=1)
                if st.button("✅ CHECK", use_container_width=True):
                    if ans == st.session_state.math_problem['a']: st.success("🌟 Correct!")
                    else: st.warning("Try again!")

        # --- FUN FACT ---
        elif st.session_state.mode == "fact":
            st.markdown("<h1 style='color:black;'>💡 Fun Fact!</h1>", unsafe_allow_html=True)
            if st.button("🌟 SURPRISE ME", use_container_width=True):
                facts = ["Octopuses have three hearts! 🐙", "Honey never spoils! 🍯", "A group of flamingos is a 'flamboyance'! 🦩"]
                st.success(random.choice(facts))
                st.button("🖨️ PRINT FACT", use_container_width=True)

        # --- HOME BUTTON ---
        st.write("---")
        if st.button("🏠 BACK TO MAIN MENU", use_container_width=True):
            st.session_state.mode = None
            st.session_state.selected_char = None
            st.session_state.math_problem = None
            st.rerun()
