import streamlit as st

pages = {
    "Test management": [
        st.Page("test/create_new_test.py", title="Create a new test"),
        st.Page("test/view_a_test.py", title="View a test detail"),
        st.Page("test/list_all_tests.py", title="List all tests"),
    ],
    "Class management": [
        st.Page("class/create_new_class.py", title="Create a new class"),
        st.Page("class/view_a_class.py", title="View a class detail"),
        st.Page("class/list_all_classes.py", title="List all class"),
    ],
    "Study": [
        st.Page("study/practice.py", title="Practice with a test"),
        st.Page("study/study_note.py", title="View a study note"),
        st.Page("study/flashcard.py", title="View a flashcard"),
    ],
    "Your account": [
            st.Page("credential/login.py", title="Login"),
            st.Page("credential/register.py", title="Register"),
    ],
}

pg = st.navigation(pages)
pg.run()