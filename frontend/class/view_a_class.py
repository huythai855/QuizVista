import streamlit as st
import json
import requests

# from frontend.test.list_all_tests import tests_data

# from frontend.test.view_a_test import selected_test

st.set_page_config(layout="wide")

# Load data
# with open("data/class_db.json", "r") as f:
#     class_data = json.load(f)
# with open("data/user_db.json", "r") as f:
#     user_data = json.load(f)
# with open("data/test_db.json", "r") as f:
#     test_data = json.load(f)


class_id = st.query_params["class_id"]

response = requests.get("http://localhost:1510/api/tests/")
test_data = response.json()["tests"]

response = requests.get(f"http://localhost:1510/api/classes/members?class_id={class_id}")
member_data = response.json()["members"]

response = requests.get(f"http://localhost:1510/api/classes/")
class_data = response.json()["classes"]
selected_class = None
for class_ in class_data:
    if class_["id"] == int(class_id):
        selected_class = class_
        break


# Helper to find entries by ID
def find_by_id(data_list, item_id):
    return next((item for item in data_list if item["id"] == item_id), {"name": "Unknown"})

# Component for a styled table header
def table_header(columns):
    st.markdown(
        f"""
        <style>
            .table-header {{
                display: flex;
                justify-content: space-between;
                background-color: #f3f4f6;
                padding: 10px 15px;
                border-bottom: 2px solid #e5e7eb;
                font-weight: bold;
                color: #374151;
            }}
            .table-row {{
                display: flex;
                justify-content: space-between;
                padding: 8px 15px;
                border-bottom: 1px solid #e5e7eb;
                color: #374151;
            }}
            .table-row:hover {{
                background-color: #f9fafb;
            }}
        </style>
        <div class="table-header">
            {''.join([f"<div style='flex:{flex};'>{col}</div>" for col, flex in columns])}
        </div>
        """,
        unsafe_allow_html=True,
    )

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


# selected_class = find_by_id(class_data, int(class_id)) if class_id else None

if selected_class:
    st.title(selected_class["name"])
    st.write(selected_class["description"])
    creator = {"fullname": "Nguyen Thi Huong"}

    st.markdown(f"**Creator:** {creator['fullname']}")

    with st.expander("Add a new member"):
        username = st.text_input("Enter username or email to add member")

        if st.button("Add Member"):
            st.success(f"Member '{username}' added successfully.")
            member_data = member_data + [{"fullname": "Nguyen Van A", "role": "Student"}]

    view_mode = st.radio("View Mode:", ("📋 Tests in Class", "👥 Members"), index=0, horizontal=True)

    if view_mode == "📋 Tests in Class":
        st.subheader("Tests in this Class")
        # Tests grid layout
        test_columns = 4
        st.markdown('<div class="card-grid">', unsafe_allow_html=True)
        for i in range(0, len(test_data), test_columns):
            row_tests = test_data[i: i + test_columns]
            print(row_tests)
            cols = st.columns(test_columns)
            for col, test in zip(cols, row_tests):
                # test = find_by_id(test_data, test_id)
                with col:
                    st.markdown(f"""
                        <div class="card">
                            <div class="creation-date">"12/11/2024"</div>
                            <a href="view_a_test?test_id={test['id']}" target="_self">{test['name']}</a>
                            <p>Total Questions: 10</p>
                            <p>Time Limit: 15 minutes</p>
                            <p>Average Score: 92%</p>
                        </div>
                    """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif view_mode == "👥 Members":
        st.subheader("Members in this Class")
        # Display table header
        table_header([ 
            ("Full Name", 2),
            ("Role", 2),
            # ("Email", 2),
            ("Tests", 3),  # Add a column for tests
        ])
        
        # Member rows

        count = 0
        for member in member_data:
            count = count + 1
            # member = find_by_id(user_data, member_id)

            # Get list of tests the user is enrolled in
            user_tests = test_data
            test_names = [test["name"] for test in user_tests]

            # Create a delete button for each member
            st.text("")
            # delete_button = st.button(f"Delete {member['fullname']}", key=f"delete_{count}")

            # if delete_button:
            #     # Remove the member from the class and update the data (in this example, it just removes from the class view)
            #     # selected_class["members"].remove(member_id)
            #     # In a real app, you'd update the class data here.
            #     st.success(f"Member '{member['fullname']}' has been deleted.")

            st.markdown(f"""
                <div class="table-row">
                    <div style="flex: 2;">{member['fullname']}</div>
                    <div style="flex: 2;">{member['role']}</div>
                    <div style="flex: 3;">{", ".join(test_names) if test_names else 'No tests assigned'}</div>
                </div>
                """, unsafe_allow_html=True)
else:
    st.error("Class not found.")
