import time

import streamlit as st
from src.components.header import header_dashboard
from src.ui.base_layout import style_base_layout, style_background_dashboard
from src.components.footer import footer_home_dashboard

def student_screen():
    style_background_dashboard()
    style_base_layout()
    
    c1, c2 = st.columns(2, gap="xxlarge",vertical_alignment="center")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Back to Home", type="secondary", key="loginBackHome", icon=":material/arrow_back:", icon_position="right"):
            st.session_state['login_type'] = None
            st.rerun() 
    st.space()
    st.header("Login using FaceID",text_alignment="center")
    st.camera_input("Position your face in front of the camera and click on the button below to login")
    
    st.divider()
    footer_home_dashboard()