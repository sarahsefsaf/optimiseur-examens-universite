import streamlit as st

from department_cheif import department_chief
from professeur import professor
from vice_doyen import vice_doyen

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title=" Exam Optimization System",
    layout="wide"
)

# -----------------------------
# Sidebar navigation
# -----------------------------
st.sidebar.title(" User Access")

user_role = st.sidebar.radio(
    "Choose user type:",
    [
        " Home",
        " Student",
        # Future:
        " Professor",
        " Department Chief",
        " Admin",
        " Vice-Doyen"
    ]
)

# -----------------------------
# Home Page
# -----------------------------
if user_role == " Home":
    st.title(" Exam Optimization Platform")

    st.markdown("""
    ### Welcome  
    This system allows:
    - Students to view their exams
    - Professors to view supervision schedules
    - Administration to validate constraints

    **Select a user role from the sidebar to continue.**
    """)

# -----------------------------
# Student Page
# -----------------------------
elif user_role == " Student":
    try:
        from student import student
        student()
    except Exception as e:
        st.error("❌ Failed to load Student Page")
        st.exception(e)
# -----------------------------
# Professor Page
# -----------------------------
elif user_role == " Professor":
    try:
        from professeur import professor
        professor()
    except Exception as e:
        st.error("❌ Failed to load Professor Page")
        st.exception(e)
# -----------------------------
# Department Chief Page
# -----------------------------
elif user_role == " Department Chief":
    try:
        from department_cheif import department_chief
        department_chief()
    except Exception as e:
        st.error("❌ Failed to load Department Chief Page")
        st.exception(e)
# -----------------------------
# Admin Page
# -----------------------------
elif user_role == " Admin":
    try:
        from admin import admin
        admin()
    except Exception as e:
        st.error("❌ Failed to load Admin Page")
        st.exception(e)


 # -----------------------------
# Vice-Doyen Page
# -----------------------------
elif user_role == " Vice-Doyen":
    try:
        from vice_doyen import vice_doyen
        vice_doyen()
    except Exception as e:
        st.error("❌ Failed to load Vice-Doyen Page")
        st.exception(e)