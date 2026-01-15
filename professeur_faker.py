import psycopg2
from faker import Faker
import random

# -----------------------------
# Database connection
# -----------------------------
DB_NAME = "exam_optimization"
DB_USER = "postgres"
DB_PASSWORD = "hana1234"
DB_HOST = "localhost"
DB_PORT = "5432"

fake = Faker(locale='fr_FR')

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
# Get all departments
# -----------------------------
cur.execute("SELECT id, nom FROM departements;")
departments = cur.fetchall()

# -----------------------------
# Generate professors per department
# -----------------------------
for dept_id, dept_name in departments:
    num_profs = random.randint(25, 30)
    for _ in range(num_profs):
        first_name = fake.first_name()
        last_name = fake.last_name()
        cur.execute(
            "INSERT INTO professeurs (nom, prenom, departement_id) VALUES (%s, %s, %s)",
            (last_name, first_name, dept_id)
        )

cur.close()
conn.close()

print("✓ Professors inserted successfully!")
