import streamlit as st
import datetime
import random
import os

# --- 1. IPAD STYLING ---
st.set_page_config(page_title="AI Exploration for Kids", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #F8FAFF; }
    
    @keyframes logo-spin {
        0% { transform: rotate(0deg); }
        10% { transform: rotate(360deg); } 
        100% { transform: rotate(360deg); } 
    }

    [data-testid="stImage"] img {
        animation: logo-spin 10s infinite ease-in-out !important;
        max-width: 100% !important;
        height: auto !important;
    }

    @keyframes gold-glow {
        0% { border-color: #1E3A8A; box-shadow: 0px 4px 6px rgba(0,0,0,0.1); }
        50% { border-color: #FFD700; box-shadow: 0px 0px 20px #FFD700; transform: scale(1.02); }
        100% { border-color: #1E3A8A; box-shadow: 0px 4px 6px rgba(0,0,0,0.1); }
    }

    div.stButton > button {
        border-radius: 20px;
        border: 3px solid #1E3A8A;
        background-color: white;
        color: #1a202c;
        font-weight: bold;
        font-size: 22px !important;
        height: 90px !important;
        margin-bottom: 15px;
        animation: gold-glow 5s infinite ease-in-out;
    }

    [data-testid="stImage"] { background-color: transparent !important; }
    h1, h3 { color: #1E3A8A; text-align: center; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if 'mode' not in st.session_state: st.session_state.mode = None
if 'selected_char' not in st.session_state: st.session_state.selected_char = None
if 'math_problem' not in st.session_state: st.session_state.math_problem = None

# --- 3. MAIN MENU ---
if st.session_state.mode is None:
    if os.path.exists("logo.png"):
        _, mid, _ = st.columns([0.5, 5, 0.5])
        with mid: st.image("logo.png", use_container_width=True)
    else:
        st.markdown("<h1>🤖 My Creative Buddy</h1>", unsafe_allow_html=True)
    
    st.write("### Choose an activity:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎨 Coloring Page", use_container_width=True): 
            st.session_state.mode = "coloring"; st.rerun()
        if st.button("🧩 Today's Puzzle", use_container_width=True): 
            st.session_state.mode = "puzzle"; st.rerun()
    with col2:
        if st.button("💡 Fun Fact", use_container_width=True): 
            st.session_state.mode = "fact"; st.rerun()
        if st.button("➕ Math Magic", use_container_width=True): 
            st.session_state.mode = "math"; st.rerun()

# --- 4. COLORING PAGE ---
elif st.session_state.mode == "coloring":
    st.markdown("<style>button { animation: none !important; }</style>", unsafe_allow_html=True)
    if st.session_state.selected_char is None:
        st.write("## 1. Pick a Friend!")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.image("https://img.icons8.com/color/200/dinosaur.png", use_container_width=True)
            if st.button("Dinosaur", use_container_width=True): 
                st.session_state.selected_char = "dinosaur"; st.rerun()
        with c2:
            st.image("https://img.icons8.com/color/200/astronaut-helmet.png", use_container_width=True)
            if st.button("Astronaut", use_container_width=True): 
                st.session_state.selected_char = "astronaut"; st.rerun()
        with c3:
            st.image("https://img.icons8.com/color/200/unicorn.png", use_container_width=True)
            if st.button("Unicorn", use_container_width=True): 
                st.session_state.selected_char = "unicorn"; st.rerun()
    else:
        st.markdown(f"### Ready to see your **{st.session_state.selected_char.upper()}**?")
        if st.button("✨ SHOW MY PAGE ✨", use_container_width=True):
            with st.spinner("Drawing..."):
                arts = {
                    "dinosaur": ["https://img.icons8.com/ios/500/dinosaur.png", "https://img.icons8.com/ios-filled/500/dinosaur.png", "https://img.icons8.com/external-flatart-icons-outline-flatarticons/500/external-dinosaur-dinosaur-flatart-icons-outline-flatarticons.png"],
                    "astronaut": ["https://img.icons8.com/ios/500/astronaut-helmet.png", "https://img.icons8.com/ios-filled/500/astronaut-helmet.png", "https://img.icons8.com/external-outline-juicy-fish/500/external-astronaut-space-exploration-outline-outline-juicy-fish.png"],
                    "unicorn": ["https://img.icons8.com/ios/500/unicorn.png", "https://img.icons8.com/ios-filled/500/unicorn.png", "https://img.icons8.com/external-outline-lafs/500/external-unicorn-fantasy-and-magic-outline-lafs.png"]
                }
                st.image(random.choice(arts[st.session_state.selected_char]), use_container_width=True)
                st.button("🖨️ PRINT NOW", use_container_width=True)

# --- 5. PUZZLE ---
elif st.session_state.mode == "puzzle":
    st.markdown("<style>button { animation: none !important; }</style>", unsafe_allow_html=True)
    st.write("## 🧩 The Robot's Riddle")
    if st.button("🎲 GET A NEW RIDDLE", use_container_width=True):
        riddles = [
            "I have keys, but no locks. I have a space, but no room. You can enter, but never leave. \n\n**Answer:** A Keyboard! ⌨️",
            "What has to be broken before you can use it? \n\n**Answer:** An Egg! 🥚",
            "What has hands but cannot clap? \n\n**Answer:** A Clock! ⏰"
        ]
        st.info(f"### Riddle:\n{random.choice(riddles)}")
        st.button("🖨️ PRINT RIDDLE CARD", use_container_width=True)

# --- 6. MATH MAGIC (LIVE) ---
elif st.session_state.mode == "math":
    st.markdown("<style>button { animation: none !important; }</style>", unsafe_allow_html=True)
    st.write("## ➕ Math Magic!")
    topic = st.radio("Topic:", ["Counting", "Addition", "Subtraction"], horizontal=True)
    if st.button("📝 GENERATE PROBLEM", use_container_width=True):
        n1, n2 = random.randint(1, 10), random.randint(1, 10)
        if topic == "Counting": st.session_state.math_problem = {"q": f"Count the stars: {'⭐' * n1}", "a": n1}
        elif topic == "Addition": st.session_state.math_problem = {"q": f"{n1} + {n2} =", "a": n1 + n2}
        else: st.session_state.math_problem = {"q": f"{max(n1,n2)} - {min(n1,n2)} =", "a": abs(n1-n2)}
    if st.session_state.math_problem:
        st.write(f"### {st.session_state.math_problem['q']}")
        ans = st.number_input("Your Answer:", min_value=0, step=1)
        if st.button("✅ CHECK", use_container_width=True):
            if ans == st.session_state.math_problem['a']: st.success("🌟 Amazing!")
            else: st.warning("Try again!")

# --- 7. FUN FACT ---
elif st.session_state.mode == "fact":
    st.markdown("<style>button { animation: none !important; }</style>", unsafe_allow_html=True)
    st.write("## 💡 Learning Time!")
    if st.button("🌟 SURPRISE ME", use_container_width=True):
        facts = [
            "A group of flamingos is called a **flamboyance**! 🦩",
            "Honey never spoils. Archaeologists found some 3,000 years old! 🍯",
            "Octopuses have **three hearts** and blue blood! 🐙"
        ]
        st.success(f"### Did you know?\n\n{random.choice(facts)}")
        st.button("🖨️ PRINT FACT STRIP", use_container_width=True)

# --- 8. HOME BUTTON ---
if st.session_state.mode:
    st.write("---")
    if st.button("🏠 START OVER", use_container_width=True):
        st.session_state.mode = None
        st.session_state.selected_char = None
        st.session_state.math_problem = None
        st.rerun()
