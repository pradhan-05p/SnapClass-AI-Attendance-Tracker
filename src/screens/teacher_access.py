import streamlit as st
from src.components.header import header_dashboard
from src.ui.base_layout import style_base_layout, style_background_dashboard
from src.components.footer import footer_home_dashboard
from src.components.dialouge_create_subject import create_dialouge_subject
from src.components.subject_card import subject_card
from src.components.share_dialouge_qr import share_sub_dialogue


from src.database.db import get_teacher_subjects
def teacher_tab_take_attendance():
    st.subheader("Take Attendance")
    st.write("This is the Take Attendance tab. Here you can take attendance for your classes.")
    # Add your code for taking attendance here


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
    st.subheader("Attendance Logs")
    st.write("This is the Attendance Logs tab. Here you can view attendance logs.")
    # Add your code for viewing attendance logs here
 