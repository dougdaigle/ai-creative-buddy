import streamlit as st
import os

# --- 1. IPAD STYLING: PERMANENT SKY BLUE ---
st.set_page_config(page_title="My Creative Buddy", layout="centered")

st.markdown("""
    <style>
    /* Full Sky Blue Background */
    .stApp { background-color: #00BFFF; }
    
    /* THE FLOATING BACK BUTTON: Fixed to Top-Left */
    .floating-back {
        position: fixed;
        top: 20px;
        left: 20px;
        background-color: white !important;
        color: black !important;
        text-decoration: none !important;
        padding: 12px 24px;
        font-size: 30px !important;
        font-weight: 900 !important;
        border-radius: 20px;
        border: 5px solid #1a202c;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.3);
        z-index: 9999;
        font-family: 'Arial Black', sans-serif;
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

    /* THE UNIVERSAL KIOSK BUTTON (2-Column Size) */
    .kiosk-link {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        background-color: white !important;
        color: black !important;
        text-decoration: none !important;
        padding: 0 20px;
        font-size: 28px !important; /* Adjusted for 2-column fit */
        font-weight: 900 !important;
        min-height: 110px !important;
        width: 100% !important;
        border-radius: 30px;
        border: 6px solid #1a202c;
        margin-bottom: 20px;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.3);
        font-family: 'Arial Black', sans-serif;
    }

    .btn-icon { font-size: 45px; margin-right: 15px; flex-shrink: 0; }

    /* UI Cleanup */
    header, footer, #MainMenu, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    .instruction-text {
        color: white;
        text-align: center;
        font-size: 45px;
        font-weight: 900;
        margin-bottom: 30px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    /* WORKSHEET PREVIEW FRAME */
    .worksheet-preview {
        background-color: white;
        padding: 25px;
        border-radius: 10px;
        border: 8px solid #1a202c;
        margin-bottom: 30px;
        box-shadow: 0px 15px 30px rgba(0,0,0,0.5);
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .answer-box {
        background-color: #FFF;
        color: black;
        padding: 30px;
        border-radius: 30px;
        font-size: 40px;
        font-weight: 900;
        border: 8px solid #1a202c;
        margin-bottom: 25px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. NAVIGATION LOGIC ---
params = st.query_params
mode = params.get("mode")
animal = params.get("animal")
action = params.get("action")

# --- 3. HARD-RESET BACK BUTTON ---
# This forces the app to reload at the root URL, clearing all parameters
if mode:
    st.markdown('<a href="/" class="floating-back" target="_self">🏠 BACK</a>', unsafe_allow_html=True)

# --- 4. HOME PAGE ---
if not mode:
    st.markdown('<div class="kiosk-title">Current choice:</div>', unsafe_allow_html=True)
    st.markdown('<a href="/?mode=coloring" class="kiosk-link" target="_self" style="font-size:38px !important; min-height:140px !important;"><span class="btn-icon">🎨</span> A. Color Sheet Maker</a>', unsafe_allow_html=True)
    st.markdown('<a href="/?mode=puzzle" class="kiosk-link" target="_self" style="font-size:38px !important; min-height:140px !important;"><span class="btn-icon">🧩</span> B. Today\'s Puzzle</a>', unsafe_allow_html=True)
    st.markdown('<a href="/?mode=fact" class="kiosk-link" target="_self" style="font-size:38px !important; min-height:140px !important;"><span class="btn-icon">💡</span> C. Fun Fact</a>', unsafe_allow_html=True)
    st.markdown('<a href="/?mode=math" class="kiosk-link" target="_self" style="font-size:38px !important; min-height:140px !important;"><span class="btn-icon">➕</span> D. Math Magic</a>', unsafe_allow_html=True)

# --- 5. OPTION A: COLOR SHEET MAKER ---
elif mode == "coloring":
    if not animal:
        st.markdown('<div class="instruction-text">Pick an animal!</div>', unsafe_allow_html=True)
        
        # 14 Animals in 2 Columns
        animals = [
            ("🦖", "Dino"), ("🦁", "Lion"), ("🐘", "Elephant"), ("🦒", "Giraffe"),
            ("🐯", "Tiger"), ("🦓", "Zebra"), ("🐒", "Monkey"), ("🦈", "Shark"),
            ("🐙", "Octopus"), ("🐸", "Frog"), ("🐼", "Panda"), ("🐱", "Cat"),
            ("🐶", "Dog"), ("🐰", "Rabbit")
        ]
        
        col1, col2 = st.columns(2)
        for i, (icon, name) in enumerate(animals):
            target_col = col1 if i % 2 == 0 else col2
            target_col.markdown(f'<a href="/?mode=coloring&animal={name}" class="kiosk-link" target="_self"><span class="btn-icon">{icon}</span> {name}</a>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="instruction-text">{animal} Color Sheet</div>', unsafe_allow_html=True)
        
        dino_file = "Dinosaur adventure in a prehistoric world.jpg"
        
        animal_imgs = {
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
        st.image(animal_imgs.get(animal), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown(f'<a href="/?mode=coloring&animal={animal}&action=print" class="kiosk-link" target="_self" style="font-size:38px !important; min-height:140px !important;"><span class="btn-icon">🖨️</span> PRINT NOW</a>', unsafe_allow_html=True)
        
        if action == "print":
            st.toast("🖨️ Sending to printer...", icon="🤖")
            st.success("Success! Pick it up at the desk.")

# --- 6-8 (PUZZLE, MATH, FACT remain the same) ---
elif mode == "puzzle":
    st.markdown('<div class="instruction-text">🧩 Today\'s Riddle</div>', unsafe_allow_html=True)
    st.markdown('<div class="answer-box">What has hands but cannot clap?</div>', unsafe_allow_html=True)
    if action == "reveal":
        st.markdown('<div class="answer-box" style="background-color:#FFD700;">Answer: A Clock! ⏰</div>', unsafe_allow_html=True)
    else:
        st.markdown('<a href="/?mode=puzzle&action=reveal" class="kiosk-link" target="_self" style="font-size:38px !important; min-height:140px !important;"><span class="btn-icon">🔍</span> SHOW ANSWER</a>', unsafe_allow_html=True)

elif mode == "math":
    st.markdown('<div class="instruction-text">➕ Math Magic!</div>', unsafe_allow_html=True)
    st.markdown('<div class="answer-box" style="font-size:80px !important;">5 + 5 = ?</div>', unsafe_allow_html=True)
    if action == "reveal":
        st.markdown('<div class="answer-box" style="background-color:#FFD700; font-size:80px !important;">10! 🌟</div>', unsafe_allow_html=True)
    else:
        st.markdown('<a href="/?mode=math&action=reveal" class="kiosk-link" target="_self" style="font-size:38px !important; min-height:140px !important;"><span class="btn-icon">🤔</span> CHECK ANSWER</a>', unsafe_allow_html=True)

elif mode == "fact":
    st.markdown('<div class="instruction-text">💡 Fun Fact!</div>', unsafe_allow_html=True)
    st.markdown('<div class="answer-box">Octopuses have three hearts and blue blood! 🐙</div>', unsafe_allow_html=True)
