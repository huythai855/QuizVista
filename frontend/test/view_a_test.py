import json

import streamlit as st
from sympy import false
# this_page = "create_new_test"

st.set_page_config(layout="wide")

with open("data/test_db.json", "r") as f:
    tests_data = json.load(f)

with open("data/user_db.json", "r") as f:
    users_data = json.load(f)

# Get the test ID from the URL parameters
test_id = st.query_params["test_id"]

def find_by_id(data_list, item_id):
    return next((item for item in data_list if item["id"] == item_id), {"name": "Unknown"})

# Find the selected test from the tests_data
selected_test = None
for test in tests_data:
    if test["id"] == int(test_id):
        selected_test = test
        break

if selected_test:
    st.title(f"{selected_test['name']}")
    st.write(f"{selected_test['description']}")
    
    questions = selected_test["question_list"]
    creator = find_by_id(users_data, selected_test["created_by_id"])
    # print(questions)

    col1, col2, col3, col4 = st.columns([0.3, 0.3, 0.2, 0.2])
    with col1:
        st.markdown(f"**Number of questions:** {len(questions)}")
        st.markdown(f"**Test creator:** {creator['fullname']}")
    with col2:
        st.markdown(f"**Time limit:** {selected_test['time_limit']}")
        st.markdown(f"**Average score:** {selected_test['average_score']}%")
    with col3:
        flashcard = st.button("Learn with flashcard")
        study_note = st.button("Learn with study notes")
    with col4:
        export = st.button("Export test")
    take_quiz_link = f'<a href="/practice?test_id={selected_test["id"]}" target="_self"><button style="background-color:#4CAF50;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer;">Take the Quiz Now</button></a>'
    st.markdown(take_quiz_link, unsafe_allow_html=True)


    st.text("")
    st.text("")

    counter = 0
    for key, value in questions.items():
        box = st.container(border=True)
        counter += 1
        box.markdown(f"### {value['question']}")
        for i in range(1, 5):
            in_col1, in_col2 = box.columns([0.9, 0.05])
            in_col1.text_input(f"Answer {i}", value[f"answer_{i}"], key=f"{counter}{i}")
            in_col2.text("")
            in_col2.text("")
            checkboxA = in_col2.checkbox(f"{counter}{i}", key=f"{counter}{i}A", label_visibility="hidden")

else:
    st.error("Test not found. Please check the test ID in the URL.")
