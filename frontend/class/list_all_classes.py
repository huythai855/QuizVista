import json
import streamlit as st
import pandas as pd
st.set_page_config(layout="wide")

with open("data/class_db.json", "r") as f:
    classes_data = json.load(f)

with open("data/user_db.json", "r") as f:
    user_data = json.load(f)

st.title("Your classes")
class_columns = 3  # Number of columns in the grid

# Define styles for the card
st.markdown("""
    <style>
    /* Card grid container */
    .card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); /* Adjusted for better spacing */
        gap: 20px;
        margin-top: 20px;
    }

    /* Individual card styling */
    .card {
        background-color: #f9f9f9;
        padding: 20px;
        margin-bottom: 20px;
        border-radius: 8px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow for hover effect */
        text-align: center;
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        position: relative;
    }
    .card:hover {
        transform: scale(1.02);
        box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.15); /* Enhanced hover effect */
    }

    /* Card content - Name, link, description */
    .card a {
        font-weight: bold;
        font-size: 24px; /* Larger test/class name */
        color: #0072C6;
        text-decoration: none;
        margin-top: 10px;
    }
    .card a:hover {
        color: #005a9e;
        text-decoration: underline;
    }

    /* Creation date styling */
    .card .creation-date {
        position: absolute;
        top: 10px;
        left: 10px;
        background-color: #ffffff;
        padding: 5px 10px;
        font-size: 12px;
        color: #888888;
        border-radius: 5px;
    }

    /* Paragraphs inside cards */
    .card p {
        margin: 8px 0;
        color: #333;
    }

    /* Consistent styling for layout on all pages */
    .card-container {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        justify-content: space-between;
    }

    </style>
    """, unsafe_allow_html=True)

def get_creator_name(creator_id, user_db):
    for user in user_db:
        if user["id"] == creator_id:
            return user["fullname"]
    return "Unknown"

for i in range(0, len(classes_data), class_columns):
    row_classes = classes_data[i: i + class_columns]
    cols = st.columns(class_columns)
    
    for col, classs in zip(cols, row_classes):
        with col:
            creator_name = get_creator_name(classs['created_by_id'], user_data)
            st.markdown(f"""
                <div class="card">
                    <div class="creation-date">{classs['creation_date']}</div>
                    <a href="view_a_class?class_id={classs['id']}" target="_self">{classs['name']}</a>
                    <p>Teacher: {creator_name}</p>
                </div>
            """, unsafe_allow_html=True)