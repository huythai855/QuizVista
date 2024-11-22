import base64
import json

import requests
import streamlit as st
from sympy import false
age = "create_new_test"# this_p

st.set_page_config(layout="wide")

test_id = st.query_params["test_id"]
response = requests.get(f"http://127.0.0.1:1510/api/tests/detail?test_id={test_id}")

print(response.json())

test_data2 = response.json()

encoded_question_set = response.json()["question_set"]

# Giải mã từ base64 sang chuỗi JSON
decoded_question_set = base64.b64decode(encoded_question_set).decode("utf-8")

# Parse chuỗi JSON thành Python dictionary
question_set = json.loads(decoded_question_set)

print(question_set)





with open("data/test_db.json", "r") as f:
    tests_data = json.load(f)

with open("data/user_db.json", "r") as f:
    users_data = json.load(f)

# Get the test ID from the URL parameters

def find_by_id(data_list, item_id):
    return next((item for item in data_list if item["id"] == item_id), {"name": "Unknown"})

# Find the selected test from the tests_data
selected_test = None
for test in tests_data:
    if test["id"] == int(test_id):
        selected_test = test
        break

print (test_data2)

if selected_test:
    st.title(f"{test_data2['name']}")
    st.write(f"{test_data2['description']}")
    
    # questions = selected_test["question_list"]
    questions = question_set["questions"]
    print("Questions: ", questions)

    # creator = find_by_id(users_data, selected_test["created_by_id"])
    creator = {
        "fullname": "Nguyễn Thị Hương",
    }
    # print(questions)

    col1, col2, col3, col4 = st.columns([0.3, 0.3, 0.2, 0.2])
    with col1:
        st.markdown(f"**Number of questions:** {len(questions)}")
        st.markdown(f"**Test creator:** {creator['fullname']}")
    with col2:
        st.markdown(f"**Time limit:** 15 minutes")
        st.markdown(f"**Average score:** 92%")
    with col3:
        # flashcard = st.button("Learn with flashcard")
        flashcard = f'<a href="/flashcard?test_id={selected_test["id"]}" target="_self"><button style="background-color:#4CAF50;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer;">Learn with flashcard</button></a>'
        st.markdown(flashcard, unsafe_allow_html=True)
        # study_note = st.button("Learn with study notes")
        # if study_note:
        #     st.switch_page("/Users/nguyenhuythai/Documents/GitHub/QuizVista/frontend/study/study_note.py")
        study_note = f'<a href="/study_note?test_id={selected_test["id"]}" target="_self"><button style="background-color:#4CAF50;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer;">Learn with study note</button></a>'
        st.markdown(study_note, unsafe_allow_html=True)
    with col4:
        export = st.button("Export test")
    take_quiz_link = f'<a href="/practice?test_id={selected_test["id"]}" target="_self"><button style="background-color:#4CAF50;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer;">Take the Quiz Now</button></a>'
    st.markdown(take_quiz_link, unsafe_allow_html=True)


    st.text("")
    st.text("")

    counter = 0
    for question in questions:
        box = st.container(border=True)
        counter += 1
        box.markdown(f"### {question['question']}")
        # question['link_image'] = "data/0.png"
        temp = question['link_image']
        print("Tempppp" , temp)
        if temp != "":
            box.image(temp, width=600)
        # if question['link_image'] is not None:
        #     box.image(question['link_image'], width=600)
        for i in range(1, 5):
            in_col1, in_col2 = box.columns([0.9, 0.05])
            in_col1.text_input(f"Answer {i}", question[f"answer_{i}"], key=f"{counter}{i}")
            in_col2.text("")
            in_col2.text("")
            # "link_image": "data/0.png"
            checkboxA = in_col2.checkbox(f"{counter}{i}", key=f"{counter}{i}A", label_visibility="hidden")

else:
    st.error("Test not found. Please check the test ID in the URL.")
