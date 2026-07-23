import streamlit as st
from src.database.db import crete_attendance_logs
import time

def attendance_result_dialouge_voice(df,logs):
    st.write("please review the attendance results below:")
    st.dataframe(df,hide_index=True,width="stretch")
    
    col1,col2 = st.columns(2,gap="small")
    
    with col1:
        if st.button("Discard",type="secondary"):
            st.session_state.voice_attendance_results = None
            st.rerun()
    
    with col2:
        if st.button("Confirm & Save",type="primary"):
            try:
                crete_attendance_logs(logs)
                st.toast("Attendance logs saved successfully!",icon="✅")
                st.session_state.attendance_image = []
                st.session_state.voice_attendance_results = None
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"An error occurred while saving attendance: {e}", icon="❌")


@st.dialog(title="Attendance Reports (Voice)")
def attendance_result_dialouge(df,logs):
    if st.session_state.get("voice_attendance_results") is not None:
        attendance_result_dialouge_voice(
            df=st.session_state.voice_attendance_results[0],
            logs=st.session_state.voice_attendance_results[1]
        )
