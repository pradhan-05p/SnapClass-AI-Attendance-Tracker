import streamlit as st
from src.database.db import create_subject
import time
from src.database.config import supabase
from src.database.db import enroll_student_to_subject

@st.dialog(title="Quick Enrollment")
def auto_enroll_diaglogue(join_code):
    student_id = st.session_state.student_data['student_id']
    res = supabase.table('subjects').select('subject_id,name,subject_code').eq('subject_code', join_code).execute()
    if not res.data:
        st.error("Invalid subject code. Please check the code and try again.", icon="❌")
        if st.button("Close", type="primary", width="stretch"):
            st.query_params.clear()
    
    subject = res.data[0]
    check = supabase.table('subject_students').select('*').eq('subject_id', subject['subject_id']).eq('student_id', student_id).execute()
    if check.data:
        st.warning("You are already enrolled in this subject.", icon="⚠️")
        if st.button("Got it", type="primary"):
            st.query_params.clear()
            st.rerun()
    st.markdown(f"Would you like to enroll in {subject['name']}(Code: {subject['subject_code']})?")
    
    
    c1, c2 = st.columns(2)
    
    with c1:
        if st.button("No thanks", type="primary"):
            st.query_params.clear()
            st.rerun()
    with c2:
        if st.button("Yes Enroll Now", type="primary"):
            enroll_student_to_subject(student_id, subject['subject_id'])
            st.success(f"You have successfully enrolled in {subject['name']}!", icon="✅")
            time.sleep(1)
            st.query_params.clear()
            st.rerun()
    
    
    
    
    