import base64
import json

import requests
import streamlit as st
import streamlit.components.v1 as components
from streamlit import button

from sympy import false
this_page = "create_new_test"

st.set_page_config(layout="wide")

st.markdown("# Flashcard")
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


def navigation_buttons(current_question, total_questions):
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
    with col1:
        if current_question > 1:
            if st.button("Previous"):
                return "Previous"
    with col3:
        if current_question < total_questions:
            if st.button("Next"):
                return "Next"
        # else:
        #     if st.button("Submit"):
        #         return "Submit"

    return None

def flash():
    test_id = int(st.query_params["test_id"]) if "test_id" in st.query_params else 1

    response = requests.get(f"http://localhost:1510/api/tests/detail?test_id={test_id}")
    test = response.json()

    encoded_question_set = test["question_set"]
    decoded_question_set = base64.b64decode(encoded_question_set).decode("utf-8")
    question_set = json.loads(decoded_question_set)["questions"]

    # test = find_test_by_id(test_id)

    if not test:
        st.error("Test not found!")
        return
    # Get questions and answers
    questions = question_set
    total_questions = len(questions)

    # Dictionary to store answers
    user_answers = {}

    # Session state to track current question index
    if "current_question" not in st.session_state:
        st.session_state["current_question"] = 1

    current_question = st.session_state["current_question"]

    # Get current question and answers
    current_q = questions[int(current_question) - 1]

    question_text = current_q["question"]
    answers = [
        current_q["answer_1"],
        current_q["answer_2"],
        current_q["answer_3"],
        current_q["answer_4"]
    ]
    current_answer = user_answers.get(current_question, None)

    # Display question and answers
    flashcard_component(question_text, answers[0])

    # Store user answer

    # Navigation buttons (Previous, Next, Submit)
    action = navigation_buttons(current_question, total_questions)

    if action == "Previous" and current_question > 1:
        st.session_state["current_question"] -= 1
        st.rerun()  # Refresh the page to display the previous question

    elif action == "Next" and current_question < total_questions:
        st.session_state["current_question"] += 1
        st.rerun()  # Refresh the page to display the next question


# flashcard_component("Hello", "Xin chào")
flash()

# col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
# with col1:
#     button_prev = st.button("Previous", key="prev")
# with col3:
#     button_next = st.button("Next", key="next")

