import time

import streamlit as st
from src.components.header import header_dashboard
from src.ui.base_layout import style_base_layout, style_background_dashboard
from src.components.footer import footer_home_dashboard

from src.database.db import check_teacher_exists, create_teacher, teacher_login

from src.screens.teacher_access import teacher_tab_take_attendance, teacher_tab_manage_attendance, teacher_tab_attendance_logs

def teacher_screen():
    style_background_dashboard()
    style_base_layout()
    
    if 'teacher_data' in st.session_state:
        teacher_dashboard_after_login()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=='login':
        teacher_screen_login()
    elif st.session_state.teacher_login_type=='register':
        teacher_screen_register()


def dashboard_teacher():
    c1, c2 = st.columns(2, gap="xxlarge",vertical_alignment="center")
    with c1:
        header_dashboard()
    
    with c2:
        if st.button("Back to Home", type="secondary", key="loginBackHome", icon=":material/arrow_back:", icon_position="right"):
            st.session_state['login_type'] = None
            st.rerun() 



def teacher_dashboard_after_login():
    teacher = st.session_state.teacher_data
    c1, c2 = st.columns(2, gap="xxlarge",vertical_alignment="center")
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"Welcome, {teacher['name']}!")
        if st.button("LogOut", type="secondary", icon=":material/arrow_back:", icon_position="right"):
            st.session_state.is_logged_in = False
            del st.session_state['teacher_data']
            st.rerun() 
            
        st.space()

    if 'current_teacher_tab' not in st.session_state:
        st.session_state.current_teacher_tab = 'Take Attendance'
    st.divider()
    tab1,tab2,tab3 = st.columns(3,gap="small")
        
    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'Take Attendance' else "tertiary"
        if st.button("Take Attendance", type=type1, width="stretch", icon=":material/ar_on_you:", icon_position="right"):
            st.session_state.current_teacher_tab = 'Take Attendance'
            st.rerun()
    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == 'Manage Attendance' else "tertiary"
        if st.button("Manage Attendance", type=type2, width="stretch", icon=":material/book_ribbon:", icon_position="right"):
            st.session_state.current_teacher_tab = 'Manage Attendance'
            st.rerun()
    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == 'Attendance Logs' else "tertiary"
        if st.button("Attendance Logs", type=type3, width="stretch", icon=":material/cards_stack:", icon_position="right"):
            st.session_state.current_teacher_tab = 'Attendance Logs'
            st.rerun()
            

    if st.session_state.current_teacher_tab == 'Take Attendance':
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == 'Manage Attendance':
        teacher_tab_manage_attendance()
    if st.session_state.current_teacher_tab == 'Attendance Logs':
        teacher_tab_attendance_logs()
    
    
        
    
    footer_home_dashboard()
    



def login_teacher(teacher_user_name, teacher_password):
    if not teacher_user_name or not teacher_password:
        return False
    teacher = teacher_login(teacher_user_name, teacher_password)
    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    return False

def teacher_screen_login():
    dashboard_teacher()
    st.space()
    st.header("Login Using password",text_alignment="center")
    st.space()
    teacher_user_name = st.text_input("Enter Your Username : ", placeholder="Hello! please enter your username")
    teacher_password = st.text_input("Enter Your Password : ", placeholder="please enter a password", type="password")
    st.divider()
    
    btn1, btn2 = st.columns(2)
    with btn1:
        if st.button("Login", type="secondary", key="loginTeacher",width="stretch" ,icon=":material/passkey:", icon_position="right",shortcut="enter"):
            if login_teacher(teacher_user_name, teacher_password):
                st.toast("Welcome back, " + teacher_user_name + "!", icon=":material/check_circle:")
                time.sleep(2)
                st.rerun()
            else:
                st.error("Invalid username or password. Please try again.", icon=":material/error:")
    with btn2:
        if st.button("Register Instead", type="primary", key="registerTeacher",width="stretch" ,icon=":material/person_add:", icon_position="right"):
            st.session_state.teacher_login_type = 'register'
            st.rerun()
    footer_home_dashboard()




def register_teacher(teacher_user_name, teacher_name, teacher_password, teacher_confirm_password):
    if not teacher_user_name or not teacher_name or not teacher_password or not teacher_confirm_password:
        return False, "Please fill in all the fields. Required!!!"
    if check_teacher_exists(teacher_user_name):
        return False, "Username already exists. Please choose a different username."
    if teacher_password != teacher_confirm_password:
        return False, "Passwords do not match. Please try again."
    try:
        create_teacher(teacher_user_name, teacher_password, teacher_name)
        return True, "Teacher profile created successfully! You can now log in."
    except Exception as e:
        return False, f"{str(e)} An error occurred while creating the teacher profile. Please try again."


def teacher_screen_register():
    dashboard_teacher() 
    st.header("Register Your Teacher Profile",text_alignment="center")
    
    st.space()
    teacher_user_name = st.text_input("Enter Your User Name : ", placeholder="username")
    teacher_name = st.text_input("Enter Your Name : ", placeholder="Hello! please enter your name")
    teacher_password = st.text_input("Enter Your Password : ", placeholder="please enter a password", type="password")
    teacher_confirm_password = st.text_input("Confirm Your Password : ", placeholder="please confirm your password", type="password")
    st.divider()
    
    btn1, btn2 = st.columns(2)
    with btn1:
        if st.button("Register", type="secondary",width="stretch" ,icon=":material/person_add:", icon_position="right",shortcut="enter"):
            success,message = register_teacher(teacher_user_name, teacher_name, teacher_password, teacher_confirm_password)
            if success:
                st.success(message, icon=":material/check_circle:")
                time.sleep(2)
                st.session_state.teacher_login_type = 'login'
                st.rerun()
            else:
                st.error(message, icon=":material/error:")
    with btn2:
       if st.button("Login Instead", type="primary",width="stretch" ,icon=":material/passkey:", icon_position="right"):
            st.session_state.teacher_login_type = 'login'
            st.rerun()
    
    footer_home_dashboard()

    
    