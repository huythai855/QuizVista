import streamlit as st

pages = {
    "": [
        st.Page("home.py", title="Home", icon="🏠"),
    ],
    "Test management": [
        st.Page("test/create_new_test.py", title="Create a new test", icon="📝"),
        st.Page("test/list_all_tests.py", title="List all tests", icon="📋"),
        st.Page("test/view_a_test.py", title="View a test detail", icon="🔍"),
    ],
    "Class management": [
        st.Page("class/create_new_class.py", title="Create a new class", icon="📝"),
        st.Page("class/list_all_classes.py", title="List all classes", icon="📋"),
        st.Page("class/view_a_class.py", title="View a class detail", icon="🔍"),
    ],
    "Study": [
        st.Page("study/practice.py", title="Practice with a test", icon="📝"),
        st.Page("study/study_note.py", title="View a study note", icon="📖"),
        st.Page("study/flashcard.py", title="View a flashcard", icon="🃏"),
        st.Page("study/chat.py", title="Chat with AI Mentor", icon="💬"),
    ],
    "Your account": [
        st.Page("credential/login.py", title="Login", icon="🔑"),
        st.Page("credential/register.py", title="Register", icon="📝"),
    ],
}

pg = st.navigation(pages)
pg.run()