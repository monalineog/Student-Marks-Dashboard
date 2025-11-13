import streamlit as st
import pandas as pd

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Student Marks Dashboard",
    page_icon="📊",
    layout="centered"
)

# ---------- PAGE TITLE ----------
st.title("📘 Student Marks Dashboard")
st.markdown("Add students and analyze their performance with class insights.")

# ---------- SESSION STATE ----------
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["Name", "Maths", "Physics", "English"])

# ---------- ADD STUDENT FORM ----------
st.subheader("➕ Add New Student")
with st.form("add_student_form", clear_on_submit=True):
    name = st.text_input("Student Name")
    maths = st.number_input("Maths Marks", min_value=0, max_value=100, step=1)
    physics = st.number_input("Physics Marks", min_value=0, max_value=100, step=1)
    english = st.number_input("English Marks", min_value=0, max_value=100, step=1)
    submitted = st.form_submit_button("Add Student")

if submitted:
    if name.strip() == "":
        st.warning("⚠️ Please enter a valid student name.")
    else:
        new_row = pd.DataFrame({
            "Name": [name],
            "Maths": [maths],
            "Physics": [physics],
            "English": [english]
        })
        st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
        st.success(f"✅ Added {name}'s record successfully!")

# ---------- DATA PROCESSING ----------
df = st.session_state.df.copy()

if not df.empty:
    # Calculate total marks and percentage
    df
