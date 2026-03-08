import streamlit as st
import os
from google import genai
from google.genai import types

# --- 1. KIOSK STYLING ---
st.set_page_config(page_title="My Creative Buddy", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #F0F5FF; }
    div.stButton > button:first-child {
        background-color: #FF4B4B;
        color: white;
        height: 5em;
        width: 100%;
        border-radius: 25px;
        font-size: 24px;
        font-weight: bold;
        border: 5px solid #FFFFFF;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.1);
    }
    h1, h2, h3 { color: #1E3A8A; text-align: center; }
    /* Style the dropdown labels to be dark and readable */
    label { color: #1E3A8A !important; font-size: 18px !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. AI CLIENT SETUP ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("🔑 API Key Missing! Add it to Streamlit Secrets.")
    st.stop()

# --- 3. APP NAVIGATION ---
if 'mode' not in st.session_state:
    st.session_state.mode = None

st.title("🤖 My Creative Buddy!")

# --- 4. MAIN MENU ---
if st.session_state.mode is None:
    st.subheader("What do you want to make today?")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🎨\nColoring\nPage"):
            st.session_state.mode = "coloring"
    with col2:
        if st.button("📸\nFace\nCaricature"):
            st.session_state.mode = "caricature"
    with col3:
        if st.button("💡\nFun\nFact"):
            st.session_state.mode = "fact"

# --- 5. ACTIVITY: MIX & MATCH COLORING ---
if st.session_state.mode == "coloring":
    st.divider()
    st.subheader("🎨 Mix & Match Your Drawing!")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        character = st.selectbox(
            "Pick a Character:",
            ["A Friendly Dinosaur", "A Brave Astronaut", "A Magic Unicorn", 
             "A Cool Robot", "A Scuba Diving Cat", "A Flying Dragon"]
        )
        
    with col_b:
        setting = st.selectbox(
            "Pick a Setting:",
            ["in Outer Space", "under the Ocean", "in a Candy Kingdom", 
             "at a Jungle Party", "on a Skateboard", "eating a Giant Pizza"]
        )

    # The AI will combine these two selections
    combined_prompt = f"{character} {setting}"
    st.info(f"The Robot will draw: **{combined_prompt}**")

    if st.button("✨ GENERATE COLORING PAGE"):
        with st.spinner("🎨 Your robot buddy is drawing..."):
            try:
                response = client.models.generate_content(
                    model='gemini-3.1-flash-image-preview',
                    contents=f"Simple kids coloring book page, black and white line art of {combined_prompt}. Thick outlines, no shading, white background.",
                    config=types.GenerateContentConfig(response_modalities=["IMAGE"])
                )
                
                for part in response.parts:
                    if part.inline_data:
                        st.image(part.as_image(), use_container_width=True)
                        st.success("Tada! Ready to print.")
                        st.button("🖨️ PRINT MY PAGE")
            
            except Exception as e:
                # Quota check logic
                if "429" in str(e):
                    st.warning("💤 The robot is taking a nap. Try again in 1 minute!")
                else:
                    st.error("The robot got stuck. Try a different combo!")

# --- 6. HOME BUTTON ---
if st.session_state.mode is not None:
    st.write("---")
    if st.button("🏠 START OVER"):
        st.session_state.mode = None
        st.rerun()
