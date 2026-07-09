import streamlit as st

def footer_home():
    st.markdown(
        """
        <p style="text-align:center;color:white; margin-top: 50px; font-size: 1.2rem; item-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; font-weight: 400;">
            Created with ❤️ by Prateek
        </p>
        """,
        unsafe_allow_html=True,
    )