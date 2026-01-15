import psycopg2
from faker import Faker

fake = Faker('fr_FR')

conn = psycopg2.connect(
    dbname="exam_optimization",
    user="postgres",
    password="hana1234",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# -------------------------
# Fetch departments
# -------------------------
cur.execute("SELECT id FROM departements ORDER BY id;")
departements = [d[0] for d in cur.fetchall()]

levels = ['L1', 'L2', 'L3', 'M1', 'M2']
students_per_department = 1857

base = students_per_department // len(levels)   # 371
rest = students_per_department % len(levels)    # 2

# -------------------------
# Reset table
# -------------------------
cur.execute("TRUNCATE TABLE etudiants RESTART IDENTITY CASCADE;")
conn.commit()

total = 0

try:
    for dept_id in departements:
        for i, level in enumerate(levels):
            count = base + (1 if i < rest else 0)

            for _ in range(count):
                cur.execute("""
                    INSERT INTO etudiants (nom, prenom, departement_id, niveau)
                    VALUES (%s, %s, %s, %s)
                """, (
                    fake.last_name()[:100],
                    fake.first_name()[:100],
                    dept_id,
                    level
                ))
                total += 1

        print(f"✔ Department {dept_id} done → total = {total}")

    conn.commit()
    print(f"\n✅ SUCCESS: {total} students inserted")

except Exception as e:
    conn.rollback()
    print("❌ ERROR:", e)

finally:
    cur.close()
    conn.close()
