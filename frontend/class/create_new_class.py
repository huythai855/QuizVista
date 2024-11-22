import json

import requests
import streamlit as st
from sympy import false
this_page = "create_new_class"

# with open("data/class_db.json", "r") as f:
#     classes_data = json.load(f)
# class1 = classes_data[0]

st.set_page_config(layout="wide")

st.markdown("# Create a new class")
st.write("")

col1, col2, col3 = st.columns([0.3, 0.05, 0.6])
state = st.session_state

if 'submit' not in st.session_state:
    st.session_state.submit = False

with col1:
    class_name = st.text_input("Class name")
    class_description = st.text_area("Class description")
    submit = st.button("Submit", key=f"{this_page}")
    if submit:
        response = requests.post("http://127.0.0.1:1510/api/classes/",
                                 json={"name": class_name, "description": class_description, "created_by_id": 1, "created_at": "2022-01-01"})
        print(response.json())
        st.session_state.submit = True

with col3:
    if state.submit :
        success_message = (f"""
        <div style="background-color:#e6f4ea; padding:10px; border-radius:5px; font-size:16px; color:#2e7d32;">
            <span>Class created successfully!</span> 
            <a href="view_a_class?class_id={response.json()['id']}" target="_self" style="color:#2e7d32; text-decoration:none; font-weight:bold;" 
            onmouseover="this.style.color='#1b5e20'" onmouseout="this.style.color='#2e7d32'">Click here</a> to view your class.
        </div>
        """)

        st.markdown(success_message, unsafe_allow_html=True)
            
    else:
        box = st.container(border=True)
        box.markdown(
            """
            ### Create a new class
            1. Fill in class details
            2. Click on the `Submit` button
            3. Start making tests for your very own class
            """
        )