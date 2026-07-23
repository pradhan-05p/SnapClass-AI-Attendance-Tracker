import streamlit as st
from src.database.db import create_attendance_logs
import time
@st.dialog(title="Attendance Reports")
def attendance_result_dialouge(df,logs):
    st.write("please review the attendance results below:")
    st.dataframe(df,hide_index=True,width="stretch")
    
    col1,col2 = st.columns(2,gap="small")
    
    with col1:
        if st.button("Discard",type="secondary"):
            st.rerun()
    
    with col2:
        if st.button("Confirm & Save",type="primary"):
            try:
                create_attendance_logs(logs)
                st.toast("Attendance logs saved successfully!",icon="✅")
                time.sleep(1)
                st.session_state.attendance_image = []
                st.rerun()
            except Exception as e:
                st.error(f"An error occurred while saving attendance: {e}", icon="❌")
