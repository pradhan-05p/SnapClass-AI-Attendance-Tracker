#  Under Maintenance: The delete profile feature is temporarily disabled for students due to potential issues with data integrity and user experience. We are working on a more robust solution to ensure that profile deletion is handled safely and effectively.

# import streamlit as st
# import time
# from src.database.db import delete_student

# @st.dialog(title="Confirm Delete Profile", width="medium")
# def confirm_delete_profile_student():
#     st.divider()
#     st.warning("Are you sure you want to delete your profile? This action cannot be undone.", icon="⚠️")
#     col1, col2 = st.columns(2, gap="large")
#     with col1:
#         if st.button("Cancel", type="secondary", icon=":material/cancel:", icon_position="right"):
#             st.toast("Profile deletion canceled.", icon="ℹ️")
#             st.rerun()
#     with col2:
#         if st.button("Delete Profile", type="primary", icon=":material/delete:", icon_position="right"):
#             student_id = st.session_state.get('student_data', {}).get('student_id')
#             if student_id:
#                 delete_student(student_id)
#                 time.sleep(1)
#                 st.toast("Your profile has been deleted successfully.", icon="✅")
#                 st.session_state.is_logged_in = False
#                 del st.session_state['student_data']
#                 st.cache_data.clear()
#                 st.cache_resource.clear()
#                 st.rerun()
#             else:
#                 st.error("Error: Student ID not found. Unable to delete profile.", icon="❌")