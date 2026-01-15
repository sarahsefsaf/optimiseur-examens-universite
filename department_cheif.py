import streamlit as st
import pandas as pd
from db.connection import get_connection

# -------------------------------------------------
# Page config
# -------------------------------------------------
def department_chief():
   # st.set_page_config(page_title="Department Chief Dashboard", layout="wide")
    st.title(" Department Chief Dashboard")
    st.success("Department Chief page loaded successfully ✅")

    # -------------------------------------------------
    # 1️⃣ Select Department
    # -------------------------------------------------
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, nom FROM departements ORDER BY nom")
    departments = cur.fetchall()
    dept_dict = {name: id for id, name in departments}

    selected_dept_name = st.selectbox(
        "Select Department:",
        options=list(dept_dict.keys())
    )
    selected_dept_id = dept_dict[selected_dept_name]

    if st.button("Show Department Overview"):
        # -------------------------------------------------
        # 2️⃣ Department Info
        # -------------------------------------------------
        cur.execute("""
            SELECT COUNT(*) FROM etudiants
            WHERE departement_id = %s
        """, (selected_dept_id,))
        num_students = cur.fetchone()[0]

        cur.execute("""
            SELECT COUNT(*) FROM modules
            WHERE departement_id = %s
        """, (selected_dept_id,))
        num_modules = cur.fetchone()[0]

        st.subheader(" Department Info")
        st.write({
            "Department": selected_dept_name,
            "Number of Students": num_students,
            "Number of Modules": num_modules
        })

        # -------------------------------------------------
        # 3️⃣ Exam Overview
        # -------------------------------------------------
        cur.execute("""
            SELECT
                e.id AS exam_id,
                m.nom AS module,
                e.niveau AS level,
                e.date_exam,
                e.heure_debut,
                COUNT(ers.etudiant_id) AS num_students,
                STRING_AGG(DISTINCT s.nom, ', ') AS rooms
            FROM examens e
            JOIN modules m ON m.id = e.module_id
            LEFT JOIN exam_room_students ers ON ers.exam_id = e.id
            LEFT JOIN salles s ON s.id = ers.salle_id
            WHERE m.departement_id = %s
            GROUP BY e.id, m.nom, e.niveau, e.date_exam, e.heure_debut
            ORDER BY e.date_exam, e.heure_debut
        """, (selected_dept_id,))

        exams = cur.fetchall()
        columns = ["Exam ID", "Module", "Level", "Date", "Start Time", "Number of Students", "Rooms"]
        df_exams = pd.DataFrame(exams, columns=columns)

        st.subheader(" Department Exam Schedule")
        st.dataframe(df_exams, use_container_width=True)

        # -------------------------------------------------
        # 4️⃣ Validation Checks
        # -------------------------------------------------
        st.subheader("✅ Validation Checks")

        # Exams without rooms
        exams_no_room = df_exams[df_exams["Rooms"].isnull()]
        if not exams_no_room.empty:
            st.error("❌ Some exams have no rooms assigned")
            st.dataframe(exams_no_room)
        else:
            st.success("✔ All exams have rooms assigned")

        # Students with more than one exam per day
        cur.execute("""
            SELECT i.etudiant_id, e.date_exam, COUNT(*)
            FROM inscriptions i
            JOIN examens e ON e.id = i.examen_id
            JOIN modules m ON m.id = e.module_id
            WHERE m.departement_id = %s
            GROUP BY i.etudiant_id, e.date_exam
            HAVING COUNT(*) > 1
        """, (selected_dept_id,))
        conflicts = cur.fetchall()

        if conflicts:
            st.error("❌ Some students have more than one exam in the same day")
            df_conflicts = pd.DataFrame(conflicts, columns=["Student ID", "Date", "Exam Count"])
            st.dataframe(df_conflicts)
        else:
            st.success("✔ No student has more than one exam per day")

        # Professors exceeding max supervisions per day
        cur.execute("""
            SELECT s.professeur_id, e.date_exam, COUNT(*)
            FROM surveillances s
            JOIN examens e ON e.id = s.examen_id
            JOIN modules m ON m.id = e.module_id
            WHERE m.departement_id = %s
            GROUP BY s.professeur_id, e.date_exam
            HAVING COUNT(*) > 3
        """, (selected_dept_id,))
        prof_conflicts = cur.fetchall()

        if prof_conflicts:
            st.error("❌ Some professors supervise more than 3 exams per day")
            df_prof_conflicts = pd.DataFrame(prof_conflicts, columns=["Professor ID", "Date", "Supervisions"])
            st.dataframe(df_prof_conflicts)
        else:
            st.success("✔ No professor supervises more than 3 exams per day")

    conn.close()
