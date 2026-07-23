import streamlit as st
from src.database.db import create_attendance_logs
import logging
from src.database.config import supabase
import time
logger = logging.getLogger(__name__)
def attendance_result_dialouge(df, logs,subject_id):
    subject_res = supabase.table("subjects").select("name").eq("subject_id", subject_id).execute()
    subject_name = subject_res.data[0]['name'] if subject_res.data else "Unknown Subject"
    st.write(f"**Date:** {__import__('datetime').datetime.now().strftime('%A, %d %B %Y')}")
    st.write(f"**Subject:** {subject_name}")
    st.write('Review the attendance results below. You can either discard the results or confirm and save them to the database.')
    st.dataframe(df, hide_index=True, width="stretch")
    col1, col2 = st.columns(2, gap="small")

    with col1:
        if st.button("Discard", type="secondary", key="voice_discard_btn"):
            st.session_state.voice_attendance_results = None
            st.rerun()

    with col2:
        if st.button("Confirm & Save", type="primary", key="voice_confirm_btn"):
            with st.spinner("Saving attendance logs..."):
                try:
                    resp = create_attendance_logs(logs)
                    time.sleep(1)  
                    logger.info("create_attendance_logs returned: %r", resp)
                except Exception as e:
                    logger.exception("Failed to save attendance logs")
                    st.error(f"Something went wrong while saving: {e}")
                    return

            if resp:
                st.session_state.voice_attendance_results = None
                st.session_state.attendance_save_success = True
                st.toast("Attendance logs saved successfully!", icon="✅")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Failed to save attendance logs — insert returned no data.")