import sqlite3
import pandas as pd

# Connect database
conn = sqlite3.connect("database/students.db")

# SQL Query with JOIN
query = """
SELECT 
    students.id,
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

# Load data into pandas dataframe
df = pd.read_sql_query(query, conn)

# Display complete dataframe
print("\nSTUDENT PERFORMANCE DATA")
print(df)

# Average marks
average_marks = df["marks"].mean()

print("\nAVERAGE MARKS")
print(round(average_marks, 2))

# Highest scorer
topper = df[df["marks"] == df["marks"].max()]

print("\nTOP PERFORMER")
print(topper)

# Subject-wise average
subject_average = df.groupby("subject")["marks"].mean()

print("\nSUBJECT-WISE AVERAGE")
print(subject_average)

# Students with low attendance
low_attendance = df[df["attendance_percent"] < 75]

print("\nLOW ATTENDANCE STUDENTS")
print(low_attendance[["name", "attendance_percent"]].drop_duplicates())

conn.close()