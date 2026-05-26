import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# PAGE CONFIGURATION

st.set_page_config(
    page_title="Student Analytics Dashboard",
    page_icon="🎓",
    layout="wide"
)

# DATABASE CONNECTION

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(BASE_DIR, "database", "students.db")

conn = sqlite3.connect(db_path)

# SQL QUERY

query = """
SELECT 
    students.name,
    students.course,
    students.semester,
    marks.subject,
    marks.marks,
    attendance.attendance_percent

FROM students

JOIN marks
ON students.id = marks.student_id

JOIN attendance
ON students.id = attendance.student_id
"""

df = pd.read_sql_query(query, conn)

# -------------------------------------------------
# DASHBOARD TITLE
# -------------------------------------------------

st.title("🎓 Student Performance Analytics Dashboard")

st.markdown(
    "Analyze academic performance, attendance trends, and subject-wise insights."
)

# SIDEBAR FILTERS

st.sidebar.header("📌 Dashboard Filters")

subject_options = ["All"] + list(df["subject"].unique())

selected_subject = st.sidebar.selectbox(
    "Select Subject",
    subject_options
)

# Filter dataset
if selected_subject != "All":
    filtered_df = df[df["subject"] == selected_subject]
else:
    filtered_df = df

# KPI SECTION

average_marks = round(filtered_df["marks"].mean(), 2)
highest_marks = filtered_df["marks"].max()
lowest_marks = filtered_df["marks"].min()

col1, col2, col3 = st.columns(3)

col1.metric("📊 Average Marks", average_marks)
col2.metric("🏆 Highest Marks", highest_marks)
col3.metric("📉 Lowest Marks", lowest_marks)

# DATA TABLE

st.subheader("📋 Student Dataset")

st.dataframe(filtered_df, use_container_width=True)

# STUDENT PERFORMANCE CHART

st.subheader("📈 Student Performance Analysis")

student_avg = filtered_df.groupby("name")["marks"].mean()

fig, ax = plt.subplots(figsize=(10, 5))

bars = ax.bar(
    student_avg.index,
    student_avg.values
)

ax.set_title("Average Student Performance")
ax.set_xlabel("Students")
ax.set_ylabel("Average Marks")

# Add labels on bars
for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + 1,
        f"{height:.1f}",
        ha="center"
    )

st.pyplot(fig)

# SUBJECT-WISE ANALYSIS


st.subheader("📚 Subject-wise Average")

subject_avg = filtered_df.groupby("subject")["marks"].mean()

fig2, ax2 = plt.subplots(figsize=(8, 5))

subject_avg.plot(
    kind="bar",
    ax=ax2
)

ax2.set_ylabel("Average Marks")

st.pyplot(fig2)


# ATTENDANCE ANALYSIS

st.subheader("📅 Attendance Analysis")

attendance_df = filtered_df.drop_duplicates(subset=["name"])

fig3, ax3 = plt.subplots(figsize=(10, 5))

ax3.plot(
    attendance_df["name"],
    attendance_df["attendance_percent"],
    marker="o",
    linewidth=3
)

ax3.set_ylabel("Attendance Percentage")

st.pyplot(fig3)

# TOP PERFORMERS


st.subheader("🏅 Top Performers")

top_students = filtered_df.sort_values(
    by="marks",
    ascending=False
).head(5)

st.dataframe(top_students, use_container_width=True)


st.markdown("---")

st.markdown(
    "Built using Python, Pandas, SQLite, Matplotlib, and Streamlit."
)


conn.close()