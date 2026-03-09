import streamlit as st
from google import genai
from google.genai import types
import datetime
import random
import os

# --- 1. IPAD STYLING: Blue Background & Kiosk Button Matching ---
st.set_page_config(page_title="My Creative Buddy", layout="centered")

st.markdown("""
    <style>
    /* Medium-Dark Blue Background to match kiosk screen */
    .stApp { 
        background-color: #1E3A8A; 
    }
    
    /* Centered Text for the Menu Title */
    .menu-title {
        color: white;
        text-align: center;
        font-size: 30px;
        font-weight: bold;
        margin-top: 40px;
        margin-bottom: 20px;
    }

    /* MATCH THE KIOSK BUTTON STYLE: Dark Blue background, white text, thick border */
    div.stButton > button {
        background-color: #1E293B !important; # Very Dark Blue
        color: white !important; # White text
        border-radius: 20px !important;
        border: 4px solid #1a202c !important; # Dark gray-blue border
        font-size: 35px !important; # LARGE FONT
        font-weight: bold !important;
        height: 120px !important; # VERY TALL
        width: 100% !important;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.3);
        margin-bottom: 30px; # Spacing between buttons
        transition: transform 0.1s;
    }

    /* Touch Feedback like the kiosk */
    div.stButton > button:active {
        transform: scale(0.95);
        background-color: #0f172a !important;
    }
    
    /* General Typography matching the kiosk terminal look */
    h1, h2, h3, p, span { color: white; text-align: center; }
    
    /* Clean Kiosk look: Hide menus */
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
    # Logo removed as requested to focus on text/buttons
    # Use HTML for the menu title to ensure it blends with the new blue background
    st.markdown('<div class="menu-title">Choose an activity:</div>', unsafe_allow_html=True)
    
    # 3-Stack Layout for the buttons, filling the screen width
    col1 = st.columns(1)[0]
    with col1:
        # A. Coloring Page (A-C and big font matching kiosk)
        if st.button("🎨 A. Coloring Page", use_container_width=True): 
            st.session_state.mode = "coloring"; st.rerun()
            
        # B. Today's Puzzle
        if st.button("🧩 B. Today's Puzzle", use_container_width=True): 
            st.session_state.mode = "puzzle"; st.rerun()
            
        # C. Fun Fact (Updated text to match "A-C" scheme)
        if st.button("💡 C. Fun Fact", use_container_width=True): 
            st.session_state.mode = "fact"; st.rerun()

# --- 5. ACTIVITY: COLORING PAGE (Updated Buttons/Look) ---
elif st.session_state.mode == "coloring":
    # Temporarily change background to white for drawing mode so colors pop
    st.markdown("<style>.stApp { background-color: white; } h1,h2,h3,p,span, div { color: black; }</style>", unsafe_allow_html=True)
    
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
        
        # Reset to dark kiosk-style button for the 'Make My Page' action
        st.markdown("<style>div.stButton > button { background-color: #1E293B !important; color: white !important; font-size: 25px !important; height: 80px !important; }</style>", unsafe_allow_html=True)
        
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
    st.markdown("<style>button { background-color: white !important; color: #1E3A8A !important; }</style>", unsafe_allow_html=True)
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

# --- 7. ACTIVITY: MATH MAGIC ---
elif st.session_state.mode == "math":
    # Math magic (D. below) should keep white background for clarity
    st.markdown("<style>.stApp { background-color: white; } h1,h2,h3,p,span, div { color: black; }</style>", unsafe_allow_html=True)
    st.write("## ➕ Math Magic!")
    topic = st.radio("Choose a topic:", ["Counting", "Addition", "Subtraction"], horizontal=True)
    
    # Custom wide button for generating the problem
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
        # Ensure input fits on an iPad screen well
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
    # Use dark button for Start Over on white screens
    st.markdown("<style>#main_reset button { background-color: #1E293B !important; color: white !important; font-size: 20px !important; height: 70px !important; }</style>", unsafe_allow_html=True)
    st.write("---")
    # Home button is always visible on an iPad interface
    if st.button("🏠 START OVER", use_container_width=True, key="main_reset"):
        st.session_state.mode = None
        st.session_state.selected_char = None
        st.session_state.math_problem = None
        st.rerun()
