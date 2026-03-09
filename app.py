import streamlit as st
from google import genai
from google.genai import types

# --- 1. KIOSK STYLING ---
st.set_page_config(page_title="My Creative Buddy", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #F0F5FF; }
    /* Style for the Picture Cards */
    [data-testid="stVerticalBlock"] > div:has(button) {
        text-align: center;
    }
    /* Make selection buttons look like "Cards" */
    div.stButton > button {
        border-radius: 20px;
        border: 3px solid #1E3A8A;
        background-color: white;
        color: #1a202c;
        transition: 0.3s;
    }
    div.stButton > button:active {
        background-color: #FFD700;
        transform: scale(0.95);
    }
    h1, h2, h3 { color: #1E3A8A; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. AI CLIENT SETUP ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("🔑 API Key Missing in Secrets!")
    st.stop()

# --- 3. APP LOGIC ---
if 'mode' not in st.session_state:
    st.session_state.mode = None
if 'selected_char' not in st.session_state:
    st.session_state.selected_char = None

st.title("🤖 My Creative Buddy!")

# --- 4. MAIN MENU ---
if st.session_state.mode is None:
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🎨\nColoring\nPage"): st.session_state.mode = "coloring"
    with col2:
        if st.button("📸\nFace\nCaricature"): st.session_state.mode = "caricature"
    with col3:
        if st.button("💡\nFun\nFact"): st.session_state.mode = "fact"

# --- 5. ACTIVITY: PICTURE SELECTION ---
if st.session_state.mode == "coloring":
    st.write("## 1. Pick a Friend!")
    
    # Create a grid of 3 pictures
    char_col1, char_col2, char_col3 = st.columns(3)
    
    with char_col1:
        st.image("https://img.icons8.com/color/200/dinosaur.png", width=150)
        if st.button("Dinosaur"): st.session_state.selected_char = "a friendly dinosaur"
        
    with char_col2:
        st.image("https://img.icons8.com/color/200/astronaut-helmet.png", width=150)
        if st.button("Astronaut"): st.session_state.selected_char = "a brave astronaut"
        
    with char_col3:
        st.image("https://img.icons8.com/color/200/unicorn.png", width=150)
        if st.button("Unicorn"): st.session_state.selected_char = "a magic unicorn"

    # Show what is selected
    if st.session_state.selected_char:
        st.success(f"You picked: **{st.session_state.selected_char.upper()}**")
        
        st.write("## 2. Ready to Draw?")
        if st.button("✨ MAKE MY COLORING PAGE ✨"):
            with st.spinner("Drawing..."):
                try:
                    response = client.models.generate_content(
                        model='gemini-3.1-flash-image-preview',
                        contents=f"Simple kids coloring book page, black and white line art of {st.session_state.selected_char}. Thick outlines, no shading, white background.",
                        config=types.GenerateContentConfig(response_modalities=["IMAGE"])
                    )
                    for part in response.parts:
                        if part.inline_data:
                            st.image(part.as_image(), use_container_width=True)
                            st.button("🖨️ PRINT NOW")
                except Exception as e:
                    st.error("The robot is busy! Try again in a minute.")

# --- 6. HOME BUTTON ---
if st.session_state.mode is not None:
    st.write("---")
    if st.button("🏠 START OVER"):
        st.session_state.mode = None
        st.session_state.selected_char = None
        st.rerun()
