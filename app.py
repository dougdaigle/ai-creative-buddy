import streamlit as st
import os
from google import genai
from google.genai import types

# --- 1. KIOSK STYLING (CSS) ---
# This transforms the website into a kid-friendly kiosk interface
st.set_page_config(page_title="My Creative Buddy", layout="centered")

st.markdown("""
    <style>
    /* Background color for the whole app */
    .stApp {
        background-color: #F0F5FF;
    }
    /* Style for the massive touch-friendly buttons */
    div.stButton > button:first-child {
        background-color: #FF4B4B;
        color: white;
        height: 5em;
        width: 100%;
        border-radius: 25px;
        font-size: 28px;
        font-weight: bold;
        border: 5px solid #FFFFFF;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        white-space: pre-line;
    }
    /* Interactive hover/touch effect */
    div.stButton > button:hover {
        background-color: #FFD700;
        color: #31333F;
        border: 5px solid #FF4B4B;
    }
    /* Hide top bar and footer for an immersive look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. AI CLIENT SETUP ---
# Securely connects to Gemini using your secret key
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("🔑 API Key Missing! Please add 'GEMINI_API_KEY' to your Streamlit Secrets.")
    st.stop()

# --- 3. APP NAVIGATION LOGIC ---
if 'mode' not in st.session_state:
    st.session_state.mode = None

st.title("🤖 My Creative Buddy!")
st.write("### What should we make today?")

# --- 4. THE MAIN MENU ---
if st.session_state.mode is None:
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🎨\nColoring\nPage"):
            st.session_state.mode = "coloring"
    with col2:
        if st.button("📸\nCool\nCaricature"):
            st.session_state.mode = "caricature"
    with col3:
        if st.button("💡\nFun\nFact"):
            st.session_state.mode = "fact"

# --- 5. ACTIVITY: COLORING PAGE ---
if st.session_state.mode == "coloring":
    st.divider()
    prompt = st.text_input("What do you want to color?", placeholder="Ex: A dragon playing soccer...")
    
    if st.button("CREATE MASTERPIECE"):
        with st.spinner("🎨 Your robot buddy is drawing..."):
            try:
                # March 2026 Image Generation Model
                response = client.models.generate_content(
                    model='gemini-3.1-flash-image-preview',
                    contents=f"Kids coloring book page, black and white line art of {prompt}. Thick outlines, no shading, white background.",
                    config=types.GenerateContentConfig(
                        response_modalities=["IMAGE"],
                        safety_settings=[
                            types.SafetySetting(category="HATE_SPEECH", threshold="BLOCK_ONLY_HIGH"),
                            types.SafetySetting(category="HARASSMENT", threshold="BLOCK_ONLY_HIGH")
                        ]
                    )
                )
                
                # Extract and display the image
                for part in response.parts:
                    if part.inline_data:
                        st.image(part.as_image(), use_container_width=True)
                        st.success("Ready to print!")
                        st.button("🖨️ PRINT NOW")
            
            except Exception as e:
                st.error("The robot is feeling a bit shy. Try a different idea!")
                st.write(f"Log: {str(e)}")

# --- 6. ACTIVITY: FUN FACT ---
elif st.session_state.mode == "fact":
    st.divider()
    # Updated to today's date: March 8
    st.write("### 📅 On This Day: March 8th")
    st.info("Today is International Women's Day! A day to celebrate all the incredible women who have shaped our world.")
    st.write("---")
    st.write("### 🐙 Weird Animal Fact:")
    st.success("An octopus has 3 hearts and 9 brains! They even have blue blood.")
    st.button("🖨️ PRINT FACT STRIP")

# --- 7. HOME BUTTON ---
if st.session_state.mode is not None:
    st.write("---")
    if st.button("🏠 START OVER"):
        st.session_state.mode = None
        st.rerun()
