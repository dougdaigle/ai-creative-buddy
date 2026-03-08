import streamlit as st
import os
from google import genai
from google.genai import types

# --- 1. PREMIUM KIOSK STYLING ---
st.set_page_config(page_title="Creative Buddy AI", layout="wide")

# Custom CSS for a polished, "App-like" look
st.markdown("""
    <style>
    /* Import a friendly font */
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Fredoka', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Hero Header Area */
    .hero-text {
        text-align: center;
        color: #1E3A8A;
        padding: 20px;
    }

    /* Huge Rounded Buttons */
    div.stButton > button:first-child {
        background-color: #ffffff;
        color: #1E3A8A;
        height: 8em;
        width: 100%;
        border-radius: 30px;
        font-size: 24px;
        font-weight: 600;
        border: none;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    div.stButton > button:hover {
        transform: translateY(-5px);
        box-shadow: 0px 15px 30px rgba(0,0,0,0.15);
        background-color: #1E3A8A;
        color: white;
    }

    /* Styled Input Boxes */
    .stTextInput input {
        border-radius: 20px;
        border: 2px solid #1E3A8A;
        padding: 10px 20px;
    }

    /* Hide technical UI elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. AI CLIENT SETUP ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("🔑 Please add GEMINI_API_KEY to your Secrets.")
    st.stop()

# --- 3. APP HEADER ---
st.markdown('<div class="hero-text"><h1>🤖 My Creative Buddy</h1><p>The AI Library Station</p></div>', unsafe_allow_html=True)

if 'mode' not in st.session_state:
    st.session_state.mode = None

# --- 4. MAIN MENU (Centered Cards) ---
if st.session_state.mode is None:
    st.write("## Choose your adventure!")
    # Use empty columns to center the buttons
    _, col_mid, _ = st.columns([1, 4, 1])
    
    with col_mid:
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🎨\nColoring\nPage"):
                st.session_state.mode = "coloring"
        with c2:
            if st.button("📸\nCool\nCaricature"):
                st.session_state.mode = "caricature"
        with c3:
            if st.button("💡\nFun\nFact"):
                st.session_state.mode = "fact"

# --- 5. ACTIVITY: COLORING PAGE ---
if st.session_state.mode == "coloring":
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        st.markdown("### 🎨 Create a Coloring Sheet")
        prompt = st.text_input("What should the robot draw?", placeholder="e.g. A space dinosaur")
        
        if st.button("✨ GENERATE"):
            with st.spinner("Drawing your masterpiece..."):
                try:
                    response = client.models.generate_content(
                        model='gemini-3.1-flash-image-preview',
                        contents=f"Kids coloring book page, black and white line art of {prompt}. Thick outlines, no shading, white background.",
                        config=types.GenerateContentConfig(response_modalities=["IMAGE"])
                    )
                    for part in response.parts:
                        if part.inline_data:
                            st.image(part.as_image(), use_container_width=True)
                            st.success("Tada! Ready to print.")
                            st.button("🖨️ SEND TO PRINTER")
                except Exception as e:
                    st.error("The robot is resting. Try a different idea!")

# --- 6. ACTIVITY: FUN FACT ---
elif st.session_state.mode == "fact":
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        st.markdown("### 💡 Today's Fun Facts")
        st.info("**On This Day (March 8):** International Women's Day!")
        st.success("**Animal Fact:** A snail can sleep for three years!")
        st.button("🖨️ PRINT FACT STRIP")

# --- 7. HOME BUTTON ---
if st.session_state.mode is not None:
    st.write("---")
    if st.button("🏠 BACK TO MENU"):
        st.session_state.mode = None
        st.rerun()
