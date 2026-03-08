import streamlit as st
from google import genai # 2026 SDK

# --- Kiosk Configuration ---
st.set_page_config(page_title="My Creative Buddy", layout="centered")

# Friendly 2026 Header
st.title("🤖 My Creative Buddy!")
st.subheader("What do you want to make today?")

# --- Main Menu ---
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🎨 Coloring Page"):
        st.session_state.mode = "coloring"

with col2:
    if st.button("📸 Caricature"):
        st.session_state.mode = "caricature"

with col3:
    if st.button("💡 Fun Fact"):
        st.session_state.mode = "fact"

# --- Interaction Logic ---
if 'mode' in st.session_state:
    if st.session_state.mode == "coloring":
        prompt = st.text_input("Tell me what to draw! (Ex: A cat on the moon)")
        if st.button("Generate Page"):
            with st.spinner("🎨 Your robot buddy is drawing..."):
                # In your real app, call Gemini API here
                st.image("https://via.placeholder.com/500x500.png?text=Coloring+Page+Coming+Soon", 
                         caption="Your custom coloring sheet!")
                st.button("🖨️ PRINT MY PAGE")

    elif st.session_state.mode == "fact":
        st.write("### 🌟 Fun Fact of the Day:")
        st.info("Did you know that octopuses have three hearts and blue blood?")
        st.button("🖨️ PRINT FACT STRIP")
