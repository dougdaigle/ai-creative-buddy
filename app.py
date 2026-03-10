import streamlit as st
import os

# --- 1. IPAD STYLING: EXACT REPLICA OF YOUR PREFERRED STYLE ---
st.set_page_config(page_title="My Creative Buddy", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #00BFFF; }
    
    /* THE FLOATING BACK BUTTON */
    .floating-back-container {
        position: fixed;
        top: 20px;
        left: 20px;
        z-index: 10000;
    }
    
    /* Make the Streamlit Button look like your HTML Back Button */
    .floating-back-container div.stButton > button {
        background-color: white !important;
        color: black !important;
        padding: 10px 20px !important;
        font-size: 25px !important;
        font-weight: 900 !important;
        border-radius: 20px !important;
        border: 5px solid #1a202c !important;
        width: auto !important;
        height: auto !important;
    }

    .kiosk-title {
        color: white;
        text-align: center;
        font-size: 50px !important;
        font-weight: 900;
        margin-top: 20px;
        margin-bottom: 35px;
        font-family: 'Arial Black', sans-serif;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
    }

    /* THE UNIVERSAL KIOSK BUTTON: Replicating your 'kiosk-link' style */
    div.stButton > button {
        background-color: white !important;
        color: black !important;
        border-radius: 40px !important;
        border: 8px solid #1a202c !important;
        font-size: 35px !important;
        font-weight: 900 !important;
        min-height: 120px !important;
        width: 100% !important;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.4) !important;
        font-family: 'Arial Black', sans-serif !important;
        display: flex !important;
        justify-content: flex-start !important;
        padding-left: 30px !important;
        margin-bottom: 15px !important;
    }

    header, footer, #MainMenu, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    .instruction-text {
        color: white;
        text-align: center;
        font-size: 45px;
        font-weight: 900;
        margin-bottom: 30px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .worksheet-preview {
        background-color: white;
        padding: 25px;
        border-radius: 10px;
        border: 8px solid #1a202c;
        margin-bottom: 30px;
        box-shadow: 0px 15px 30px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE (The Bulletproof Brain) ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'animal' not in st.session_state: st.session_state.animal = None
if 'reveal' not in st.session_state: st.session_state.reveal = False

# --- 3. FLOATING BACK BUTTON (Logic Fix) ---
if st.session_state.page != "home":
    st.markdown('<div class="floating-back-container">', unsafe_allow_html=True)
    if st.button("🏠 BACK", key="main_back"):
        st.session_state.page = "home"
        st.session_state.animal = None
        st.session_state.reveal = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. NAVIGATION ---

# --- HOME PAGE ---
if st.session_state.page == "home":
    st.markdown('<div class="kiosk-title">Current choice:</div>', unsafe_allow_html=True)
    if st.button("🎨 A. Color Sheet Maker"):
        st.session_state.page = "coloring"; st.rerun()
    if st.button("🧩 B. Today's Puzzle"):
        st.session_state.page = "puzzle"; st.rerun()
    if st.button("💡 C. Fun Fact"):
        st.session_state.page = "fact"; st.rerun()
    if st.button("➕ D. Math Magic"):
        st.session_state.page = "math"; st.rerun()

# --- COLOR SHEET MAKER ---
elif st.session_state.page == "coloring":
    if st.session_state.animal is None:
        st.markdown('<div class="instruction-text">Pick an animal!</div>', unsafe_allow_html=True)
        
        animals = [
            ("🦖 Dino", "Dino"), ("🦁 Lion", "Lion"), ("🐘 Elephant", "Elephant"), 
            ("🦒 Giraffe", "Giraffe"), ("🐯 Tiger", "Tiger"), ("🦓 Zebra", "Zebra"), 
            ("🐒 Monkey", "Monkey"), ("🦈 Shark", "Shark"), ("🐙 Octopus", "Octopus"), 
            ("🐸 Frog", "Frog"), ("🐼 Panda", "Panda"), ("🐱 Cat", "Cat"), 
            ("🐶 Dog", "Dog"), ("🐰 Rabbit", "Rabbit")
        ]
        
        col1, col2 = st.columns(2)
        for i, (label, name) in enumerate(animals):
            target_col = col1 if i % 2 == 0 else col2
            if target_col.button(label):
                st.session_state.animal = name
                st.rerun()
    else:
        st.markdown(f'<div class="instruction-text">{st.session_state.animal} Color Sheet</div>', unsafe_allow_html=True)
        
        dino_file = "Dinosaur adventure in a prehistoric world.jpg"
        img_urls = {
            "Dino": dino_file if os.path.exists(dino_file) else "https://img.icons8.com/ios/500/dinosaur.png",
            "Lion": "https://img.icons8.com/ios/500/lion.png",
            "Elephant": "https://img.icons8.com/ios/500/elephant.png",
            "Giraffe": "https://img.icons8.com/ios/500/giraffe.png",
            "Tiger": "https://img.icons8.com/ios/500/tiger-side-view.png",
            "Zebra": "https://img.icons8.com/ios/500/zebra.png",
            "Monkey": "https://img.icons8.com/ios/500/monkey.png",
            "Shark": "https://img.icons8.com/ios/500/shark.png",
            "Octopus": "https://img.icons8.com/ios/500/octopus.png",
            "Frog": "https://img.icons8.com/ios/500/frog.png",
            "Panda": "https://img.icons8.com/ios/500/panda.png",
            "Cat": "https://img.icons8.com/ios/500/cat.png",
            "Dog": "https://img.icons8.com/ios/500/dog.png",
            "Rabbit": "https://img.icons8.com/ios/500/rabbit.png"
        }
        
        st.markdown('<div class="worksheet-preview">', unsafe_allow_html=True)
        st.image(img_urls.get(st.session_state.animal), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🖨️ PRINT NOW"):
            st.success("Success! Pick it up at the desk.")

# --- PUZZLE PAGE ---
elif st.session_state.page == "puzzle":
    st.markdown('<div class="instruction-text">🧩 Today\'s Riddle</div>', unsafe_allow_html=True)
    st.info("What has hands but cannot clap? \n\n Answer: A Clock! ⏰" if st.session_state.reveal else "What has hands but cannot clap?")
    if not st.session_state.reveal:
        if st.button("🔍 SHOW ANSWER"):
            st.session_state.reveal = True
            st.rerun()
