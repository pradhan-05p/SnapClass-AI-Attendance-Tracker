import streamlit as st

from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen

from src.components.auto_enroll import auto_enroll_diaglogue

def main():
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    match st.session_state['login_type']:
        case 'Teacher':
            teacher_screen()
        case 'Student':
            student_screen()
        case _:
            home_screen()
    
    join_code = st.query_params.get("join-code")
    if join_code:
        if st.session_state.get('login_type') != 'Student':
            st.session_state.login_type = 'Student'
            st.rerun()
            print(f"DEBUG A: join_code={join_code}, is_logged_in={st.session_state.get('is_logged_in')}, user_role={st.session_state.get('user_role')}")
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
            auto_enroll_diaglogue(join_code)
main()