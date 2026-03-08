import streamlit as st
import os
from google import genai
from google.genai import types

# --- 1. KIOSK STYLING (CSS) ---
# This makes the app look like a professional machine rather than a website
st.set_page_config(page_title="My Creative Buddy", layout="centered")

st.markdown("""
    <style>
    /* Main Background color */
    .stApp {
        background-color: #F0F5FF;
    }
    /* Make Buttons Massive, Colorful, and Easy to Touch */
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
        white-space: pre-line; /* Allows the emoji to be on a different line */
    }
    /* Change button color when touched/hovered */
    div.stButton > button:hover {
        background-color: #FFD700;
        color: #31333F;
        border: 5px solid #FF4B4B;
    }
    /* Hide the technical menus from the kids */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. AI CLIENT SETUP ---
# This connects to the "brain" of the kiosk using your secret API key
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("🔑 Missing API Key! Go to Streamlit Settings > Secrets and add: GEMINI_API_KEY = 'your_key_here'")
    st.stop()

# --- 3. APP NAVIGATION ---
if 'mode' not in st.session_state:
    st.session_state.mode = None

st.title("🤖 My Creative Buddy!")
st.write("### What should we make today?")

# --- 4. HOME MENU ---
if st.session_state.mode is None:
    # Creating 3 big columns for the main buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🎨\nColor"):
            st.session_state.mode = "coloring"
    with col2:
        if st.button("📸\nFace"):
            st.session_state.mode = "caricature"
    with col3:
        if st.button("💡\nFact"):
            st.session_state.mode = "fact"

# --- 5. ACTIVITY: COLORING PAGE ---
if st.session_state.mode == "coloring":
    st.divider()
    prompt = st.text_input("What do you want to color?", placeholder="Ex: A space cat...")
    
    if st.button("CREATE MASTERPIECE"):
        with st.spinner("🎨 Your robot buddy is drawing..."):
            try:
                # March 2026 Model Name & Settings
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
                
                # Show the resulting image
                for part in response.parts:
                    if part.inline_data:
                        st.image(part.as_image(), use_container_width=True)
                        st.success("Ready to print!")
                        # This would connect to your kiosk printer
                        st.button("🖨️ PRINT NOW")
            
            except Exception as e:
                st.error("Oh no! The robot got shy. Try a different idea!")
                st.write(f"Tech detail for you: {str(e)}")

# --- 6. ACTIVITY: FUN FACT ---
elif st.session_state.mode == "fact":
    st.divider()
    st.write("### 📅 On This Day: March 8th")
    st.info("Today is International Women's Day! It's a day to celebrate all the amazing women who have changed the world.")
    st.write("---")
    st.write("### 🐙 Weird Animal Fact:")
    st.success("An octopus has 3 hearts, 9 brains, and blue blood! They are like aliens of the ocean.")
    st.button("🖨️ PRINT FACT STRIP")

# --- 7. RESTART BUTTON ---
if st.session_state.mode is not None:
    st.write("---")
    if st.button("🏠 START OVER"):
        st.session_state.mode = None
        st.rerun()
