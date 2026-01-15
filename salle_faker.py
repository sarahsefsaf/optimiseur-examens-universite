import psycopg2

# -----------------------------
# Database connection
# -----------------------------
DB_NAME = "exam_optimization"
DB_USER = "postgres"
DB_PASSWORD = "hana1234"
DB_HOST = "localhost"
DB_PORT = "5432"

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
# Optional: get department IDs to randomly assign rooms
# -----------------------------
cur.execute("SELECT id FROM departements;")
departments = [d[0] for d in cur.fetchall()]

# -----------------------------
# Insert 100 unique rooms
# -----------------------------
for i in range(1, 101):
    room_name = f"Salle {i}"
    capacite = 30 + (i % 20)  # just some variation: 30–49 seats
    dept_id = departments[i % len(departments)]  # distribute among departments
    cur.execute(
        "INSERT INTO salles (nom, capacite, departement_id) VALUES (%s, %s, %s)",
        (room_name, capacite, dept_id)
    )

cur.close()
conn.close()
print("✓ 100 salles inserted successfully!")
