import streamlit as st
import os

# --- 1. IPAD STYLING: EXACT ORIGINAL PILL LOOK ---
st.set_page_config(page_title="My Creative Buddy", layout="centered")

st.markdown("""
    <style>
    /* Sky Blue Background */
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
        font-size: 65px !important;
        font-weight: 900;
        margin-top: 20px;
        margin-bottom: 40px;
        font-family: 'Arial Black', sans-serif;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
    }

    /* THE UNIVERSAL KIOSK BUTTON: Pill Style */
    .kiosk-link {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        background-color: white !important;
        color: black !important;
        text-decoration: none !important;
        padding: 0 40px;
        font-size: 42px !important;
        font-weight: 900 !important;
        min-height: 140px !important;
        width: 100% !important;
        border-radius: 80px;
        border: 10px solid #1a202c;
        margin-bottom: 30px;
        box-shadow: 0px 12px 0px #1a202c;
        font-family: 'Arial Black', sans-serif;
    }

    .btn-icon {
        font-size: 65px; 
        margin-right: 30px;
        flex-shrink: 0;
    }

    /* UI Cleanup */
    header, footer, #MainMenu, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    .instruction-text {
        color: white;
        text-align: center;
        font-size: 50px;
        font-weight: 900;
        margin-bottom: 30px;
        font-family: 'Arial Black', sans-serif;
    }

    /* THE WORKSHEET FRAME */
    .worksheet-preview {
        background-color: white;
        padding: 20px;
        border-radius: 20px;
        border: 10px solid #1a202c;
        margin-bottom: 30px;
        box-shadow: 0px 15px 30px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. NAVIGATION LOGIC ---
params = st.query_params
mode = params.get("mode")
animal = params.get("animal")
action = params.get("action")

# --- 3. THE BULLETPROOF BACK BUTTON ---
if mode:
    st.markdown("""
        <a href="/" onclick="window.location.href='/'; return false;" class="floating-back" target="_self">🏠 BACK</a>
    """, unsafe_allow_html=True)

# --- 4. HOME PAGE ---
if not mode:
    st.markdown('<div class="kiosk-title">Current choice:</div>', unsafe_allow_html=True)
    st.markdown('<a href="/?mode=coloring" class="kiosk-link" target="_self"><span class="btn-icon">🎨</span> A. Color Sheet Maker</a>', unsafe_allow_html=True)
    st.markdown('<a href="/?mode=puzzle" class="kiosk-link" target="_self"><span class="btn-icon">🧩</span> B. Today\'s Puzzle</a>', unsafe_allow_html=True)
    st.markdown('<a href="/?mode=fact" class="kiosk-link" target="_self"><span class="btn-icon">💡</span> C. Fun Fact</a>', unsafe_allow_html=True)
    st.markdown('<a href="/?mode=math" class="kiosk-link" target="_self"><span class="btn-icon">➕</span> D. Math Magic</a>', unsafe_allow_html=True)

# --- 5. OPTION A: COLOR SHEET MAKER ---
elif mode == "coloring":
    if not animal:
        st.markdown('<div class="instruction-text">Pick an animal!</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        animals = [
            ("🦖", "Dino"), ("🦁", "Lion"), ("🐘", "Elephant"), ("🦒", "Giraffe"),
            ("🐯", "Tiger"), ("🦓", "Zebra"), ("🐒", "Monkey"), ("🦈", "Shark"),
            ("🐙", "Octopus"), ("🐸", "Frog"), ("🐼", "Panda"), ("🐱", "Cat"),
            ("🐶", "Dog"), ("🐰", "Rabbit")
        ]
        
        for i, (icon, name) in enumerate(animals):
            target = col1 if i % 2 == 0 else col2
            target.markdown(f'<a href="/?mode=coloring&animal={name}" class="kiosk-link" target="_self" style="min-height:110px !important; font-size:30px !important; border-radius:50px;"><span class="btn-icon" style="font-size:45px;">{icon}</span> {name}</a>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="instruction-text">{animal} Color Sheet</div>', unsafe_allow_html=True)
        
        # MAPPING: Local file paths
        dino_file = "Dinosaur adventure in a prehistoric world.jpg"
        cat_file = "cat.png"
        elephant_file = "elephant.png"
        giraffe_file = "giraffe.png"

        animal_imgs = {
            "Dino": dino_file if os.path.exists(dino_file) else "https://img.icons8.com/ios/500/dinosaur.png",
            "Cat": cat_file if os.path.exists(cat_file) else "https://img.icons8.com/ios/500/cat.png",
            "Elephant": elephant_file if os.path.exists(elephant_file) else "https://img.icons8.com/ios/500/elephant.png",
            "Giraffe": giraffe_file if os.path.exists(giraffe_file) else "https://img.icons8.com/ios/500/giraffe.png",
            "Lion": "https://img.icons8.com/ios/500/lion.png",
            "Tiger": "https://img.icons8.com/ios/500/tiger-side-view.png",
            "Zebra": "https://img.icons8.com/ios/500/zebra.png",
            "Monkey": "https://img.icons8.com/ios/500/monkey.png",
            "Shark": "https://img.icons8.com/ios/500/shark.png",
            "Octopus": "https://img.icons8.com/ios/500/octopus.png",
            "Frog": "https://img.icons8.com/ios/500/frog.png",
            "Panda": "https://img.icons8.com/ios/500/panda.png",
            "Dog": "https://img.icons8.com/ios/500/dog.png",
            "Rabbit": "https://img.icons8.com/ios/500/rabbit.png"
        }
        
        st.markdown('<div class="worksheet-preview">', unsafe_allow_html=True)
        st.image(animal_imgs.get(animal), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown(f'<a href="/?mode=coloring&animal={animal}&action=print" class="kiosk-link" target="_self" style="justify-content:center;"><span class="btn-icon">🖨️</span> PRINT NOW</a>', unsafe_allow_html=True)
        
        if action == "print":
            st.toast("🖨️ Sending to printer...", icon="🤖")
