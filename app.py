import streamlit as st
from google import genai
from google.genai import types
import datetime

# --- 1. IPAD & TOUCH OPTIMIZATION (CSS) ---
st.set_page_config(page_title="My Creative Buddy", layout="centered")

st.markdown("""
    <style>
    /* Full-screen feel for iPad */
    .stApp { 
        background-color: #F0F5FF; 
        padding-top: 0rem;
    }
    
    /* Make titles very clear and centered */
    h1, h2, h3 { 
        color: #1E3A8A; 
        text-align: center; 
        font-family: 'Arial', sans-serif;
    }

    /* iPad Touch Optimization: Massive Buttons */
    div.stButton > button {
        border-radius: 20px;
        border: 3px solid #1E3A8A;
        background-color: white;
        color: #1a202c;
        font-weight: bold;
        font-size: 22px !important;
        height: 100px !important; /* Fixed height for touch consistency */
        margin-bottom: 10px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
    }

    /* Image labels for the coloring page */
    .stMarkdown p {
        text-align: center;
        font-weight: bold;
        color: #1E3A8A;
        font-size: 18px;
    }

    /* Hide the top bar and "Made with Streamlit" for a clean kiosk look */
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
    st.write("### Choose an activity:")
    # On iPad, stacked buttons or a clean grid work best
    if st.button("🎨 Coloring Page", use_container_width=True): 
        st.session_state.mode = "coloring"
    if st.button("📸 Face Caricature", use_container_width=True): 
        st.session_state.mode = "caricature"
    if st.button("💡 Fun Fact", use_container_width=True): 
        st.session_state.mode = "fact"

# --- 5. ACTIVITY: COLORING PAGE ---
elif st.session_state.mode == "coloring":
    st.write("## 1. Pick a Friend!")
    # Using 3 columns for the pictures to fit iPad width perfectly
    char_col1, char_col2, char_col3 = st.columns(3)
    
    with char_col1:
        st.image("https://img.icons8.com/color/200/dinosaur.png", use_container_width=True)
        if st.button("Dinosaur", use_container_width=True): 
            st.session_state.selected_char = "a friendly dinosaur"
    with char_col2:
        st.image("https://img.icons8.com/color/200/astronaut-helmet.png", use_container_width=True)
        if st.button("Astronaut", use_container_width=True): 
            st.session_state.selected_char = "a brave astronaut"
    with char_col3:
        st.image("https://img.icons8.com/color/200/unicorn.png", use_container_width=True)
        if st.button("Unicorn", use_container_width=True): 
            st.session_state.selected_char = "a magic unicorn"

    if st.session_state.selected_char:
        st.markdown(f"### Ready to draw your **{st.session_state.selected_char}**?")
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
                    st.error("Robot is busy! Make sure billing is enabled in AI Studio.")

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
            except Exception as e:
                st.error("The robot forgot its history book!")

# --- 7. HOME BUTTON (Standardized for iPad) ---
if st.session_state.mode is not None:
    st.write("---")
    if st.button("🏠 START OVER", use_container_width=True):
        st.session_state.mode = None
        st.session_state.selected_char = None
        st.rerun()
