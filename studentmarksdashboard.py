import streamlit as st
import pandas as pd

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------- CUSTOM STYLING ----------
st.markdown("""
    <style>
        body {
            background-color: #f8fafc;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        .stMetric {
            background: white;
            padding: 15px 25px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        div[data-testid="stForm"] {
            background-color: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
    </style>
""", unsafe_allow_html=True)

# ---------- PAGE TITLE ----------
st.title("📘 Student Performance Dashboard")
st.markdown("Manage student marks, analyze performance, and wrangle data easily!")

# ---------- SESSION STATE ----------
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["Name", "Maths", "Physics", "English"])

# ---------- ADD NEW STUDENT ----------
st.subheader("➕ Add New Student Record")
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
            "Name": [name.strip()],
            "Maths": [maths],
            "Physics": [physics],
            "English": [english]
        })
        st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
        st.success(f"✅ Added {name}'s record successfully!")

# ---------- WORKING DATAFRAME ----------
df = st.session_state.df.copy()

if not df.empty:
    # ---------------- DATA WRANGLING CONCEPTS ----------------
    # Clean column names (if needed)
    df.columns = df.columns.str.strip().str.title()

    # Fill missing values with 0 (handling NaN)
    df.fillna(0, inplace=True)

    # Sort data by Name
    df.sort_values(by="Name", inplace=True, ignore_index=True)

    # Compute new derived columns
    df["Total Marks"] = df["Maths"] + df["Physics"] + df["English"]
    df["Percentage"] = (df["Total Marks"] / 300) * 100

    # Grade Assignment Function
    def assign_grade(p):
        if p >= 90:
            return "A"
        elif p >= 80:
            return "B"
        elif p >= 70:
            return "C"
        elif p >= 60:
            return "D"
        else:
            return "F"

    df["Grade"] = df["Percentage"].apply(assign_grade)

    # ---------------- CLASS STATISTICS ----------------
    class_avg = round(df["Percentage"].mean(), 2)
    highest_score = int(df["Total Marks"].max())
    lowest_score = int(df["Total Marks"].min())

    # ---------------- DISPLAY METRICS ----------------
    st.markdown("### 📊 Class Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("📈 Class Average (%)", class_avg)
    col2.metric("🏆 Highest Score", highest_score)
    col3.metric("📉 Lowest Score", lowest_score)

    # ---------------- WRANGLING TOOLS ----------------
    st.markdown("### 🔍 Data Wrangling & Filtering")
    st.write("You can use these tools to clean and explore your dataset.")

    # Filter by Grade
    grade_filter = st.selectbox("Filter by Grade:", options=["All"] + sorted(df["Grade"].unique().tolist()))
    filtered_df = df if grade_filter == "All" else df[df["Grade"] == grade_filter]

    # Sort by percentage
    sort_order = st.radio("Sort by Percentage:", ["Descending", "Ascending"])
    filtered_df = filtered_df.sort_values(by="Percentage", ascending=(sort_order == "Ascending"))

    # ---------------- DISPLAY TABLE ----------------
    st.markdown("### 🧾 Student Performance Table")
    display_df = filtered_df.copy()
    display_df["Percentage"] = display_df["Percentage"].map("{:.2f}%".format)
    st.dataframe(display_df, use_container_width=True)

    # ---------------- DOWNLOAD BUTTON ----------------
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name="student_results_filtered.csv",
        mime="text/csv"
    )

    # ---------------- SUMMARY SECTION ----------------
    st.markdown("### 🧮 Data Wrangling Summary")
    st.write(f"""
    **Data Cleaning Applied:**
    - Stripped and standardized column names  
    - Filled missing values with 0  
    - Sorted alphabetically by student name  

    **Derived Columns:**
    - `Total Marks` = Maths + Physics + English  
    - `Percentage` = (Total Marks / 300) × 100  
    - `Grade` assigned based on percentage thresholds  
    """)

else:
    st.info("👆 Add at least one student above to see analytics and wrangling tools.")

# ---------- FOOTER ----------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit — includes Data Wrangling, Analysis & Visualization Concepts.")
