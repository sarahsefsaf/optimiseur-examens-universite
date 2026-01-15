import psycopg2

conn = psycopg2.connect(
    dbname="exam_optimization",
    user="postgres",
    password="hana1234",
    host="localhost"
)
cursor = conn.cursor()

# Clear previous conflicts
cursor.execute("DELETE FROM exam_conflicts")

# 1️⃣ Room capacity conflicts
cursor.execute("""
    INSERT INTO exam_conflicts (exam_id, conflict_type, conflict_detail)
    SELECT ers.exam_id, 'Room capacity',
           'Room ' || ers.salle_id || ' has ' || COUNT(*) || ' students'
    FROM exam_room_students ers
    JOIN salles s ON ers.salle_id = s.id
    GROUP BY ers.exam_id, ers.salle_id, s.capacite
    HAVING COUNT(*) > s.capacite
""")

# 2️⃣ Students assigned to multiple rooms for same exam
cursor.execute("""
    INSERT INTO exam_conflicts (exam_id, conflict_type, conflict_detail)
    SELECT ers.exam_id, 'Student double exam',
           'Student ' || ers.etudiant_id || ' assigned to multiple rooms'
    FROM exam_room_students ers
    GROUP BY ers.exam_id, ers.etudiant_id
    HAVING COUNT(*) > 1
""")

# 3️⃣ Exams with no professor assigned
cursor.execute("""
    INSERT INTO exam_conflicts (exam_id, conflict_type, conflict_detail)
    SELECT e.id, 'Professor missing', 
           'No professor assigned for exam ' || e.id
    FROM examens e
    LEFT JOIN surveillances ep ON e.id = ep.examen_id
    WHERE ep.professeur_id IS NULL
""")

conn.commit()
cursor.close()
conn.close()
print("✅ exam_conflicts table populated successfully!")
