import streamlit as st
import os
try:
    from google import genai
    from google.genai import types
except ImportError:
    st.error("Please run: pip install google-genai")

# --- Kiosk Configuration ---
st.set_page_config(page_title="My Creative Buddy", layout="centered")

# Initialize Gemini Client (Uses GEMINI_API_KEY environment variable)
# If you don't have one set, you can use: client = genai.Client(api_key="YOUR_KEY")
client = genai.Client()

st.title("🤖 My Creative Buddy!")
st.subheader("Choose an activity:")

# --- Main Menu ---
col1, col2, col3 = st.columns(3)

if 'mode' not in st.session_state:
    st.session_state.mode = None

with col1:
    if st.button("🎨 Coloring Page", use_container_width=True):
        st.session_state.mode = "coloring"
with col2:
    if st.button("📸 Caricature", use_container_width=True):
        st.session_state.mode = "caricature"
with col3:
    if st.button("💡 Fun Fact", use_container_width=True):
        st.session_state.mode = "fact"

# --- Content Areas ---
if st.session_state.mode == "coloring":
    st.divider()
    prompt = st.text_input("What should we color today?", placeholder="A dragon playing soccer...")
    if st.button("Create Page"):
        with st.spinner("Drawing your masterpiece..."):
            # 2026 Image Generation Logic
            response = client.models.generate_content(
                model='gemini-3-flash-image',
                contents=f"A simple black and white line art coloring page of {prompt}. No shading, thick lines.",
                config=types.GenerateContentConfig(response_modalities=["IMAGE"])
            )
            st.image(response.generated_images[0], use_container_width=True)
            st.button("🖨️ PRINT NOW", type="primary")

elif st.session_state.mode == "fact":
    st.divider()
    # Simple logic for 'On This Day'
    st.write("### 📅 On This Day: March 7th")
    st.info("In 1876, Alexander Graham Bell was granted a patent for the telephone!")
    st.button("🖨️ PRINT FACT STRIP")

if st.button("🏠 Start Over"):
    st.session_state.mode = None
    st.rerun()