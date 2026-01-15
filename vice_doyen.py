import streamlit as st
import pandas as pd
from db.connection import get_connection

# --------------------------------------------------
# VICE-DOYEN DASHBOARD
# --------------------------------------------------
def vice_doyen():
   # st.set_page_config(page_title="Vice-Doyen Dashboard", layout="wide")
    st.title(" Vice-Doyen – Strategic Exam Dashboard")

    conn = get_connection()
    cur = conn.cursor()

    # ==================================================
    # 1️⃣ OVERVIEW METRICS
    # ==================================================
    st.subheader(" Global Overview")

    cur.execute("SELECT COUNT(*) FROM departements")
    dept_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM salles")
    room_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM etudiants")
    student_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM professeurs")
    prof_count = cur.fetchone()[0]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(" Departments", dept_count)
    col2.metric(" Rooms", room_count)
    col3.metric(" Students", student_count)
    col4.metric(" Professors", prof_count)

    # ==================================================
    # 2️⃣ ALERTS
    # ==================================================
    st.subheader("⚠️ Alerts & Risks")

    alerts = []

    # Rooms under-used (< 10 students)
    cur.execute("""
        SELECT esa.salle_id, COUNT(ers.etudiant_id)
        FROM exam_salle_affectation esa
        LEFT JOIN exam_room_students ers
            ON ers.salle_id = esa.salle_id
        GROUP BY esa.salle_id
        HAVING COUNT(ers.etudiant_id) < 10
    """)
    if cur.fetchall():
        alerts.append("⚠️ Some rooms are under-utilized (<10 students)")

    # Professors overload (>3 exams/day)
    cur.execute("""
        SELECT p.id, COUNT(*)
        FROM surveillances s
        JOIN examens e ON e.id = s.examen_id
        JOIN professeurs p ON p.id = s.professeur_id
        GROUP BY p.id, e.date_exam
        HAVING COUNT(*) > 3
    """)
    if cur.fetchall():
        alerts.append("⚠️ Some professors exceed daily supervision limit")

    # Exams without rooms
    cur.execute("""
        SELECT id
        FROM examens
        WHERE date_exam IS NOT NULL
          AND NOT EXISTS (
              SELECT 1
              FROM exam_salle_affectation
              WHERE exam_id = examens.id
          )
    """)
    if cur.fetchall():
        alerts.append("❌ Exams scheduled without rooms")

    if alerts:
        for a in alerts:
            st.warning(a)
    else:
        st.success("✅ No critical alerts detected")

    # ==================================================
    # 3️⃣ KPI SECTION
    # ==================================================
    st.subheader(" Key Performance Indicators")

    # Room utilization %
    cur.execute("""
            
        SELECT
            COUNT(ers.etudiant_id)::float / NULLIF(COUNT(DISTINCT esa.salle_id) * 20,0) * 100   
            
        FROM exam_room_students ers
        JOIN exam_salle_affectation esa ON esa.salle_id = ers.salle_id
    """)
    room_util = cur.fetchone()[0] or 0

    # Avg exams per professor
    cur.execute("""
        SELECT AVG(cnt)
        FROM (
            SELECT COUNT(*) cnt
            FROM surveillances
            GROUP BY professeur_id
        ) t
    """)
    avg_prof = cur.fetchone()[0] or 0

    k1, k2 = st.columns(2)
    k1.metric(" Room Utilization", f"{room_util:.1f}%", "Target: 75%")
    k2.metric(" Avg Exams / Professor", f"{avg_prof:.1f}", "Target: 3")

    # ==================================================
    # 4️⃣ DEPARTMENT RANKING
    # ==================================================
    st.subheader(" Department Ranking (Room Usage)")

    cur.execute("""
        SELECT d.nom, COUNT(ers.etudiant_id) AS total_students
        FROM departements d
        JOIN modules m ON m.departement_id = d.id
        JOIN examens e ON e.module_id = m.id
        LEFT JOIN exam_room_students ers ON ers.exam_id = e.id
        GROUP BY d.nom
        ORDER BY total_students DESC
    """)

    rank_df = pd.DataFrame(
        cur.fetchall(),
        columns=["Department", "Students Examined"]
    )

    st.dataframe(rank_df, use_container_width=True)

    # ==================================================
    # 5️⃣ VALIDATION STATUS (LOGICAL)
    # ==================================================
    st.subheader("✅ Validation Status")

    cur.execute("""
        SELECT d.nom,
               COUNT(e.id) FILTER (WHERE e.date_exam IS NOT NULL) AS scheduled,
               COUNT(e.id) AS total
        FROM departements d
        JOIN modules m ON m.departement_id = d.id
        JOIN examens e ON e.module_id = m.id
        GROUP BY d.nom
    """)

    val_df = pd.DataFrame(
        cur.fetchall(),
        columns=["Department", "Scheduled Exams", "Total Exams"]
    )

    val_df["Status"] = val_df.apply(
        lambda r: "✅ Ready" if r["Scheduled Exams"] == r["Total Exams"]
        else "⏳ Pending",
        axis=1
    )

    st.dataframe(val_df, use_container_width=True)

    conn.close()
