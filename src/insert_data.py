import sqlite3

conn = sqlite3.connect("database/students.db")

cursor = conn.cursor()

# Insert into students table
students = [
    (1, "Rahul Sharma", "BCA", 6),
    (2, "Aman Verma", "BCA", 6),
    (3, "Sneha Kapoor", "BCA", 6),
    (4, "Priya Singh", "BCA", 6)
]

cursor.executemany("""
INSERT INTO students(id, name, course, semester)
VALUES (?, ?, ?, ?)
""", students)

# Insert into marks table
marks = [
    (1, "Python", 85),
    (2, "Python", 76),
    (3, "Python", 92),
    (4, "Python", 67),

    (1, "DBMS", 80),
    (2, "DBMS", 72),
    (3, "DBMS", 95),
    (4, "DBMS", 60)
]

cursor.executemany("""
INSERT INTO marks(student_id, subject, marks)
VALUES (?, ?, ?)
""", marks)

# Insert attendance
attendance = [
    (1, 91.5),
    (2, 85.0),
    (3, 96.0),
    (4, 70.0)
]

cursor.executemany("""
INSERT INTO attendance(student_id, attendance_percent)
VALUES (?, ?)
""", attendance)

conn.commit()
conn.close()

print("Sample student data inserted successfully!")