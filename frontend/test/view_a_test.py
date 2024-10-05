import json

import streamlit as st
from sympy import false
this_page = "create_new_test"

st.set_page_config(layout="wide")

st.markdown("## Bài kiểm tra số 1")
st.write("")


data = '''
{
    "question1": {
        "question": "Who is the current president of the United States?",
        "answer_1": "Donald Trump",
        "answer_2": "Kamala Harris",
        "answer_3": "Joe Biden",
        "answer_4": "Barack Obama",
        "link_image": "image_save/0.png"
    },
    "question2": {
        "question": "Who is the current prime minister of Vietnam?",
        "answer_1": "Pham Minh Chinh",
        "answer_2": "To Lam",
        "answer_3": "Nguyen Thi Kim Ngan",
        "answer_4": "Le Kha Phieu",
        "link_image": "image_save/0.png"
    }
}
'''

questions = json.loads(data)
col1, col2, col3 = st.columns([0.3, 0.3, 0.3])
with col1:
    st.markdown("**Number of questions:** 6")
    st.markdown("**Test creator:** Mrs. Jane Doe")
with col2:
    st.markdown("**Time limit:** 60 minutes")
    st.markdown("**Average score:** 8.5/10")
with col3:
    flashcard = st.button("Learn with flashcard")
    study_note = st.button("Learn with study notes")
take_quiz = st.button("Take the quiz now")

st.text("")
st.text("")


counter = 0
for key, value in questions.items():
    box = st.container(border=True)
    counter += 1
    box.markdown(f"### {value['question']}")
    for i in range(1, 5):
        in_col1, in_col2 = box.columns([0.9, 0.05])
        in_col1.text_input(f"Answer {i}", value[f"answer_{i}"])
        in_col2.text("")
        in_col2.text("")
        checkboxA = in_col2.checkbox(f"{counter}{i}", key=f"{counter}{i}A", label_visibility="hidden")
