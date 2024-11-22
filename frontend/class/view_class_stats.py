import requests
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide")
# Generate larger sample data
data = []
np.random.seed(42)  # For reproducibility

class_id = 1
response = requests.get(f"http://localhost:1510/api/classes/members?class_id={class_id}")
member_data = response.json()["members"]

response2 = requests.get("http://localhost:1510/api/tests/")
test_data = response2.json()["tests"]

response3 = requests.get(f"http://localhost:1510/api/classes/")
class_data = response3.json()["classes"]
selected_class = None
for class_ in class_data:
    if class_["id"] == int(class_id):
        selected_class = class_
        break


# Simulate data for 10 students, each taking 3 tests
student_names = [member["fullname"] for member in member_data]
test_names = [test["name"] for test in test_data]
class_name = selected_class["name"]

# Simulate data for 20 students, each taking 10 tests
tmp = {}
for student in student_names:
    for test in test_names:
        # there is a record of that student in that test, continue
        if (student, test) in tmp:
            continue
        data.append({
            "taker_name": student,
            "test_name": test,
            "score": np.random.randint(60, 100)
        })
        tmp[(student, test)] = True
print(data)

# Convert to DataFrame
df = pd.DataFrame(data)

table_df = df.pivot(index="taker_name", columns="test_name", values="score")
table_df = table_df.reset_index().rename(columns={"taker_name": "Name"})

# Set page configuration for full-width layout

# Page Title
st.title("Class Statistics")

# Display Table in full width
st.subheader("Grades Table")
st.dataframe(table_df, use_container_width=True)

# Calculate summary statistics for charts
average_scores = df.groupby("test_name")["score"].mean()
all_scores = df["score"]

# Histogram: Distribution of Scores
st.subheader("Score Distribution ")
fig_hist = px.histogram(df, x="score", nbins=12, title="", labels={"score": "Score"})
st.plotly_chart(fig_hist)

# Line Chart: Average Score Trend across Tests
st.subheader("Average Class Score per Test")
fig_line = px.line(x=average_scores.index, y=average_scores.values, title="", labels={"x": "Test", "y": "Average Score"})
st.plotly_chart(fig_line)