import streamlit as st
from google import genai
from google.genai import types
import datetime
import random
import os

# --- 1. IPAD STYLING: SELECTIVE SPIN & GOLD PULSE ---
st.set_page_config(page_title="AI Exploration for Kids", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #F8FAFF; }
    
    /* 1. LOGO SPIN ANIMATION (Targeted to the header area only) */
    @keyframes logo-spin {
        0% { transform: rotate(0deg); }
        10% { transform: rotate(360deg); } 
        100% { transform: rotate(360deg); } 
    }

    /* This selector only targets the logo on the Home Page */
    .home-logo img {
        animation: logo-spin 10s infinite ease-in-out !important;
        max-width: 100% !important;
        height: auto !important;
    }

    /* 2. GOLD BUTTON PULSE ANIMATION */
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
        transition: all 0.3s ease;
        animation: gold-glow 5s infinite ease-in-out;
    }

    /* Ensure all image containers remain transparent */
    [data-testid="stImage"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    h1, h3 { color: #1E3A8A; text-align: center; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
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

# --- 4. MAIN MENU ---
if st.session_state.mode is None:
    if os.path.exists("logo.png"):
        _, mid, _ = st.columns([0.5, 5, 0.5])
        with mid:
            # Wrapped in a div class 'home-logo' so ONLY this image spins
            st.markdown('<div class="home-logo">', unsafe_allow_html=True)
            st.image("logo.png", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
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

# --- 5. ACTIVITY: COLORING PAGE (DEMO MODE) ---
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
                demo_images = {
                    "dinosaur": "https://img.icons8.com/ios/500/dinosaur.png",
                    "astronaut": "https://img.icons8.com/ios/500/astronaut-helmet.png",
                    "unicorn": "https://img.icons8.com/ios/500/unicorn.png"
                }
                # No 'home-logo' class here, so these stay static
                st.image(demo_images[st.session_state.selected_char], use_container_width=True)
                st.button("🖨️ PRINT NOW", use_container_width=True)

# --- 6. ACTIVITY: TODAY'S PUZZLE ---
elif st.session_state.mode == "puzzle":
    st.markdown("<style>button { animation: none !important; }</style>", unsafe_allow_html=True)
    st.write("## 🧩 The Robot's Riddle")
    if st.button("🎲 GET A NEW RIDDLE", use_container_width=True):
        with st.spinner("Thinking..."):
            try:
                prompt = "Write a simple riddle for a child."
                response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
                st.info(response.text)
            except Exception:
                st.warning("💤 The robot is busy!")

# --- 7. ACTIVITY: MATH MAGIC ---
elif st.session_state.mode == "math":
    st.markdown("<style>button { animation: none !important; }</style>", unsafe_allow_html=True)
    st.write("## ➕ Math Magic!")
    topic = st.radio("Choose a topic:", ["Counting", "Addition", "Subtraction"], horizontal=True)
    if st.button("📝 GENERATE PROBLEM", use_container_width=True):
        num1, num2 = random.randint(1, 10), random.randint(1, 10)
        if topic == "Counting":
            st.session_state.math_problem = {"q": f"Count the stars: {'⭐' * num1}", "a": num1}
        elif topic == "Addition":
            st.session_state.math_problem = {"q": f"What is {num1} + {num2}?", "a": num1 + num2}
        else:
            high, low = max(num1, num2), min(num1, num2)
            st.session_state.math_problem = {"q": f"What is {high} - {low}?", "a": high - low}
    if st.session_state.math_problem:
        st.write(f"### {st.session_state.math_problem['q']}")
        user_ans = st.number_input("Your Answer:", min_value=0, step=1)
        if st.button("✅ CHECK ANSWER", use_container_width=True):
            if user_ans == st.session_state.math_problem['a']:
                st.success("🌟 AMAZING! You got it right!")
            else:
                st.warning("Try again!")

# --- 8. ACTIVITY: FUN FACT ---
elif st.session_state.mode == "fact":
    st.markdown("<style>button { animation: none !important; }</style>", unsafe_allow_html=True)
    st.write("## 💡 Learning Time!")
    if st.button("🌟 GENERATE SURPRISE", use_container_width=True):
        try:
            prompt = "One fun fact for kids."
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            st.success(response.text)
        except Exception:
            st.warning("💤 Robot is busy!")

# --- 9. HOME BUTTON ---
if st.session_state.mode:
    st.write("---")
    if st.button("🏠 START OVER", use_container_width=True, key="main_reset"):
        st.session_state.mode = None
        st.session_state.selected_char = None
        st.session_state.math_problem = None
        st.rerun()
