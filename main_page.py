import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIG/SETUP ---

st.set_page_config("main_page.py", ":chart:", "wide")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --------------------

# --- DATA ---

st.sidebar.header("Filter Here...")

filter_param0 = st.sidebar.selectbox(
    "Select Box...",
    options=["Option 0", "Option 1"]
)

# ------------

# --- FUNCTIONS ---
# -----------------

# --- PAGE CONTENT ---
# --------------------