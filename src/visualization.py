import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------
# DATABASE CONNECTION
# ------------------------------------------

conn = sqlite3.connect("database/students.db")

query = """
SELECT
    students.name,
    marks.subject,
    marks.marks,
    attendance.attendance_percent

FROM students

JOIN marks
ON students.id = marks.student_id

JOIN attendance
ON students.id = attendance.student_id
"""

# Load SQL data into DataFrame

df = pd.read_sql_query(query, conn)

# Improve overall chart appearance
plt.style.use('ggplot')

# ------------------------------------------
# 1. STUDENT MARKS BAR CHART
# ------------------------------------------

plt.figure(figsize=(10, 6))

plt.bar(
    df["name"],
    df["marks"],
    edgecolor='black'
)

plt.title(
    "Student Performance Analysis",
    fontsize=18,
    fontweight='bold'
)

plt.xlabel(
    "Students",
    fontsize=13
)

plt.ylabel(
    "Marks",
    fontsize=13
)

plt.xticks(rotation=10)

# Add values on bars
for index, value in enumerate(df["marks"]):
    plt.text(index, value + 1, str(value), ha='center', fontsize=10)

plt.tight_layout()
plt.show()

# ------------------------------------------
# 2. SUBJECT-WISE AVERAGE ANALYSIS
# ------------------------------------------

subject_avg = df.groupby("subject")["marks"].mean()

plt.figure(figsize=(8, 6))

subject_avg.plot(
    kind='bar',
    edgecolor='black'
)

plt.title(
    "Subject-wise Average Marks",
    fontsize=18,
    fontweight='bold'
)

plt.xlabel(
    "Subjects",
    fontsize=13
)

plt.ylabel(
    "Average Marks",
    fontsize=13
)

plt.xticks(rotation=0)

plt.tight_layout()
plt.show()

# ------------------------------------------
# 3. ATTENDANCE TREND ANALYSIS
# ------------------------------------------

attendance_data = df.drop_duplicates(subset=["name"])

plt.figure(figsize=(10, 6))

plt.plot(
    attendance_data["name"],
    attendance_data["attendance_percent"],
    marker='o',
    linewidth=3,
    markersize=10
)

plt.title(
    "Student Attendance Analysis",
    fontsize=18,
    fontweight='bold'
)

plt.xlabel(
    "Students",
    fontsize=13
)

plt.ylabel(
    "Attendance Percentage",
    fontsize=13
)

# Add attendance labels
for index, value in enumerate(attendance_data["attendance_percent"]):
    plt.text(index, value + 0.5, f'{value}%', ha='center')

plt.tight_layout()
plt.show()

# ------------------------------------------
# 4. PIE CHART - SUBJECT DISTRIBUTION
# ------------------------------------------

subject_counts = df["subject"].value_counts()

plt.figure(figsize=(8, 8))

plt.pie(
    subject_counts,
    labels=subject_counts.index,
    autopct='%1.1f%%',
    startangle=140
)

plt.title(
    "Subject Distribution",
    fontsize=18,
    fontweight='bold'
)

plt.tight_layout()
plt.show()

# ------------------------------------------
# 5. TOPPER ANALYSIS
# ------------------------------------------

sorted_df = df.sort_values(by="marks", ascending=False)

plt.figure(figsize=(10, 6))

plt.bar(
    sorted_df["name"],
    sorted_df["marks"],
    edgecolor='black'
)

plt.title(
    "Top Performers Ranking",
    fontsize=18,
    fontweight='bold'
)

plt.xlabel(
    "Students",
    fontsize=13
)

plt.ylabel(
    "Marks",
    fontsize=13
)

plt.xticks(rotation=10)

plt.tight_layout()
plt.show()

# ------------------------------------------
# CLOSE DATABASE CONNECTION
# ------------------------------------------

conn.close()

print("Professional visualizations generated successfully!")
