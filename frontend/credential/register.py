import streamlit as st
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
        else:
            st.error("Invalid Username or Password")

    # st.text("Not registered yet? Sign up now")
    st.markdown("[Have an account yet? Sign in now](https://www.google.com/)")
with col2:
    pass

with col3:
    st.image("images/intro.png")
