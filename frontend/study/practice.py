import base64

import requests
import streamlit as st
import json

# Set page configuration
st.set_page_config(layout="wide")

# Load the test data (assuming data is already available)
# with open("data/test_db.json", "r") as f:
#     test_data = json.load(f)

# Custom CSS for better styling
st.markdown("""
    <style>
    .question {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .answer {
        margin-bottom: 10px;
    }
    .navigation-buttons {
        display: flex;
        justify-content: space-between;
        margin-top: 20px;
    }
    .navigation-buttons button {
        width: 100px;
    }
    </style>
""", unsafe_allow_html=True)

# Helper to find test by ID
# def find_test_by_id(test_id):
#     return next((test for test in test_data if test['id'] == test_id), None)

# Function to display question and answers
def display_question(question, question_number, total_questions, answers, current_answer=None):
    st.markdown(f"<div class='question'>Question {question_number}/{total_questions}: {question}</div>", unsafe_allow_html=True)
    
    # Display answers as radio buttons
    selected_answer = st.radio("Choose an answer:", answers, key=question_number, index=answers.index(current_answer) if current_answer else 0)
    return selected_answer

# Function to show the test navigation (Previous, Next, and Submit)
def navigation_buttons(current_question, total_questions):
    col1, col2 = st.columns([1, 1])

    with col1:
        if current_question > 1:
            if st.button("Previous"):
                return "Previous"
    
    with col2:
        if current_question < total_questions:
            if st.button("Next"):
                return "Next"
        else:
            if st.button("Submit"):
                return "Submit"

    return None

# Main test-taking function
def take_test():
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

    st.title(f"Taking the test: {test['name']}")

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
    user_answer = display_question(question_text, current_question, total_questions, answers, current_answer)

    # Store user answer
    user_answers[current_question] = user_answer

    # Navigation buttons (Previous, Next, Submit)
    action = navigation_buttons(current_question, total_questions)

    if action == "Previous" and current_question > 1:
        st.session_state["current_question"] -= 1
        st.rerun()  # Refresh the page to display the previous question

    elif action == "Next" and current_question < total_questions:
        st.session_state["current_question"] += 1
        st.rerun()  # Refresh the page to display the next question

    elif action == "Submit":
        # Once the user submits the test, you can calculate the score, store the result, etc.
        score = calculate_score(user_answers, questions)
        st.success(f"Test submitted! Your score is: {score}%")

        # Optionally, save the user answers and score in the database here
        save_test_result(test_id, user_answers, score)
        st.session_state["current_question"] = 1  # Reset to the first question for next test


# Function to calculate the score (example)
def calculate_score(user_answers, questions):
    correct_answers = 0
    for question_number, user_answer in user_answers.items():
        print(question_number)
        correct_answer = questions[question_number - 1]["answer_1"]  # Assuming answer_1 is the correct answer
        if user_answer == correct_answer:
            correct_answers += 1
    
    return 92

# Function to save test results (for example, saving to a file or database)
def save_test_result(test_id, user_answers, score):
    # Here you could save the result to a database or file.
    # For example, save to a json file or database:
    with open("data/test_results.json", "a") as f:
        result = {
            "test_id": test_id,
            "user_answers": user_answers,
            "score": score
        }
        json.dump(result, f)
        f.write("\n")  # Newline for each result for easier processing

# Start a test with the test_id from the query params
take_test()
