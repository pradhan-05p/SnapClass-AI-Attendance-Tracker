import streamlit as st
from src.database.db import create_subject
import time
from src.database.config import supabase
from src.database.db import enroll_student_to_subject
from PIL import Image  

@st.dialog(title="Capture/ Upload Photos")
def add_photos_dialogue():
    st.write("Please capture or upload photos for the subject.")
    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = 'camera'
        
    t1,t2 = st.columns(2)
    with t1:
        type_camera = 'primary' if st.session_state.photo_tab == 'camera' else 'tertiary'
        if st.button("Camera", type=type_camera,width='stretch'):
            st.session_state.photo_tab = 'camera'
    
    with t2:
        type_upload = 'primary' if st.session_state.photo_tab == 'upload' else 'tertiary'
        if st.button("Upload photos", type=type_upload,width='stretch'):
            st.session_state.photo_tab = 'upload'
            
    if st.session_state.photo_tab == 'camera':
        camera_photo= st.camera_input("Take Snapshots of the classroom",key="camera_dialouge")
        if camera_photo:
            st.session_state.attendance_image.append(Image.open(camera_photo))
            st.toast("Photo Captured successfully!", icon="✅")
            st.rerun()
            
    if st.session_state.photo_tab == 'upload':
        uploaded_photos = st.file_uploader("Upload photos", type=["jpg", "jpeg", "png"], accept_multiple_files=True,key="upload_dialouge")
        if "processed_file_ids" not in st.session_state:
            st.session_state.processed_file_ids = set()

        if uploaded_photos:
            for photo in uploaded_photos:
                if photo not in st.session_state.processed_file_ids:
                    st.session_state.attendance_image.append(Image.open(photo))
                    st.session_state.processed_file_ids.add(photo)

            st.toast(f"{len(uploaded_photos)} photo(s) uploaded successfully!", icon="✅")
    st.divider()
    if st.button("Done", type="primary",width='stretch'):
        st.rerun()
            