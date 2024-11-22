import os

import requests
import streamlit as st
from flask import request
from mpmath.libmp import BACKEND

st.set_page_config(layout="wide")

st.markdown("# Register")
st.write('Welcome to QuizVista, an AI-powered education platform!')
st.write("")

col1, col2, col3 = st.columns([0.7, 0.2, 0.7])

with col1:
    st.text("")
    fullname = st.text_input("Full Name")
    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    gender = st.radio("Gender", ["male", "female", "other"])
    birthdate = st.date_input("Birthdate")

    if st.button("Register"):
        if username == "admin" and password == "admin":
            st.success("Login Successful")

        BACKEND_URL = "http://localhost:1510"

        response = requests.post(
            BACKEND_URL + "/api/credentials/register",
            json={
                "username": username,
                "password": password,
                "role": "student",
                "registered_at": "2021-09-01",
                "fullname": fullname,
                "gender": gender,
                "dob": str(birthdate),
            }
        )

        if response.status_code == 200:
            st.success("Registration Successful")
            st.switch_page("/Users/nguyenhuythai/Documents/GitHub/QuizVista/frontend/test/create_new_test.py")
        else:
            print(response.json())
            st.error("Invalid Username or Password")

    # st.text("Not registered yet? Sign up now")
    st.markdown("[Have an account yet? Sign in now](https://www.google.com/)")
with col2:
    pass

with col3:
    st.image("images/intro.png")
