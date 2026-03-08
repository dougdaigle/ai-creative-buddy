import streamlit as st
from google import genai
from google.genai import types

# --- 1. PREMIUM KIOSK STYLING (UPDATED FOR DARK FONT) ---
# We're moving from a simple style to a more rugged, "touchscreen-ready" kiosk feel.
st.set_page_config(page_title="My Creative Buddy AI", layout="centered")

# Custom CSS for that professional, kiosk-app feel
st.markdown("""
    <style>
    /* --- Main App Styling --- */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* --- Centering and Styling Titles/Subtitles --- */
    /* Target the main titles and subtitles to center them and use dark font */
    h1, h2, h3, .stMarkdown p {
        text-align: center;
        color: #1a202c; /* A very dark, almost black, readable gray */
        font-family: 'Inter', sans-serif; /* A clear, clean kiosk font */
    }

    /* Target specifically the main title on the landing page */
    .css-k1v44b h1 {
        margin-bottom: 0.5rem;
    }

    /* --- Styling Input and Puzzles for the Kiosk --- */
    /* Centering the instruction text */
    div[data-testid="stMarkdownContainer"] {
        text-align: center;
        color: #1a202c;
    }

    /* Styling the Input Box */
    .stTextInput input {
        border-radius: 20px;
        border: 2px solid #1a202c;
        text-align: center;
        color: #1a202c;
    }

    /* Styling the Quiz/Puzzle Area with dark, clear font */
    div.stAlert {
        background-color: #f7fafc;
        border: 2px solid #1a202c;
        border-radius: 15px;
        color: #1a202c; /* Making sure instructions are dark */
    }
    div.stAlert p {
        color: #1a202c;
    }

    /* Styling the puzzle answer input for a kiosk feel */
    .stNumberInput input {
        border-radius: 15px;
        border: 2px solid #1a202c;
        text-align: center;
        font-size: 24px;
        color: #1a202c;
    }

    /* --- Making Buttons Massive & Fun --- */
    /* We'll use Streamlit's primary buttons to make them really stand out on a kiosk screen */
    div.stButton > button:first-child {
        background-color: #f7fafc; /* Standard button color */
        color: #1a202c; /* Make sure the standard button text is dark */
        height: 6em;
        width: 100%;
        border-radius: 25px;
        font-size: 20px;
        font-weight: bold;
        border: 2px solid #1a202c;
        box-shadow: 0px 5px 10px rgba(0,0,0,0.1);
        display: flex; /* Helps center vertically */
        align-items: center; /* Center vertically */
        justify-content: center; /* Center horizontally */
        text-align: center;
    }
    
    /* Style for our massive "START" primary buttons */
    div.stButton > button.css-1f912p4 {
        background-color: #1a202c; /* Kiosk Primary button color (Dark) */
        color: white; /* Text color for dark button */
        height: 10em;
        width: 100%;
        border-radius: 30px;
        font-size: 32px;
        border: none;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.2);
    }

    /* --- Custom Header Section (Updated for Dark Font) --- */
    .custom-header {
        text-align: center;
        padding: 20px;
        background-color: #ffffff; /* Make the header area pop against the background */
        border-radius: 20px;
        border: 3px solid #1a202c;
        margin-bottom: 2rem;
    }
    .custom-header h1 {
        color: #1a202c;
        margin-bottom: 5px;
    }
    .custom-header p {
        color: #1a202c;
        font-style: italic;
    }

    /* --- Styling Success/Warning boxes (Updated for Dark Font) --- */
    div.stSuccess {
        background-color: #e6fffa;
        color: #1a202c;
        border: 2px solid #285e61;
        border-radius: 15px;
    }
    div.stSuccess p {
        color: #1a202c;
    }
    div.stWarning {
        background-color: #fffaf0;
        color: #1a202c;
        border: 2px solid #744210;
        border-radius: 15px;
    }
    div.stWarning p {
        color: #1a202c;
    }

    /* Hide the top technical menu for an immersive kiosk feel */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. AI CLIENT SETUP ---
# Securely accessing your secret API key
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("🔑 Please add GEMINI_API_KEY to your Streamlit Secrets before deploying.")
    st.stop()

# --- 3. APP HEADER ---
# This is a custom HTML section for the title to make it look nicer on a kiosk
st.markdown("""
    <div class="custom-header">
        <h1>🤖 My Creative Buddy</h1>
        <p>The AI Library Station</p>
    </div>
    """, unsafe_allow_html=True)

# --- 4. APP NAVIGATION LOGIC ---
if 'mode' not in st.session_state:
    st.session_state.mode = None

# --- THE MAIN MENU ---
if st.session_state.mode is None:
    st.markdown("## Choose your creative adventure!")
    st.write("Click a massive button to get started.")

    # We use empty columns to center the buttons on the screen
    _, mid_col, _ = st.columns([1, 4, 1])

    with mid_col:
        col1, col2, col3 = st.columns(3)
        with col1:
            # Adding a "Start coloring!" specific function
            if st.button("🎨\nColoring\nPage"):
                st.session_state.mode = "coloring"
        with col2:
            # Adding a "Let's draw!" specific function
            if st.button("📸\nFace\nCaricature"):
                st.session_state.mode = "caricature"
        with col3:
            # Adding a "What's the puzzle?" specific function
            if st.button("💡\nDaily\nFact"):
                st.session_state.mode = "fact"

# --- ACTIVITY: COLORING PAGE ---
if st.session_state.mode == "coloring":
    st.divider()
    # Adding a clean, centered kiosk input field
    prompt = st.text_input("What should the AI draw?", placeholder="e.g. A cat on the moon...")
    
    if st.button("CREATE MASTERPIECE", key="gen_color"):
        with st.spinner("🎨 Your robot buddy is drawing..."):
            try:
                # March 2026 Model Name & Image Configuration
                response = client.models.generate_content(
                    model='gemini-3.1-flash-image-preview',
                    contents=f"Kids coloring book page, black and white line art of {prompt}. Thick outlines, no shading, white background.",
                    config=types.GenerateContentConfig(response_modalities=["IMAGE"])
                )
                
                # Use the new 2026 as_image() method to convert the AI output directly for Streamlit
                for part in response.parts:
                    if part.inline_data:
                        st.image(part.as_image(), use_container_width=True, caption=f"Coloring sheet: {prompt}")
                        st.success(" Ready to print!")
                        # This button would connect to your kiosk printer script
                        st.button("🖨️ SEND TO PRINTER")
            
            except Exception as e:
                st.error("The robot is resting. Try a different idea!")
                st.write(f"Technical Log: {str(e)}")

# --- ACTIVITY: FUN FACT ---
elif st.session_state.mode == "fact":
    st.divider()
    # Simple logic for 'On This Day'
    st.write("### 📅 On This Day: March 8th")
    st.info("**International Women's Day:** Celebrated worldwide to honor women's achievements.")
    st.write("---")
    st.write("### Weird Animal Facts")
    st.success("**The Snail:** Did you know a snail can sleep for three years?")
    st.button("🖨️ PRINT FACT STRIP")

# --- HOME BUTTON ---
# This button needs to be clear to reset the kiosk for the next user.
if st.session_state.mode is not None:
    st.write("---")
    if st.button("🏠 BACK TO MENU"):
        st.session_state.mode = None
        st.rerun()
