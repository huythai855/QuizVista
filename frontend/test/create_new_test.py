import json

import streamlit as st
from sympy import false
this_page = "create_new_test"

st.set_page_config(layout="wide")

st.markdown("# Create a new test")
st.write('Select input source and upload the file to create a new test')
st.write("")


data = '''
{
    "question1": {
        "question": "Who is the current president of the United States?",
        "answer_1": "Donald Trump",
        "answer_2": "Kamala Harris",
        "answer_3": "Joe Biden",
        "answer_4": "Barack Obama",
        "link_image": "data/0.png"
    },
    "question2": {
        "question": "Who is the current prime minister of Vietnam?",
        "answer_1": "Pham Minh Chinh",
        "answer_2": "To Lam",
        "answer_3": "Nguyen Thi Kim Ngan",
        "answer_4": "Le Kha Phieu",
        "link_image": "data/0.png"
    }
}
'''

questions = json.loads(data)
col1, col2, col3 = st.columns([0.3, 0.05, 0.6])
state = st.session_state

if 'submit' not in st.session_state:
    st.session_state.submit = False

with col1:
    test_name = st.text_input("Test name")
    test_description = st.text_area("Test description")
    input_source = st.selectbox("Select input source", ["Upload", "Text", "URL", "Subject"])
    if input_source == "Upload":
        uploaded_file = st.file_uploader("Choose a file")
    elif input_source == "Text":
        text = st.text_area("Enter text")
    elif input_source == "URL":
        url = st.text_input("Enter URL")
    elif input_source == "Subject":
        subject = st.text_input("Enter subject")
    col4, col5 = col1.columns([1, 2])
    with col4:
        num_questions = st.number_input("Number of questions", min_value=1, value=1)
    with col5:
        question_type = st.selectbox("Question type", ["Multiple choice", "True/False", "Short answer", "Matching", "Fill in the blank"])
    submit = st.button("Submit", key=f"{this_page}")
    if submit:
        st.session_state.submit = True


with col3:
    if state.submit :
        counter = 0
        for key, value in questions.items():
            box = st.container(border=True)
            counter += 1
            box.markdown(f"### {value['question']}")
            # image
            box.image(value['link_image'])
            for i in range(1, 5):
                in_col1, in_col2 = box.columns([0.9, 0.05])
                in_col1.text_input(f"Answer {i}", value[f"answer_{i}"])
                in_col2.text("")
                in_col2.text("")
                checkboxA = in_col2.checkbox(f"{counter}{i}", key=f"{counter}{i}A", label_visibility="hidden")
    else:
        box = st.container(border=True)
        box.markdown(
            """
            ### Create new question set
            1. Select input source and upload content
            2. Click on the `Submit` button to create a new question set
            3. View your quiz set, study notes & flash cards
            """
        )