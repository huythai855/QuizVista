import requests
import streamlit as st
st.set_page_config(layout="wide")

st.markdown("# Login")
st.write('Welcome to QuizVista, an AI-powered education platform!')
st.write("")


col1, col2, col3 = st.columns([0.7, 0.2, 0.7])

with col1:
    st.text("")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        response = requests.post(
            "http://localhost:1510/api/credentials/login",
            json={
                "username": username,
                "password": password,
            }
        )

        print(response.json())

        if response.status_code == 200:
            user_id = response.json()["user_id"]
            print(user_id)

        if username == "admin" and password == "admin":
            st.success("Login Successful")
        else:
            st.error("Invalid Username or Password")

    st.markdown("[Not registered yet? Sign up now](https://www.google.com/)")
with col2:
    pass

with col3:
    st.image("images/intro.png")
