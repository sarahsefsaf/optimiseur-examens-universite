import streamlit as st
import pandas as pd
from db.connection import get_connection

# --------------------------------------------------
# ADMIN PAGE
# --------------------------------------------------
def admin():
    #st.set_page_config(page_title="Admin Dashboard", layout="wide")
    st.title(" Admin – Exam Validation & Supervision Support")

    conn = get_connection()
    cur = conn.cursor()

    # --------------------------------------------------
    # 1️⃣ Department selection
    # --------------------------------------------------
    cur.execute("SELECT id, nom FROM departements ORDER BY nom")
    departments = cur.fetchall()

    dept_map = {name: id for id, name in departments}

    dept_name = st.selectbox(
        " Select Department",
        options=list(dept_map.keys())
    )
    dept_id = dept_map[dept_name]

    # --------------------------------------------------
    # 2️⃣ Level selection
    # --------------------------------------------------
    cur.execute("""
        SELECT DISTINCT e.niveau
        FROM examens e
        JOIN modules m ON m.id = e.module_id
        WHERE m.departement_id = %s
        ORDER BY e.niveau
    """, (dept_id,))

    levels = [row[0] for row in cur.fetchall()]

    niveau = st.selectbox(" Select Level", levels)

    # --------------------------------------------------
    # 3️⃣ Exams table (core view)
    # --------------------------------------------------
    st.subheader(" Exams Overview")

    cur.execute("""
        SELECT
            e.id AS exam_id,
            m.nom AS module,
            e.date_exam,
            e.heure_debut,
            STRING_AGG(DISTINCT s.nom, ', ') AS rooms,
            STRING_AGG(DISTINCT p.nom || ' ' || p.prenom, ', ') AS professors
        FROM examens e
        JOIN modules m ON m.id = e.module_id
        LEFT JOIN exam_salle_affectation esa ON esa.exam_id = e.id
        LEFT JOIN salles s ON s.id = esa.salle_id
        LEFT JOIN surveillances sv ON sv.examen_id = e.id
        LEFT JOIN professeurs p ON p.id = sv.professeur_id
        WHERE m.departement_id = %s
          AND e.niveau = %s
        GROUP BY e.id, m.nom, e.date_exam, e.heure_debut
        ORDER BY e.date_exam, e.heure_debut
    """, (dept_id, niveau))

    exams_df = pd.DataFrame(
        cur.fetchall(),
        columns=[
            "Exam ID", "Module", "Date", "Start Time",
            "Rooms", "Professors"
        ]
    )

    st.dataframe(exams_df, use_container_width=True)

    # --------------------------------------------------
    # 4️⃣ Time-based supervision analysis
    # --------------------------------------------------
    st.subheader(" Find Available Professors (Backup)")

    exam_dates = exams_df["Date"].dropna().unique()
    exam_times = exams_df["Start Time"].dropna().unique()

    if len(exam_dates) > 0 and len(exam_times) > 0:
        selected_date = st.selectbox(" Select Date", exam_dates)
        selected_time = st.selectbox(" Select Time", exam_times)

        cur.execute("""
            SELECT p.id, p.nom, p.prenom, d.nom
            FROM professeurs p
            JOIN departements d ON d.id = p.departement_id
            WHERE NOT EXISTS (
                SELECT 1
                FROM surveillances s
                JOIN examens e ON e.id = s.examen_id
                WHERE s.professeur_id = p.id
                  AND e.date_exam = %s
                  AND e.heure_debut = %s
            )
            ORDER BY d.nom, p.nom
        """, (selected_date, selected_time))

        free_profs = cur.fetchall()

        free_df = pd.DataFrame(
            free_profs,
            columns=["ID", "Last Name", "First Name", "Department"]
        )

        if free_df.empty:
            st.warning("⚠️ No available professors at this time")
        else:
            st.success(f"✅ {len(free_df)} professors available")
            st.dataframe(free_df, use_container_width=True)

    conn.close()
