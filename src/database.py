import sqlite3

conn = sqlite3.connect("database/students.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    course TEXT,
    semester INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS marks(
    student_id INTEGER,
    subject TEXT,
    marks INTEGER,
    FOREIGN KEY(student_id) REFERENCES students(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance(
    student_id INTEGER,
    attendance_percent REAL,
    FOREIGN KEY(student_id) REFERENCES students(id)
)
""")

conn.commit()
conn.close()

print("Database setup completed successfully!")