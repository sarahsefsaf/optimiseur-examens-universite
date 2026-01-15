import psycopg2
import random

# -----------------------------
# Database connection
# -----------------------------
DB_NAME = "exam_optimization"
DB_USER = "postgres"
DB_PASSWORD = "hana1234"
DB_HOST = "localhost"
DB_PORT = "5432"

# -----------------------------
# Connect to DB
# -----------------------------
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
conn.autocommit = True
cur = conn.cursor()

# -----------------------------
# Fetch all exams with module departments and exam date
# -----------------------------
cur.execute("""
    SELECT e.id, m.departement_id, e.date_exam
    FROM examens e
    JOIN modules m ON e.module_id = m.id
""")
exams = cur.fetchall()

# -----------------------------
# Fetch all professors
# -----------------------------
cur.execute("SELECT id, departement_id FROM professeurs;")
professors = cur.fetchall()

# -----------------------------
# Clear previous surveillances
# -----------------------------
cur.execute("TRUNCATE TABLE surveillances RESTART IDENTITY CASCADE;")

# -----------------------------
# Assign professors to exams
# -----------------------------
surveillances = []

for exam_id, dept_id, exam_date in exams:
    # 1️⃣ Professors from same department
    dept_profs = [p for p in professors if p[1] == dept_id]
    assigned_count = 0

    # Shuffle for randomness
    random.shuffle(dept_profs)

    for prof_id, _ in dept_profs:
        # Check max 3 exams per day
        cur.execute("""
            SELECT COUNT(*) FROM surveillances s
            JOIN examens e ON s.examen_id = e.id
            WHERE s.professeur_id = %s AND e.date_exam = %s
        """, (prof_id, exam_date))
        count = cur.fetchone()[0]

        if count < 3:
            surveillances.append((prof_id, exam_id))
            assigned_count += 1
        if assigned_count >= 3:
            break

    # 2️⃣ Professors from other departments if needed
    if assigned_count < 3:
        other_profs = [p for p in professors if p[1] != dept_id]
        random.shuffle(other_profs)
        for prof_id, _ in other_profs:
            cur.execute("""
                SELECT COUNT(*) FROM surveillances s
                JOIN examens e ON s.examen_id = e.id
                WHERE s.professeur_id = %s AND e.date_exam = %s
            """, (prof_id, exam_date))
            count = cur.fetchone()[0]

            if count < 3:
                surveillances.append((prof_id, exam_id))
                assigned_count += 1
            if assigned_count >= 3:
                break

    # 3️⃣ Log conflict if still < 3
    if assigned_count < 3:
        cur.execute("""
            INSERT INTO exam_conflicts(exam_id, conflict_type, conflict_detail)
            VALUES (%s, 'Not enough professors', %s)
        """, (exam_id, f"Assigned {assigned_count} professors, needed 3"))

# -----------------------------
# Insert surveillances
# -----------------------------
cur.executemany(
    "INSERT INTO surveillances (professeur_id, examen_id) VALUES (%s, %s)",
    surveillances
)

print(f"✅ Successfully assigned {len(surveillances)} surveillances!")

# -----------------------------
# Close connection
# -----------------------------
cur.close()
conn.close()
print("🔚 Professors assignment complete!")
