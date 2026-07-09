import streamlit as st

def style_background_home():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #655ADA !important;
        }
        
        .stApp div[data-testid="stColumn"] {
            background-color: #90B9FB !important;
            padding: 2.5rem !important;
            border-radius: 5rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def style_background_dashboard():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #D391FA !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def style_base_layout():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

        /* Hide toolbar and footer */
        #MainMenu,footer,header {
            visibility: hidden;
            }

        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 0rem !important;
            }
        
        h2,h1{
            font-family: "Climate Crisis", sans-serif !important;
            font-size: 2rem !important;
            line-height: 2.2rem !important;
            margin-bottom: 1rem !important;
            margin: 1rem 0 !important;
           /* color: #E0E3FF !important; */
            }

        html, body, .stApp {
            font-family: "Outfit", sans-serif !important;
            }

        button[kind="primary"]{
            background-color: #190087 !important;
            color: #E0E3FF !important;
            border: none !important;
            border-radius: 1.5rem !important;
            color: white !important;
            padding: 10px 20px !important;
            transition: transform 0.3s ease-in-out !important;
        }
        button[kind="secondary"]{
            background-color: #DA2C9E !important;
            color: #E0E3FF !important;
            border: none !important;
            border-radius: 1.5rem !important;
            color: white !important;
            padding: 10px 20px !important;
            transition: transform 0.3s ease-in-out !important;
        }
        button[kind="tertiary"]{
            background-color: black !important;
            color: #E0E3FF !important;
            border: none !important;
            border-radius: 1.5rem !important;
            color: white !important;
            padding: 10px 20px !important;
            transition: transform 0.3s ease-in-out !important;
        }

        button:hover {
            transform: scale(1.1) !important;
            }
        
        </style>
        """,
        unsafe_allow_html=True
    )