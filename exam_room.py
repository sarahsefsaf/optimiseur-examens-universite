import psycopg2
from faker import Faker
import random

fake = Faker()

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="exam_optimization",
    user="postgres",
    password="hana1234",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Fetch all students, exams, rooms
cursor.execute("SELECT id FROM etudiants")
students = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT id FROM examens")
exams = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT id FROM salles")
rooms = [row[0] for row in cursor.fetchall()]

# Clear existing data
cursor.execute("DELETE FROM exam_room_students")
conn.commit()
print("✅ Cleared existing exam_room_student data")

# Fill table
for student_id in students:
    # Assign 1-3 exams per student
    student_exams = random.sample(exams, k=random.randint(1, 3))
    for exam_id in student_exams:
        # Randomly pick a room
        salle_id = random.choice(rooms)
        
        # Insert assignment
        cursor.execute(
            "INSERT INTO exam_room_students (exam_id, salle_id, etudiant_id) VALUES (%s, %s, %s)",
            (exam_id, salle_id, student_id)
        )

# Optional: Overfill some rooms to generate capacity conflicts
# Optional: Overfill some rooms without creating duplicate exam-student assignments
for exam_id in exams:
    overfill_room = random.choice(rooms)
    added_students = 0
    while added_students < 5:  # try to add 5 extra students
        student_id = random.choice(students)
        # Check if student already has this exam
        cursor.execute(
            "SELECT 1 FROM exam_room_students WHERE exam_id=%s AND etudiant_id=%s",
            (exam_id, student_id)
        )
        if cursor.fetchone() is None:
            cursor.execute(
                "INSERT INTO exam_room_students (exam_id, salle_id, etudiant_id) VALUES (%s, %s, %s)",
                (exam_id, overfill_room, student_id)
            )
            added_students += 1

conn.commit()
print("✅ exam_room_students table filled with fake data (some rooms overfilled)")

cursor.close()
conn.close()
