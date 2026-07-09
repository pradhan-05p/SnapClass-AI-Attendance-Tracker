import streamlit as st

def header_home():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"

    st.markdown(
        f"""
        <div style="text-align:center; margin-bottom: 50px; margin-top: 1px; display: flex; flex-direction: column; align-items: center; justify-content: center;">
            <img src="{logo_url}" style="height:100px;">
            <h2 style="color: #B5BACA; height: 60px;"> SNAP<br/>CLASS</h2>
        </div>
        """,
        unsafe_allow_html=True
    )