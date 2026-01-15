import psycopg2
import random

conn = psycopg2.connect(
    dbname="exam_optimization",
    user="postgres",
    password="hana1234",
    host="localhost"
)
cursor = conn.cursor()

# Fetch all exams and rooms
cursor.execute("SELECT id FROM examens")
exams = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT id FROM salles")
rooms = [row[0] for row in cursor.fetchall()]

# Assign each exam to 1-3 rooms randomly
for exam_id in exams:
    n_rooms = random.randint(1, 3)
    selected_rooms = random.sample(rooms, n_rooms)
    for salle_id in selected_rooms:
        cursor.execute(
            "INSERT INTO exam_salle_affectation (exam_id, salle_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (exam_id, salle_id)
        )

conn.commit()
cursor.close()
conn.close()
print("✅ exam_salle_affectation table populated successfully!")
