import streamlit as st
import time
import pandas as pd
from datetime import datetime
from src.database.config import supabase
from src.pipelines.voice_pipeline import process_bluk_audio
from src.components.attendance_voice_dialouge import attendance_result_dialouge

@st.dialog(title="Voice Attendance")
def voice_attendance_dialogue(selected_subject_id):
    pending = st.session_state.get("voice_attendance_results")
    st.session_state.selected_subject_name = selected_subject_id 
    if pending:
        st.divider()
        attendance_result_dialouge(pending["results_df"], pending["attendance_logs"], pending["subject_id"])
        return

    st.write("Record The class Voice One by one")
    audio_data = st.audio_input("Click the button below to record your voice.")
    if audio_data is None:
        st.warning("Please record your voice before analyzing.", icon="⚠️")
        return

    if st.button("Analyze Voice", type="primary", width="stretch"):
        with st.spinner("Analyzing voice..."):
            enrolled_res = supabase.table("subject_students").select("*,students(*)").eq("subject_id", selected_subject_id).execute()
            enrolled_students = enrolled_res.data

            if not enrolled_students:
                st.warning("No students are enrolled in this subject.", icon="⚠️")
                return

            candidate_dict = {
                s['students']['student_id']: s['students']['voice_embeddings']
                for s in enrolled_students if s.get('students') and s['students'].get('voice_embeddings')
            }
            if not candidate_dict:
                st.warning("No voice embeddings found for enrolled students.", icon="⚠️")
                return

            audio_bytes = audio_data.read()
            detected_scores = process_bluk_audio(audio_bytes, candidate_dict)

            results, attendance_logs = [], []
            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            for node in enrolled_students:
                student = node['students']
                scores = detected_scores.get(int(student['student_id']), 0.0)
                is_present = bool(scores > 0)
                results.append({
                    "Name": student['name'],
                    "Id": student['student_id'],
                    "Score": scores if is_present else None,
                    "Status": "Present ✅" if is_present else "Absent❌"
                })
                attendance_logs.append({
                    "student_id": student['student_id'],
                    "subject_id": selected_subject_id,
                    "timestamp": current_timestamp,
                    "ispresent": bool(is_present)
                })

            results_df = pd.DataFrame(results)
            st.session_state.voice_attendance_results = {
                'results_df': results_df,
                'attendance_logs': attendance_logs,
                'subject_id': selected_subject_id
            }
            st.rerun() 