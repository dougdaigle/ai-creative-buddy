import streamlit as st
import datetime
import random
import os

# --- 1. IPAD STYLING: Sky Blue Background & Large White Buttons ---
st.set_page_config(page_title="My Creative Buddy", layout="centered")

st.markdown("""
    <style>
    /* Vibrant Sky Blue Background */
    .stApp { 
        background-color: #00BFFF; 
    }
    
    .menu-title {
        color: white;
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        margin-top: 30px;
        margin-bottom: 30px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    /* LARGE WHITE BUTTONS: Dark Blue text, thick border, massive font */
    div.stButton > button {
        background-color: white !important;
        color: #1E3A8A !important; /* Dark Blue text */
        border-radius: 30px !important;
        border: 5px solid #1E3A8A !important; 
        font-size: 45px !important; /* MUCH LARGER FONT */
        font-weight: 900 !important;
        height: 150px !important; /* TALLER BUTTONS */
        width: 100% !important;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.2);
        margin-bottom: 35px;
        transition: transform 0.1s;
    }

    div.stButton > button:active {
        transform: scale(0.98);
        background-color: #F0F0F0 !important;
    }
    
    /* Clean Kiosk UI */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* White text for general labels */
    h2, h3, p, label { color: white !important; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if 'mode' not in st.session_state: st.session_state.mode = None
if 'selected_char' not in st.session_state: st.session_state.selected_char = None
if 'math_problem' not in st.session_state: st.session_state.math_problem = None

# --- 3. MAIN MENU ---
if st.session_state.mode is None:
    st.markdown('<div class="menu-title">Current choice:</div>', unsafe_allow_html=True)
    
    # Matching the A-C lettered style from the kiosk photo
    if st.button("🎨 A. Color Sheet Maker", use_container_width=True): 
        st.session_state.mode = "coloring"; st.rerun()
        
    if st.button("🧩 B. Today's Puzzle", use_container_width=True): 
        st.session_state.mode = "puzzle"; st.rerun()
        
    if st.button("💡 C. Fun Fact", use_container_width=True): 
        st.session_state.mode = "fact"; st.rerun()
        
    if st.button("➕ D. Math Magic", use_container_width=True): 
        st.session_state.mode = "math"; st.rerun()

# --- 4. COLORING PAGE ---
elif st.session_state.mode == "coloring":
    if st.session_state.selected_char is None:
        st.write("## Pick a Friend!")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.image("https://img.icons8.com/color/200/dinosaur.png", use_container_width=True)
            if st.button("Dino", use_container_width=True): 
                st.session_state.selected_char = "dinosaur"; st.rerun()
        with c2:
            st.image("https://img.icons8.com/color/200/astronaut-helmet.png", use_container_width=True)
            if st.button("Astro", use_container_width=True): 
                st.session_state.selected_char = "astronaut"; st.rerun()
        with c3:
            st.image("https://img.icons8.com/color/200/unicorn.png", use_container_width=True)
            if st.button("Magic", use_container_width=True): 
                st.session_state.selected_char = "unicorn"; st.rerun()
    else:
        st.write(f"## Showing your {st.session_state.selected_char}!")
        if st.button("✨ SHOW DRAWING", use_container_width=True):
            arts = {
                "dinosaur": ["https://img.icons8.com/ios/500/dinosaur.png", "https://img.icons8.com/ios-filled/500/dinosaur.png", "https://img.icons8.com/external-flatart-icons-outline-flatarticons/500/external-dinosaur-dinosaur-flatart-icons-outline-flatarticons.png"],
                "astronaut": ["https://img.icons8.com/ios/500/astronaut-helmet.png", "https://img.icons8.com/ios-filled/500/astronaut-helmet.png", "https://img.icons8.com/external-outline-juicy-fish/500/external-astronaut-space-exploration-outline-outline-juicy-fish.png"],
                "unicorn": ["https://img.icons8.com/ios/500/unicorn.png", "https://img.icons8.com/ios-filled/500/unicorn.png", "https://img.icons8.com/external-outline-lafs/500/external-unicorn-fantasy-and-magic-outline-lafs.png"]
            }
            st.image(random.choice(arts[st.session_state.selected_char]), use_container_width=True)
            st.button("🖨️ PRINT NOW", use_container_width=True)

# --- 5. PUZZLE ---
elif st.session_state.mode == "puzzle":
    st.write("## Today's Riddle")
    if st.button("🎲 GET RIDDLE", use_container_width=True):
        riddles = [
            "I have keys, but no locks. I have a space, but no room. \n\n**Answer:** A Keyboard! ⌨️",
            "What has hands but cannot clap? \n\n**Answer:** A Clock! ⏰"
        ]
        st.info(f"### {random.choice(riddles)}")

# --- 6. MATH ---
elif st.session_state.mode == "math":
    st.write("## Math Magic!")
    if st.button("📝 NEW PROBLEM", use_container_width=True):
        n1, n2 = random.randint(1, 10), random.randint(1, 10)
        st.session_state.math_problem = {"q": f"{n1} + {n2} =", "a": n1 + n2}
    if st.session_state.math_problem:
        st.write(f"### {st.session_state.math_problem['q']}")
        ans = st.number_input("Answer:", min_value=0, step=1)
        if st.button("✅ CHECK", use_container_width=True):
            if ans == st.session_state.math_problem['a']: st.success("🌟 Correct!")
            else: st.warning("Try again!")

# --- 7. FACT ---
elif st.session_state.mode == "fact":
    st.write("## Fun Fact!")
    if st.button("🌟 SURPRISE ME", use_container_width=True):
        facts = ["Octopuses have three hearts! 🐙", "Honey never spoils! 🍯"]
        st.success(f"### {random.choice(facts)}")

# --- 8. HOME ---
if st.session_state.mode:
    st.write("---")
    if st.button("🏠 BACK TO MENU", use_container_width=True):
        st.session_state.mode = None
        st.session_state.selected_char = None
        st.session_state.math_problem = None
        st.rerun()
