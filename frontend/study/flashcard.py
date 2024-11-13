import json

import streamlit as st
import streamlit.components.v1 as components
from streamlit import button

from sympy import false
this_page = "create_new_test"

st.set_page_config(layout="wide")

st.markdown("# Flashcard demo")
st.write("Read the definition, guess, then click on the card to see the term.")
st.write("")

def flashcard_component(front_text, back_text):
    flashcard_html = f"""
    <style>
        .flashcard {{
            background-color: #f0f0f0;
            width: 600px;
            height: 400px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transition: transform 0.6s;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: Arial, sans-serif;
            font-size: 24px;
            color: #333;
            text-align: center;
            cursor: pointer;
            position: relative;
            transform-style: preserve-3d;
            perspective: 1000px;
            margin: 0 auto;
        }}

        .flashcard.flipped {{
            transform: rotateY(180deg);
        }}

        .flashcard-content {{
            position: absolute;
            backface-visibility: hidden;
        }}

        .flashcard-front {{
            z-index: 2;
        }}

        .flashcard-back {{
            transform: rotateY(180deg);
            z-index: 1;
        }}
    </style>

    <div class="flashcard" onclick="this.classList.toggle('flipped')">
        <div class="flashcard-content flashcard-front">
            {front_text}
        </div>
        <div class="flashcard-content flashcard-back">
            {back_text}
        </div>
    </div>
    """
    # Chèn HTML và CSS vào Streamlit
    components.html(flashcard_html, height=440)


flashcard_component("Hello", "Xin chào")

col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
with col1:
    button_prev = st.button("Previous")
with col3:
    button_next = st.button("Next")

