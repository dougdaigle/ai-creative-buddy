import streamlit as st
from google import genai
from google.genai import types
import datetime
import random

# --- 1. IPAD STYLING ---
st.set_page_config(page_title="AI Exploration for Kids", layout="centered")

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
    st.error("🔑 API Key Missing! Check Streamlit Secrets.")
    st.stop()

# --- 3. SESSION STATE ---
if 'mode' not in st.session_state: st.session_state.mode = None
if 'selected_char' not in st.session_state: st.session_state.selected_char = None
if 'math_problem' not in st.session_state: st.session_state.math_problem = None

# --- 4. MAIN MENU ---
if st.session_state.mode is None:
    st.title("🤖 My Creative Buddy")
    st.write("### AI Exploration for Kids") # Your New Slogan
    
    # 5-Button Layout
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎨 Coloring Page", use_container_width=True): 
            st.session_state.mode = "coloring"; st.rerun()
        if st.button("🧩 Today's Puzzle", use_container_width=True): 
            st.session_state.mode = "puzzle"; st.rerun()
        if st.button("📖 Story Starter", use_container_width=True): 
            st.session_state.mode = "story"; st.rerun()
    with col2:
        if st.button("💡 Fun Fact", use_container_width=True): 
            st.session_state.mode = "fact"; st.rerun()
        if st.button("➕ Math Magic", use_container_width=True): 
            st.session_state.mode = "math"; st.rerun()

# --- 5. ACTIVITY: COLORING PAGE ---
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
                            st.button("🖨️ PRINT NOW", use_container_width=True)
                except Exception:
                    st.warning("💤 The robot is taking a nap. Try again in 1 minute!")

# --- 6. ACTIVITY: STORY STARTER ---
elif st.session_state.mode == "story":
    st.write("## 📖 Start Your Adventure")
    topic = st.text_input("What should the story be about?", placeholder="Ex: A talking taco...")
    if st.button("✨ WRITE THE START", use_container_width=True):
        with st.spinner("Thinking of a story..."):
            try:
                prompt = f"Write the first 3 sentences of a fun story about {topic} for a child. End with 'What happens next?'"
                response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
                st.info(response.text)
                st.button("🖨️ PRINT STORY SHEET", use_container_width=True)
            except Exception:
                st.warning("💤 The robot is busy!")

# --- 7. ACTIVITY: TODAY'S PUZZLE ---
elif st.session_state.mode == "puzzle":
    st.write("## 🧩 The Robot's Riddle")
    if st.button("🎲 GET A NEW RIDDLE", use_container_width=True):
        with st.spinner("Thinking..."):
            try:
                prompt = "Write a very simple riddle for an elementary student. Give the riddle first, then hide the answer far below."
                response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
                st.info(response.text)
                st.button("🖨️ PRINT RIDDLE CARD", use_container_width=True)
            except Exception:
                st.warning("💤 The robot is busy right now!")

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
                st.success("🌟 AMAZING! You got it right!")
            else:
                st.warning("Try again! You can do it!")

# --- 9. ACTIVITY: FUN FACT ---
elif st.session_state.mode == "fact":
    st.write("## 💡 Learning Time!")
    if st.button("🌟 GENERATE SURPRISE", use_container_width=True):
        try:
            prompt = "One fun fact for today's date and one weird animal fact for kids. Use emojis!"
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            st.success(response.text)
        except Exception:
            st.warning("💤 Robot is busy!")

# --- 10. HOME BUTTON ---
if st.session_state.mode:
    st.write("---")
    if st.button("🏠 START OVER", use_container_width=True, key="main_reset"):
        st.session_state.mode = None
        st.session_state.selected_char = None
        st.session_state.math_problem = None
        st.rerun()
