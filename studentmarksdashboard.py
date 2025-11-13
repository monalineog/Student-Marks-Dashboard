import streamlit as st
import pandas as pd

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Student Marks Dashboard",
    page_icon="📊",
    layout="centered"
)

# ---------- CUSTOM STYLING ----------
st.markdown("""
    <style>
        .main {
            background-color: #f5f7fa;
        }
        .stDataFrame {
            border-radius: 10px;
            overflow: hidden;
        }
        h1, h2, h3 {
            color: #333333;
        }
        .metric-container {
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
        }
        .stMetric {
            background: #ffffff;
            padding: 15px 25px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# ---------- APP TITLE ----------
st.title("📘 Student Marks Dashboard")
st.markdown("Add students and analyze their performance with class insights.")

# ---------- SESSION STATE (to store data dynamically) ----------
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
    # Compute totals and percentage
    df["Total Marks"] = df["Maths"] + df["Physics"] + df["English"]
    df["Percentage"] = (df["Total Marks"] / 300) * 100

    # Grade assignment function
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
    highest_score = df["Total Marks"].max()
    lowest_score = df["Total Marks"].min()

    # ---------- DISPLAY METRICS ----------
    col1, col2, col3 = st.columns(3)
    col1.metric("📈 Class Average (%)", class_avg)
    col2.metric("🏆 Highest Score", highest_score)
    col3.metric("📉 Lowest Score", lowest_score)

    # ---------- DISPLAY TABLE ----------
    st.markdown("🧾 Student Performance Table")
    st.dataframe(
        df.style.background_gradient(
            subset=["Percentage"],
            cmap="YlGn"
        ).format({"Percentage": "{:.2f}%"})
    )
else:
    st.info("👆 Add a student above to see the performance dashboard.")

# ---------- FOOTER ----------
st.markdown("---")
st.markdown("Made by Monali Neog")
