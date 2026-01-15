import streamlit as st
import pandas as pd
from db.connection import get_connection


def student():
    st.title(" Student Exam Schedule")
    st.success("Student page loaded successfully ✅")

    # -------------------------------------------------
    # Input Student ID
    # -------------------------------------------------
    student_id = st.number_input(
        "Enter your Student ID",
        min_value=1,
        step=1
    )

    if st.button("Show my exams"):
        conn = get_connection()
        cur = conn.cursor()

        # -------------------------------------------------
        # 1️⃣ Load student info
        # -------------------------------------------------
        cur.execute("""
            SELECT e.id, e.nom, e.prenom, e.niveau, d.nom
            FROM etudiants e
            JOIN departements d ON d.id = e.departement_id
            WHERE e.id = %s
        """, (student_id,))
        student_row = cur.fetchone()

        if not student_row:
            st.error("❌ Student not found")
            conn.close()
            return

        st.subheader(" Student Information")
        st.write({
            "ID": student_row[0],
            "Name": f"{student_row[1]} {student_row[2]}",
            "Level": student_row[3],
            "Department": student_row[4]
        })

        # -------------------------------------------------
        # 2️⃣ Load exam schedule
        # -------------------------------------------------
        cur.execute("""
            SELECT
                m.nom AS module,
                ex.date_exam,
                ex.heure_debut,
                '90 min' AS duration,
                s.id AS room_id
            FROM inscriptions i
            JOIN examens ex ON ex.id = i.examen_id
            JOIN modules m ON m.id = ex.module_id
            LEFT JOIN exam_room_students ers
                   ON ers.exam_id = ex.id
                  AND ers.etudiant_id = i.etudiant_id
            LEFT JOIN salles s ON s.id = ers.salle_id
            WHERE i.etudiant_id = %s
            ORDER BY ex.date_exam, ex.heure_debut
        """, (student_id,))

        columns = ["Module", "Date", "Start Time", "Duration", "Room"]
        df = pd.DataFrame(cur.fetchall(), columns=columns)

        st.subheader(" My Exam Schedule")
        st.dataframe(df, use_container_width=True)

        # -------------------------------------------------
        # 3️⃣ VALIDATION CHECKS
        # -------------------------------------------------
        st.subheader("✅ Validation Checks")

        # Check 1: more than one exam per day
        cur.execute("""
            SELECT date_exam, COUNT(*)
            FROM inscriptions i
            JOIN examens e ON e.id = i.examen_id
            WHERE i.etudiant_id = %s
            GROUP BY date_exam
            HAVING COUNT(*) > 1
        """, (student_id,))
        conflicts = cur.fetchall()

        if conflicts:
            st.error("❌ More than one exam in the same day!")
            st.write(conflicts)
        else:
            st.success("✔ Max 1 exam per day respected")

        # Check 2: exams without room
        if df["Room"].isnull().any():
            st.error("❌ Some exams have no room assigned")
        else:
            st.success("✔ All exams have rooms assigned")

        conn.close()
