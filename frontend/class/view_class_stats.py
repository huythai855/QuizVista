import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Generate larger sample data
data = []
np.random.seed(42)  # For reproducibility

# Simulate data for 10 students, each taking 3 tests
student_names = [f"Student {i}" for i in range(1, 21)]
test_names = [f"Test {i}" for i in range(1, 11)]
class_name = "Class A"

# Simulate data for 20 students, each taking 10 tests
for student_id, student_name in enumerate(student_names, start=1):
    for test_id, test_name in enumerate(test_names, start=1):
        score = np.random.randint(60, 100)  # Random scores between 60 and 100
        date = f"2021-01-{np.random.randint(1, 28):02d}"  # Random date in January 2021
        data.append({
            "id": len(data) + 1,
            "taker": student_id,
            "taker_name": student_name,
            "test": test_id,
            "test_name": test_name,
            "class": class_name,
            "score": score,
            "date": date
        })

# Convert to DataFrame
df = pd.DataFrame(data)

table_df = df.pivot(index="taker_name", columns="test_name", values="score")
table_df = table_df.reset_index().rename(columns={"taker_name": "Name"})

# Set page configuration for full-width layout
st.set_page_config(layout="wide")

# Page Title
st.title("Class Statistics")

# Display Table in full width
st.subheader("Grades Table")
st.dataframe(table_df, use_container_width=True)

# Calculate summary statistics for charts
average_scores = df.groupby("test")["score"].mean()
all_scores = df["score"]

# Histogram: Distribution of Scores
st.subheader("Score Distribution ")
fig_hist = px.histogram(df, x="score", nbins=12, title="", labels={"score": "Score"})
st.plotly_chart(fig_hist)

# Line Chart: Average Score Trend across Tests
st.subheader("Average Class Score per Test")
fig_line = px.line(x=average_scores.index, y=average_scores.values, title="", labels={"x": "Test", "y": "Average Score"})
st.plotly_chart(fig_line)
