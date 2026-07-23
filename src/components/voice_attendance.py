import streamlit as st
import time
from src.database.config import supabase
import pandas as pd
from src.pipelines.voice_pipeline import process_bluk_audio
from datetime import datetime
from src.components.attendance_voice_dialouge import attendance_result_dialouge
@st.dialog(title="Voice Attendance")
def voice_attendance_dialogue(selected_subject_id):
    st.write("Record The class Voice One by one")
    audio_data = None
    
    audio_data = st.audio_input("Click the button below to record your voice.")
    
    if st.button("Analyze Voice", type="primary", width="stretch"):
        with st.spinner("Analyzing voice..."):
            time.sleep(2)
        
            enrolled_res = supabase.table("subject_students").select("*,students(*)").eq("subject_id", selected_subject_id).execute()
            enrolled_students = enrolled_res.data
                                
            if not enrolled_students:
                st.warning("No students are enrolled in this subject.", icon="⚠️")
                return
            candidate_dict = {
                s['students']['student_id']: s['students']['voice_embeddings'] 
                for s in enrolled_students if s['students']['voice_embeddings']
            }
            
            if not candidate_dict:
                st.warning("No voice embeddings found for enrolled students.", icon="⚠️")
                return
            audio_bytes = audio_data.read()
            
            detected_scores = process_bluk_audio(audio_bytes, candidate_dict)
            
            results,attendance_logs = [],[]
            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            
            for node in enrolled_students:
                student = node['students']
                scores = detected_scores.get(int(student['student_id']),0.0)
                is_present = bool(scores > 0)
                results.append({
                    "Name": student['name'],
                    "Id": student['student_id'],
                    "Score": scores if is_present else "Not Detected",
                    "Status": "Present ✅" if is_present else "Absent❌"
                    })
                attendance_logs.append({
                    "student_id": student['student_id'],
                    "subject_id": selected_subject_id,
                    "timestamp": current_timestamp,
                    "ispresent": bool(is_present)
                })  
            st.session_state.voice_attendance_results = (pd.DataFrame(results), attendance_logs)    
            
            if st.session_state.voice_attendance_results:
                results_df, attendance_logs = st.session_state.voice_attendance_results
                st.divider()
                attendance_result_dialouge(results_df, attendance_logs)
                st.success("Voice analysis complete! Attendance has been recorded.", icon="✅")