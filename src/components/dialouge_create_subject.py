import streamlit as st
from src.database.db import create_subject

@st.dialog(title="Create New Subject")
def create_dialouge_subject(teacher_id):
    st.write("Please enter the details for the new subject.")
    sub_id = st.text_input("Subject Code",placeholder="CS1001")
    sub_name = st.text_input("Subject Name",placeholder="OPERATING SYSTEMS")
    sub_section = st.text_input("Subject Section",placeholder="CS02")
    
    if st.button("Create Subject Now", type="primary",width="stretch"):
        if sub_id and sub_name and sub_section:
            try: 
                response = create_subject(sub_id, sub_name, sub_section, teacher_id)
            except Exception as e:
                st.toast(f"Error occurred while creating subject: {e}", icon="❌")
                st.error(f"Error occurred while creating subject: {str(e)}")
            if response:
                st.toast(f"Subject {sub_name} created successfully!", icon="✅")
                st.session_state['subject_created'] = True
            else:
                st.toast("Failed to create subject. Please try again.", icon="❌")
        else:
            st.warning("Please fill in all the fields.", icon="⚠️")
