import streamlit as st
import datetime
import random
import os

# --- 1. IPAD STYLING: Sky Blue Background & Forced Visible Text ---
st.set_page_config(page_title="My Creative Buddy", layout="centered")

st.markdown("""
    <style>
    /* Vibrant Sky Blue Background */
    .stApp { 
        background-color: #00BFFF; 
    }
    
    .menu-title {
        color: white;
        text-align: center;
        font-size: 60px !important; /* Massive Title */
        font-weight: 900;
        margin-top: 20px;
        margin-bottom: 40px;
        text-shadow: 4px 4px 8px rgba(0,0,0,0.4);
        font-family: 'Arial Black', sans-serif;
    }

    /* WHITE BUTTONS WITH FORCED BLACK TEXT */
    div.stButton > button {
        background-color: white !important;
        color: #000000 !important; /* FORCED SOLID BLACK */
        border-radius: 40px !important;
        border: 8px solid #1a202c !important; /* Extra thick border for visibility */
        font-size: 70px !important; /* GIANT FONT */
        font-weight: 900 !important;
        height: 200px !important; /* Taller boxes */
        width: 100% !important;
        box-shadow: 0px 12px 24px rgba(0,0,0,0.5);
        margin-bottom: 45px;
        font-family: 'Arial Black', sans-serif;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* Ensure text stays black even when hovering or clicking on iPad */
    div.stButton > button:hover, div.stButton > button:active, div.stButton > button:focus {
        color: #000000 !important;
        background-color: #f0f0f0 !important;
    }
    
    /* Clean Kiosk UI: Hide standard Streamlit elements */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* Global label styling */
    h2, h3, p, label { 
        color: white !important; 
        text-align: center; 
        font-weight: 900; 
        font-size: 40px !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if 'mode' not in st.session_state: st.session_state.mode = None
if 'selected_char' not in st.session_state: st.session_state.selected_char = None
if 'math_problem' not in st.session_state: st.session_state.math_problem = None

# --- 3. MAIN MENU ---
if st.session_state.mode is None:
    st.markdown('<div class="menu-title">Choose an activity:</div>', unsafe_allow_html=True)
    
    # Matching the exact lettered style with GIANT visible text
    if st.button("A. Coloring Sheet", use_container_width=True): 
        st.session_state.mode = "coloring"; st.rerun()
        
    if st.button("B. Today's Puzzle", use_container_width=True): 
        st.session_state.mode = "puzzle"; st.rerun()
        
    if st.button("C. Fun Fact", use_container_width=True): 
        st.session_state.mode = "fact"; st.rerun()
        
    if st.button("D. Math Magic", use_container_width=True): 
        st.session_state.mode = "math"; st.rerun()

# --- 4. ACTIVITY: COLORING PAGE ---
elif st.session_state.mode == "coloring":
    st.write("## Pick a Friend!")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Dino", use_container_width=True): 
            st.session_state.selected_char = "dinosaur"; st.rerun()
    with c2:
        if st.button("Astro", use_container_width=True): 
            st.session_state.selected_char = "astronaut"; st.rerun()
    with c3:
        if st.button("Magic", use_container_width=True): 
            st.session_state.selected_char = "unicorn"; st.rerun()

# --- 5. PUZZLE / MATH / FACT (STATIC FOR DEMO) ---
elif st.session_state.mode == "puzzle":
    st.info("### What has hands but cannot clap? \n\n**Answer:** A Clock! ⏰")

elif st.session_state.mode == "math":
    st.write("## 5 + 3 = ?")
    st.success("### Answer: 8! 🌟")

elif st.session_state.mode == "fact":
    st.success("### Did you know? Octopuses have three hearts! 🐙")

# --- 6. HOME BUTTON ---
if st.session_state.mode:
    st.write("---")
    if st.button("🏠 BACK", use_container_width=True):
        st.session_state.mode = None
        st.session_state.selected_char = None
        st.rerun()
