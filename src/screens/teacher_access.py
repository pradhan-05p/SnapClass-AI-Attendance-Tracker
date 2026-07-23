import streamlit as st
import numpy as np
import pandas as pd
from src.components.header import header_dashboard
from src.ui.base_layout import style_base_layout, style_background_dashboard
from src.components.footer import footer_home_dashboard
from src.components.dialouge_create_subject import create_dialouge_subject
from src.components.subject_card import subject_card
from src.components.share_dialouge_qr import share_sub_dialogue
from src.components.dialouge_add_photo import add_photos_dialogue
from src.components.attendance_to_result_dialouge import attendance_result_dialouge
from src.pipelines.face_pipeline import predict_attendance
from src.database.config import supabase
from src.components.voice_attendance import voice_attendance_dialogue
from src.database.db import get_teacher_attendance_logs

from datetime import datetime

from src.database.db import get_teacher_subjects
def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.subheader("Take AI Attendance")
    if 'attendance_image' not in st.session_state:
        st.session_state.attendance_image = []
        
    subjects = get_teacher_subjects(teacher_id)
    if not subjects:
        st.info("No subjects found. Please create a new subject to take attendance.", icon="ℹ️")
        return
    subject_options = {f"{s['name']} - ({s['subject_code']})" : s['subject_id'] for s in subjects}
    col1, col2 = st.columns([3,1])
    with col1:
        selected_subject_label = st.selectbox("Select Subject", options=list(subject_options.keys()))
    with col2:
        st.markdown("""<div style="height: 25px;"></div> """,unsafe_allow_html=True)
        if st.button("Add Photos",type="primary",icon=":material/photo_prints:",key="add_photos_button",width="stretch"):
            add_photos_dialogue() 
    
    selected_subject_id = subject_options[selected_subject_label]
    st.divider()

    if st.session_state.attendance_image:
        st.subheader("Added Images")
        gallery_cols = st.columns(4)
        for idx, img in enumerate(st.session_state.attendance_image):
            with gallery_cols[idx % 4]:
                st.image(img, caption=f"Image {idx+1}",width='stretch')
        
    has_photos = bool(st.session_state.attendance_image)
    c1,c2,c3 = st.columns(3,gap="medium")
    
    with c1:
        if st.button("Clear All Photos",type="secondary",icon=":material/delete:",width="stretch",disabled=not has_photos):
            st.session_state.attendance_image = []
            st.info("All photos cleared successfully!", icon="✅")
            st.rerun()
    with c2:
        if st.button("Run Face Recognition",type="tertiary",icon=":material/face:",width="stretch",disabled=not has_photos):
            with st.spinner("Running face recognition..."): 
                all_detected_ids = {}
                
                for idx,img in enumerate(st.session_state.attendance_image):
                    img_np = np.array(img.convert("RGB"))
                    detected,_,_ = predict_attendance(img_np)
                    
                    if detected:
                        for sid in detected:
                            student_id = int(sid)
                            all_detected_ids.setdefault(student_id, []).append(f"Image {idx+1}")
                            
                            
                enrolled_res = supabase.table("subject_students").select("*,students(*)").eq("subject_id", selected_subject_id).execute()
                enrolled_students = enrolled_res.data
                
                if not enrolled_students:
                    st.warning("No students are enrolled in this subject.", icon="⚠️")
                else:
                    results,attendance_logs = [],[]
                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                    
                    for node in enrolled_students:
                        student = node['students']
                        sources = all_detected_ids.get(int(student['student_id']), [])
                        is_present = len(sources) > 0
                        results.append({
                            "Name": student['name'],
                            "Id": student['student_id'],
                            "Sources": " ,".join(sources) if is_present else "Not Detected",
                            "Status": "Present ✅" if is_present else "Absent❌"
                            })
                        attendance_logs.append({
                            "student_id": student['student_id'],
                            "subject_id": selected_subject_id,
                            "timestamp": current_timestamp,
                            "ispresent": bool(is_present)
                        })  
                    attendance_result_dialouge(pd.DataFrame(results),attendance_logs)
    with c3:
        if st.button("Voice Attendance",type="tertiary",icon=":material/mic:",width="stretch"):
            voice_attendance_dialogue(selected_subject_id)
        

def teacher_tab_manage_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.header("Manage Attendance")
    with col2:
        st.markdown("""<div style="height: 20px;"></div> """,unsafe_allow_html=True)
        if st.button("create New Subject",width="stretch"):
            create_dialouge_subject(teacher_id)
        
    # listing all subjects for the teacher
    subjects = get_teacher_subjects(teacher_id)
    
    if subjects:
        for sub in subjects:
            stats = [
                ("👥","Students",sub['total_students']),
                ("📅","Total Classes",sub['total_class'])
            ]
            def share_button():
                if st.button(f"Share Code : {sub['name']} ", type="secondary", width="content",icon=":material/share:", icon_position="left",key=f"share_{sub['subject_code']}"):
                    share_sub_dialogue(sub['subject_code'],sub['name'])
                st.space()
            subject_card(
                name = sub['name'],
                code = sub['subject_code'],
                section = sub['section'],
                stats = stats,
                footer_callback = share_button
            )
    else:
        st.info("No subjects found. Please create a new subject to manage attendance.", icon="ℹ️")
        
    

def teacher_tab_attendance_logs():
    st.header("Attendance Logs")
    
    teacher_id = st.session_state.teacher_data.get('teacher_id')
    
    records = get_teacher_attendance_logs(teacher_id)
    
    if not records:
        st.info("No attendance logs found.", icon="ℹ️")
        return

    data = []
    
    for r in records:
        ts = r.get('timestamp')
        data.append({
            'ts_group': ts.split(".")[0] if ts else "N/A",
            'time': datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N/A",
            'subject': r['subjects']['name'] if r.get('subjects') else "N/A",
            'subject_code': r['subjects']['subject_code'] if r.get('subjects') else "N/A",
            'ispresent': bool(r.get('ispresent', False))
        })
    
    df = pd.DataFrame(data)
    
    summary =(
        df.groupby(['ts_group', 'time', 'subject', 'subject_code'])
        .agg(
            Present_Count=('ispresent','sum'),
            Total_Count=('ispresent','count')
        ).reset_index()
    ) 
    
    
    summary['Attendance Stats'] = (
        "✅" + summary['Present_Count'].astype(str) + " / " + summary['Total_Count'].astype(str)
    )
    
    display_df = (summary.sort_values(by='ts_group', ascending=False)
                  [['time', 'subject', 'subject_code', 'Attendance Stats']])
    
    st.dataframe(display_df, hide_index=True, width='stretch')
    
