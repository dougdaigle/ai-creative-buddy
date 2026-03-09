import streamlit as st
from google import genai
from google.genai import types
import datetime

# --- 1. IPAD STYLING ---
st.set_page_config(page_title="My Creative Buddy", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #F0F5FF; }
    h1, h2, h3 { color: #1E3A8A; text-align: center; }
    
    /* Massive Touch Buttons for iPad */
    div.stButton > button {
        border-radius: 20px;
        border: 3px solid #1E3A8A;
        background-color: white;
        color: #1a202c;
        font-weight: bold;
        font-size: 20px !important;
        height: 80px !important;
        use-container-width: true;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. AI CLIENT SETUP ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("🔑 API Key Missing!")
    st.stop()

# --- 3. SESSION STATE INITIALIZATION ---
# This part "remembers" what the kid clicked so we don't need double-clicks
if 'mode' not in st.session_state:
    st.session_state.mode = None
if 'selected_char' not in st.session_state:
    st.session_state.selected_char = None

# --- 4. MAIN MENU ---
if st.session_state.mode is None:
    st.title("🤖 My Creative Buddy!")
    st.write("### Choose an activity:")
    if st.button("🎨 Coloring Page", use_container_width=True): 
        st.session_state.mode = "coloring"
        st.rerun() # Instant switch
    if st.button("📸 Face Caricature", use_container_width=True): 
        st.session_state.mode = "caricature"
        st.rerun()
    if st.button("💡 Fun Fact", use_container_width=True): 
        st.session_state.mode = "fact"
        st.rerun()

# --- 5. ACTIVITY: COLORING PAGE ---
elif st.session_state.mode == "coloring":
    # If no character is picked yet, show the gallery
    if st.session_state.selected_char is None:
        st.write("## 1. Pick a Friend!")
        char_col1, char_col2, char_col3 = st.columns(3)
        
        with char_col1:
            st.image("https://img.icons8.com/color/200/dinosaur.png", use_container_width=True)
            if st.button("Dinosaur", use_container_width=True): 
                st.session_state.selected_char = "a friendly dinosaur"
                st.rerun() # This forces the immediate jump to the draw screen
        with char_col2:
            st.image("https://img.icons8.com/color/200/astronaut-helmet.png", use_container_width=True)
            if st.button("Astronaut", use_container_width=True): 
                st.session_state.selected_char = "a brave astronaut"
                st.rerun()
        with char_col3:
            st.image("https://img.icons8.com/color/200/unicorn.png", use_container_width=True)
            if st.button("Unicorn", use_container_width=True): 
                st.session_state.selected_char = "a magic unicorn"
                st.rerun()

    # Once a character is picked, show the "Generate" screen
    else:
        st.markdown(f"### Ready to draw your **{st.session_state.selected_char.upper()}**?")
        if st.button("✨ MAKE MY PAGE ✨", use_container_width=True):
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
                            st.button("🖨️ PRINT NOW", use_container_width=True)
                except Exception as e:
                    if "429" in str(e):
                        st.warning("💤 Robot is napping. Wait 1 minute!")
                    else:
                        st.error("Robot error! Please check billing in AI Studio.")
        
        if st.button("⬅️ Pick a different character", use_container_width=True):
            st.session_state.selected_char = None
            st.rerun()

# --- 6. ACTIVITY: FUN FACT ---
elif st.session_state.mode == "fact":
    st.write("## 💡 Learning Time!")
    today = datetime.date.today().strftime("%B %d")
    
    if st.button("🌟 GENERATE TODAY'S SURPRISE 🌟", use_container_width=True):
        with st.spinner("Searching..."):
            try:
                prompt = f"Give me one fun 'On This Day' fact for {today} and one weird animal fact. Keep it simple for kids. Use emojis!"
                response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
                st.markdown(f"### {today} is special!")
                st.success(response.text)
                st.button("🖨️ PRINT FACT STRIP", use_container_width=True)
            except Exception:
                st.error("The robot forgot its history book!")

# --- 7. HOME BUTTON ---
if st.session_state.mode is not None:
    st.write("---")
    if st.button("🏠 START OVER", use_container_width=True):
        st.session_state.mode = None
        st.session_state.selected_char = None
        st.rerun()
