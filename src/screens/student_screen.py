import time

import streamlit as st
from src.components.header import header_dashboard
from src.ui.base_layout import style_base_layout, style_background_dashboard
from src.components.footer import footer_home_dashboard

from src.pipelines.face_pipeline import get_face_embedding, get_trained_model,predict_attendance,train_model
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students,create_student

from PIL import Image
import numpy as np

def student_dashboard_after_login():
    student = st.session_state.student_data
    st.header(f"Welcome, {student['name']}!", text_alignment="center")



def student_screen():
    style_background_dashboard()
    style_base_layout()
    
    if 'student_data' in st.session_state:
        student_dashboard_after_login()
        return
    
    c1, c2 = st.columns(2, gap="xxlarge",vertical_alignment="center")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Back to Home", type="secondary", key="loginBackHome", icon=":material/arrow_back:", icon_position="right"):
            st.session_state['login_type'] = None
            st.rerun() 
    st.space()
    
    show_registeration = False
    
    st.header("Login using FaceID",text_alignment="center")
    photo_sorce = st.camera_input("Position your face in front of the camera and click on the button below to login")
    if photo_sorce:
        img = np.array(Image.open(photo_sorce))
        with st.spinner("Verifying your face..."):
            detected,all_ids,num_faces = predict_attendance(img)
            if num_faces == 0:
                st.warning("No face detected")
            elif num_faces > 1:
                st.warning("Multiple faces detected")
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s.get("student_id") == student_id), None)
                    if student:
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.session_state.is_logged_in = True
                        st.toast(f"Welcome Back, {student['name']}!")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info("Face not recognized. Might be a new student!!!")
                    show_registeration = True
                    
                    
    if show_registeration:
        with st.container(border=True):
            st.header("Register New Profile",text_alignment="center")
            new_name = st.text_input("Enter Your Name : ", placeholder="e.g Prateek Pradhan")
            st.subheader("optional: Voice enrollment")
            st.info("Enroll your voice to enable voice-based login in the future. This step is optional but recommended for enhanced security and convenience.")
            audio_data = None
            try:
                audio_data = st.audio_input("Record a short phrase : E.g : hello, I am prateek,I am present")
            except Exception as e:
                st.error(f"Error voice enrollment failed: {e}")
                
            if st.button("Create Account", type="primary", icon=":material/add_circle:", icon_position="right"):
                if new_name:
                    with st.spinner("Creating your account..."):
                        img = np.array(Image.open(photo_sorce))
                        encodings = get_face_embedding(img)
                        if encodings:
                            face_emb = encodings[0].tolist() 
                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())
                                if voice_emb is None:
                                    st.warning("Voice enrollment failed. Continuing without voice.")
                                    print("Face length:", len(face_emb))
                                    print("Voice:", voice_emb is None)

                            if voice_emb:
                                print("Voice length:", len(voice_emb))
                            response_data = create_student(name=new_name, face_embeddings=face_emb, voice_embeddings=voice_emb)
                            
                            if response_data:
                                train_model()  # Retrain the model with the new student data
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.session_state.is_logged_in = True
                                st.toast(f"Welcome, {new_name}! Your account has been created successfully.")
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error("Face encoding failed. Please try again.")
                else:
                    st.warning("Please enter your name to create an account.")
    st.divider()
    footer_home_dashboard()