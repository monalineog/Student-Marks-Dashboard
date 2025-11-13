import streamlit as st
import pandas as pd

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Student Marks Dashboard",
    page_icon="📊",
    layout="centered"
)

# ---------- APP TITLE ----------
st.title("📘 Student Marks Dashboard")
st.markdown("Add students and analyze their performance with class insights.")

# ---------- SESSION STATE ----------
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["Name", "Maths", "Physics", "English"])

# ---------- ADD NEW STUDENT ----------
st.subheader("➕ Add New Student")
with st.form("add_student_form", clear_on_submit=True):
    name = st.text_input("Student Name")
    maths = st.number_input("Maths Marks", 0, 100, step=1)
    physics = st.number_input("Physics Marks", 0, 100, step=1)
    english = st.number_input("English Marks", 0, 100, step=1)
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

# ---------- PROCESS DATA ----------
df = st.session_state.df.copy()

if not df.empty:
    # Calculate totals and grades
    df["Total Marks"] = df["Maths"] + df["Physics"] + df["English"]
    df["Percentage"] = (df["Total Marks"] / 300) * 100

    def assign_grade(avg):
        if avg >= 90:
            return "A"
        elif avg >= 80:
            return "B"
        elif avg >= 70:
            return "C"
        elif avg >= 60:
            return "D"
        else:
            return "F"

    df["Grade"] = df["Percentage"].apply(assign_grade)

    # ---------- CLASS STATS ----------
    class_avg = round(df["Percentage"].mean(), 2)
    h
