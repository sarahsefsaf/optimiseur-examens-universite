import streamlit as st
import pandas as pd
from db.connection import get_connection

# -------------------------------------------------
# Page config
# -------------------------------------------------
def professor():
  #  st.set_page_config(page_title="Professor Supervision", layout="wide")

    st.title(" Professor Exam Supervision Schedule")
    st.success("Professor page loaded successfully ✅")

    # -------------------------------------------------
    # Input Professor ID
    # -------------------------------------------------
    professor_id = st.number_input(
        "Enter your Professor ID",
        min_value=73,
        step=1
    )

    if st.button("Show my supervision schedule"):

        conn = get_connection()
        cur = conn.cursor()

        # -------------------------------------------------
        # 1️⃣ Load professor info
        # -------------------------------------------------
        cur.execute("""
            SELECT p.id, p.nom, p.prenom, p.departement_id, d.nom AS departement_name
            FROM professeurs p
            JOIN departements d ON d.id = p.departement_id
            WHERE p.id = %s
        """, (professor_id,))
        prof = cur.fetchone()

        if not prof:
            st.error("❌ Professor not found")
            conn.close()
            st.stop()

        st.subheader(" Professor Information")
        st.write({
            "ID": prof[0],
            "Name": f"{prof[1]} {prof[2]}",
            "Department ID": prof[3],
            "Department Name": prof[4]
        })

        # -------------------------------------------------
        # 2️⃣ Load supervision schedule
        # -------------------------------------------------
        cur.execute("""
            SELECT 
                m.nom AS module,
                e.date_exam,
                e.heure_debut,
                '90 min' AS duration,
                s.id AS room_id
            FROM surveillances sv
            JOIN examens e ON e.id = sv.examen_id
            JOIN modules m ON m.id = e.module_id
            LEFT JOIN salles s ON s.id = (
                SELECT salle_id
                FROM exam_room_students ers
                WHERE ers.exam_id = e.id
                LIMIT 1
            )
            WHERE sv.professeur_id = %s
            ORDER BY e.date_exam, e.heure_debut
        """, (professor_id,))

        columns = ["Module", "Date", "Start Time", "Duration", "Room"]
        df = pd.DataFrame(cur.fetchall(), columns=columns)

        st.subheader(" My Supervision Schedule")
        st.dataframe(df, use_container_width=True)

        # -------------------------------------------------
        # 3️⃣ VALIDATION CHECKS
        # -------------------------------------------------
        st.subheader("✅ Validation Checks")

        # Check 1: max 3 exams per day
        cur.execute("""
            SELECT e.date_exam, COUNT(*)
            FROM surveillances sv
            JOIN examens e ON e.id = sv.examen_id
            WHERE sv.professeur_id = %s
            GROUP BY e.date_exam
            HAVING COUNT(*) > 3
        """, (professor_id,))
        conflicts = cur.fetchall()

        if conflicts:
            st.error("❌ Professor exceeds max 3 exams per day")
            st.write(conflicts)
        else:
            st.success("✔ Max 3 exams per day respected")

        # Check 2: same-time conflicts
        cur.execute("""
            SELECT e.date_exam, e.heure_debut, COUNT(*)
            FROM surveillances sv
            JOIN examens e ON e.id = sv.examen_id
            WHERE sv.professeur_id = %s
            GROUP BY e.date_exam, e.heure_debut
            HAVING COUNT(*) > 1
        """, (professor_id,))
        time_conflicts = cur.fetchall()

        if time_conflicts:
            st.error("❌ Professor has same-time exam conflicts")
            st.write(time_conflicts)
        else:
            st.success("✔ No same-time exam conflicts")

        conn.close()
