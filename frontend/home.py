import time
import streamlit as st

# Centering all elements using Streamlit's container and custom CSS
st.markdown(
    """
    <style>
    .centered-text {
        text-align: center;
    }
    .button-container {
        display: flex;
        justify-content: center;
        gap: 10px;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Heading
st.markdown("<h1 class='centered-text'>Welcome to QuizVista</h1>", unsafe_allow_html=True)

st.markdown("<h2 class='centered-text'>The ultimate platform for learning and testing your knowledge</h2>", unsafe_allow_html=True)


# Paragraph
st.markdown("<p class='centered-text'>Start your journey with QuizVista to test and improve your knowledge.</p>", unsafe_allow_html=True)

# Buttons
col1, col2, col3, col4 = st.columns([2, 3, 3, 1])
with col2:
    if st.button("Get Started"):
        st.write("Redirecting to Get Started...")

with col3:
    if st.button("Learn More"):
        st.write("Redirecting to Learn More...")

st.image("data/0.png", use_column_width=True)

# Sliding phrases
# phrases = ["Challenge yourself daily!", "Track your progress.", "Unlock new knowledge.", "Compete with friends!", "QuizVista makes learning fun!"]
# placeholder = st.empty()

# for i in range(5):  # Loop through phrases multiple times
#     for phrase in phrases:
#         placeholder.markdown(f"<h3 class='centered-text'>{phrase}</h3>", unsafe_allow_html=True)
#         time.sleep(2)  # Adjust timing for slide transition


# CSS for card styling
st.markdown(
    """
    <style>
    .card {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .grid-container {
        display: grid;
        grid-template-columns: 1fr 1fr;  /* 2 columns */
        gap: 20px;
        padding: 20px;
    }

    .footer {
            margin-top: 3em;
            color: #cfcfcf;
            font-size: 0.9em;
        }
        .footer a {
            color: #00d4ff;
            text-decoration: none;
        }
        .footer a:hover {
            text-decoration: underline;
        }
    </style>
    """, 
    unsafe_allow_html=True
)

# Container for grid layout
st.markdown("<div class='grid-container'>", unsafe_allow_html=True)

# List of features to display
features = [
    {"title": "Feature 1", "description": "Description of feature 1."},
    {"title": "Feature 2", "description": "Description of feature 2."},
    {"title": "Feature 3", "description": "Description of feature 3."},
    {"title": "Feature 4", "description": "Description of feature 4."},
    {"title": "Feature 5", "description": "Description of feature 5."},
    {"title": "Feature 6", "description": "Description of feature 6."},
]

# Create each feature card
for feature in features:
    st.markdown(
        f"""
        <div class="card">
            <h3>{feature['title']}</h3>
            <p>{feature['description']}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Close the grid container
st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="footer">
        <p>Connect with us on <a href="https://www.linkedin.com/company/quizvista">LinkedIn</a> | Contact: <a href="mailto:support@quizvista.com">support@quizvista.com</a></p>
        <p>© 2024 QuizVista. All rights reserved.</p>
    </div>
    """,
    unsafe_allow_html=True
)