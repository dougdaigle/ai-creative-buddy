import streamlit as st
import os
import random
import datetime
from google import genai
from google.genai import types

# --- 1. IPAD STYLING & CARD LAYOUT ---
st.set_page_config(page_title="My Creative Buddy", layout="centered")

st.markdown("""
    <style>
    /* Blending the background and removing the top header */
    .stApp { 
        background-color: #F8FAFF; 
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* Styling for the Main Menu "Cards" */
    /* This section removes the 'boxed' look and creates the transparent feel */
    [data-testid="stVerticalBlock"] > div:has(button) {
        text-align: center;
        background-color: white;
        border-radius: 25px;
        padding: 20px;
        # Removed the solid border that was present before
        # border: 3px solid #1E3A8A; 
        box-shadow: 0px 4px 15px rgba(0,0,0,0.08); # Softer shadow
        transition: transform 0.2s; # Fun 'pop' when touched
    }
    [data-testid="stVerticalBlock"] > div:has(button):active {
        transform: scale(0.95); # Touch feedback
    }

    /* Making the text inside cards dark and readable */
    h1, h2, h3, p { color: #1E3A8A; text-align: center; }

    /* Centering the images/icons inside the cards */
    .stImage > img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        margin-bottom: 10px;
    }
    
    /* iPad Touch Optimization for inner elements (if any) */
    .stNumberInput input, .stTextInput input {
        border-radius: 15px !important;
        border: 2px solid #1E3A8A !important;
        text-align: center;
    }
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
    # Centering and Displaying Logo
    if os.path.exists("logo.png"):
        _, mid, _ = st.columns([1, 2, 1])
        with mid:
            st.image("logo.png", use_container_width=True)
    else:
        st.title("🤖 My Creative Buddy")
    
    st.write("### Choose your creative adventure!")
    st.write("Click a card to begin:")
    
    # 2x2 Grid using columns for the iPad
    col1, col2 = st.columns(2)
    
    with col1:
        # Card 1: Coloring Page
        st.image("https://img.icons8.com/color/200/paint-palette.png", width=120)
        st.markdown("### Coloring Page")
        # In a real app, this whole container is the touch target.
        if st.button("Start coloring!", key="start_color", use_container_width=True): 
            st.session_state.mode = "coloring"; st.rerun()

        # Card 3: Puzzle
        st.write("---")
        st.image("https://img.icons8.com/color/200/puzzle.png", width=120)
        st.markdown("### Today's Puzzle")
        if st.button("What's the riddle?", key="start_puzzle", use_container_width=True): 
            st.session_state.mode = "puzzle"; st.rerun()

    with col2:
        # Card 2: Fun Fact
        st.image("https://img.icons8.com/color/200/idea.png", width=120)
        st.markdown("### Fun Fact")
        if st.button("Tell me something new!", key="start_fact", use_container_width=True): 
            st.session_state.mode = "fact"; st.rerun()

        # Card 4: Math
        st.write("---")
        st.image("https://img.icons8.com/color/200/plus-math.png", width=120)
        st.markdown("### Math Magic")
        if st.button("Let's do math!", key="start_math", use_container_width=True): 
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
        # Re-using the huge touch-friendly button look for consistency in activities
        st.markdown("""<style>div.stButton > button { border-radius: 20px; border: 3px solid #1E3A8A; background-color: white; color: #1E3A8A; font-weight: bold; font-size: 20px !important; height: 80px !important; }</style>""", unsafe_allow_html=True)
        
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

# --- 6. ACTIVITY: TODAY'S PUZZLE ---
elif st.session_state.mode == "puzzle":
    st.write("## 🧩 The Robot's Riddle")
    if st.button("🎲 GET A NEW RIDDLE", use_container_width=True):
        with st.spinner("Thinking..."):
            try:
                prompt = "Write a very simple riddle for an elementary student. Give the riddle first, then hide the answer far below."
                response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
                st.info(response.text)
            except Exception:
                st.warning("💤 The robot is busy right now!")

# --- 7. ACTIVITY: MATH MAGIC ---
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

# --- 8. ACTIVITY: FUN FACT ---
elif st.session_state.mode == "fact":
    st.write("## 💡 Learning Time!")
    if st.button("🌟 GENERATE SURPRISE", use_container_width=True):
        try:
            prompt = "One fun fact for today's date and one weird animal fact for kids. Use emojis!"
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            st.success(response.text)
        except Exception:
            st.warning("💤 Robot is busy! Try again soon.")

# --- 9. HOME BUTTON ---
if st.session_state.mode:
    st.write("---")
    # Using the standard primary button style for the home button
    if st.button("🏠 START OVER", use_container_width=True, key="main_reset"):
        st.session_state.mode = None
        st.session_state.selected_char = None
        st.session_state.math_problem = None
        st.rerun()
