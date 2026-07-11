import streamlit as st

def header_home():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"

    st.markdown(
        f"""
        <div style="text-align:center; margin-bottom: 50px; margin-top: 1px; display: flex; flex-direction: column; align-items: center; justify-content: center;">
            <img src="{logo_url}" style="height:100px;">
            <h2 style="color: #B5BACA; height: 60px;">SNAP<br/>&nbsp;CLASS</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
    
def header_dashboard():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"

    st.markdown(
        f"""
        <div style="text-align:left; display: flex; align-items: center; justify-content: center; gap: 10px;padding-top: 10px; margin-top: 1px;">
            <img src="{logo_url}" style="height:100px; margin-top: 10px;">
            <h2 style="color: #5865F2; height:90px; margin-top: 10px; padding-top: 10px; gap: 10px;">SNAP<br/>CLASS</h2>
        </div>
        """,
        unsafe_allow_html=True
    )