import json
import streamlit as st
import pandas as pd
st.set_page_config(layout="wide")

with open("data/test_db.json", "r") as f:
    tests_data = json.load(f)

with open("data/user_db.json", "r") as f:
    users_data = json.load(f)

st.title("All Tests")
test_columns = 4  # Number of columns in the grid

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
        margin-right: 40px;
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

def find_by_id(data_list, item_id):
    return next((item for item in data_list if item["id"] == item_id), {"name": "Unknown"})

# Display tests in a grid format
for i in range(0, len(tests_data), test_columns):
    row_tests = tests_data[i: i + test_columns]
    cols = st.columns(test_columns)
    
    for col, test in zip(cols, row_tests):
        creator = find_by_id(users_data, test["created_by_id"])
        with col:
            st.markdown(f"""
                <div class="card">
                    <div class="creation-date">{test['creation_date']}</div>
                    <a href="view_a_test?test_id={test['id']}" target="_self">{test['name']}</a>
                    <p>Creator: {creator['fullname']}</p>
                    <p>Time Limit: {test['time_limit']}</p>
                    <p>Average Score: {test['average_score']}%</p>
                </div>
            """, unsafe_allow_html=True)