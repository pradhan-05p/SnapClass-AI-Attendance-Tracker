import streamlit as st
import pandas as pd
from datetime import date
from src.database.config import supabase

def get_teacher_subjects(teacher_id) -> pd.DataFrame:
    """Fetch subjects taught by this teacher, for the selectbox."""
    resp = supabase.table("subjects").select("subject_id, name").eq("teacher_id", teacher_id).execute()
    return pd.DataFrame(resp.data)


def get_subject_attendance(subject_id, target_date) -> pd.DataFrame:
    """
    Returns student_id, name, status (Present/Absent) for a subject on a given date,
    using the ispresent bool column in attendance_logs.
    """
    # 1. Students enrolled in this subject
    enrolled_resp = (
        supabase.table("subject_students")
        .select("student_id, students(student_id, name)")
        .eq("subject_id", subject_id)
        .execute()
    )
    
    if not enrolled_resp.data:
        st.warning(f"No students found enrolled for subject ={subject_id}")
        return pd.DataFrame(columns=["student_id", "name", "status","timestamp"])

    students_df = pd.DataFrame([
        {"student_id": row["student_id"], "name": row["students"]["name"]}
        for row in enrolled_resp.data
    ])

    # 2. Attendance rows for that subject + date (timestamp is timestamptz)
    start = target_date.isoformat()
    end = (pd.Timestamp(target_date) + pd.Timedelta(days=1)).date().isoformat()

    attendance_resp = (
        supabase.table("attendance_logs")
        .select("student_id, ispresent, timestamp")
        .eq("subject_id", subject_id)
        .gte("timestamp", start)
        .lt("timestamp", end)
        .execute()
    )
    attendance_df = pd.DataFrame(attendance_resp.data)

    # 3. Merge — default to Absent if no row was ever logged for that student that day
    if attendance_df.empty:
        students_df["status"] = "Absent"
        students_df["timestamp"] = "_"
    else:
        merged = students_df.merge(
            attendance_df[["student_id", "ispresent", "timestamp"]],
            on="student_id",
            how="left"
        )
        merged["status"] = merged["ispresent"].map({True: "Present", False: "Absent"})
        merged["status"] = merged["status"].fillna("Absent")  # no log row at all that day
        students_df = merged.drop(columns="ispresent")
    
    students_df["timestamp"] = pd.to_datetime(students_df["timestamp"]).dt.strftime("%H:%M:%S")

    return students_df.sort_values("name").reset_index(drop=True)

def teacher_tab_detailed_logs():
    # st.header("Under Development: will be live soon")
    teacher_id = st.session_state.teacher_data['teacher_id']
    subjects_df = get_teacher_subjects(teacher_id)

    if subjects_df.empty:
        st.warning("No subjects found for this teacher.")
    else:
        subject_name = st.selectbox("Select Subject", subjects_df["name"])
        subject_id = int(subjects_df.loc[subjects_df["name"] == subject_name, "subject_id"].values[0])

        selected_date = st.date_input("Select Date", value=date.today())

    if st.button("View Attendance"):
        log_df = get_subject_attendance(subject_id, selected_date)
        st.dataframe(log_df, use_container_width=True, hide_index=True)
        st.download_button(
            "Download CSV",
            log_df.to_csv(index=False),
            file_name=f"attendance_{subject_name}_{selected_date}.csv"
        )