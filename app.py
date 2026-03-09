import streamlit as st
from google import genai
from google.genai import types
from streamlit_lottie import st_lottie
import requests
import datetime
import random

# --- 1. IPAD STYLING & ANIMATION SETUP ---
st.set_page_config(page_title="My Creative Buddy", layout="centered")

def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

lottie_celebration = load_lottie("https://assets5.lottiefiles.com/packages/lf20_u4yrau.json")

st.markdown("""
    <style>
    .stApp { background-color: #F0F5FF; }
    h1, h2, h3 { color: #1E3A8A; text-align: center; }
    div.stButton > button {
        border-radius: 20px;
        border: 3px solid #1E3A8A;
        background-color: white;
        color: #1a202c;
        font-weight: bold;
        font-size: 20px !important;
        height: 80px !important;
    }
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

# --- 3. SESSION STATE (The Star Chart Logic) ---
if 'mode' not in st.session_state: st.session_state.mode = None
if 'selected_char' not in st.session_state: st.session_state.selected_char = None
if 'math_problem' not in st.session_state: st.session_state.math_problem = None

# Track stars for each activity
if 'stars' not in st.session_state:
    st.session_state.stars = {"Color": False, "Fact": False, "Puzzle": False, "Math": False}

# --- 4. THE STAR CHART DISPLAY ---
def show_star_chart():
    st.write("### 🌟 Your Progress 🌟")
    cols = st.columns(4)
    for i, (activity, done) in enumerate(st.session_state.stars.items()):
        with cols[i]:
            icon = "⭐" if done else "⚪"
            st.markdown(f"<h2 style='text-align: center;'>{icon}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'>{activity}</p>", unsafe_allow_html=True)

# --- 5. MAIN MENU ---
if st.session_state.mode is None:
    st.title("🤖 My Creative Buddy!")
    show_star_chart()
    st.write("---")
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

# --- 6. ACTIVITY: COLORING PAGE ---
elif st.session_state.mode == "coloring":
    if st.session_state.selected_char is None:
        st.write("## 1. Pick a Friend!")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.image("https://img.icons8.com/color/200/dinosaur.png", use_container_width=True)
            if st.button("Dinosaur", use_container_width=True): 
                st.session_state.selected_char = "a friendly dinosaur"; st.rerun()
        with c2:
            st.image("https://img.icons8.com/color/200/astronaut-helmet.png", use_container_width=True)
            if st.button("Astronaut", use_container_width=True): 
                st.session_state.selected_char = "a brave astronaut"; st.rerun()
        with c3:
            st.image("https://img.icons8.com/color/200/unicorn.png", use_container_width=True)
            if st.button("Unicorn", use_container_width=True): 
                st.session_state.selected_char = "a magic unicorn"; st.rerun()
    else:
        st.markdown(f"### Ready to draw your **{st.session_state.selected_char.upper()}**?")
        if st.button("✨ MAKE MY PAGE ✨", use_container_width=True):
            with st.spinner("Drawing..."):
                try:
                    response = client.models.generate_content(
                        model='gemini-3.1-flash-image-preview',
                        contents=f"Kids coloring book page, black and white line art of {st.session_state.selected_char}. Thick outlines, no shading.",
                        config=types.GenerateContentConfig(response_modalities=["IMAGE"])
                    )
                    for part in response.parts:
                        if part.inline_data:
                            st.image(part.as_image(), use_container_width=True)
                            st.session_state.stars["Color"] = True # Earn a star!
                            st.button("🖨️ PRINT NOW", use_container_width=True)
                except Exception:
                    st.warning("💤 The robot is taking a nap!")

# --- 7. ACTIVITY: TODAY'S PUZZLE ---
elif st.session_state.mode == "puzzle":
    st.write("## 🧩 The Robot's Riddle")
    if st.button("🎲 GET A NEW RIDDLE", use_container_width=True):
        try:
            prompt = "A simple riddle for a child. Include the answer hidden at the bottom."
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            st.info(response.text)
            st.session_state.stars["Puzzle"] = True # Earn a star!
        except Exception:
            st.warning("💤 The robot is busy!")

# --- 8. ACTIVITY: MATH MAGIC ---
elif st.session_state.mode == "math":
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
                st_lottie(lottie_celebration, height=200, key="math_celebration")
                st.success("🌟 AMAZING! You got it right!")
                st.session_state.stars["Math"] = True # Earn a star!
            else:
                st.warning("Try again! You can do it!")

# --- 9. ACTIVITY: FUN FACT ---
elif st.session_state.mode == "fact":
    st.write("## 💡 Learning Time!")
    if st.button("🌟 GENERATE SURPRISE", use_container_width=True):
        try:
            prompt = "One fun fact for kids."
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            st.success(response.text)
            st.session_state.stars["Fact"] = True # Earn a star!
        except Exception:
            st.warning("💤 Robot is busy!")

# --- 10. HOME BUTTON (Wipes everything for the next student) ---
if st.session_state.mode:
    st.write("---")
    if st.button("🏠 START OVER", use_container_width=True, key="main_reset"):
        # Reset everything back to default
        st.session_state.mode = None
        st.session_state.selected_char = None
        st.session_state.math_problem = None
        st.session_state.stars = {"Color": False, "Fact": False, "Puzzle": False, "Math": False}
        st.rerun()
