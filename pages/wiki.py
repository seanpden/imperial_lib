import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from bs4 import BeautifulSoup

# --- CONFIG/SETUP ---

st.set_page_config("main_page.py", ":chart:", "wide")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("List of all TES books...")

# --------------------

# --- DATA ---

st.sidebar.header("Filter Here...")

filter_param0 = st.sidebar.selectbox(
    "Select Box...",
    options=["uesp", "wiki", "lib"]
)

if filter_param0 == "uesp":
    # eso_books = ""
    # eso_books_df = pd.read_html(eso_books)
    # eso_books_df = pd.concat(eso_books_df[0:len(eso_books_df)])

    skyrim_books = "https://en.uesp.net/wiki/Skyrim:Books"
    skyrim_books_df = pd.read_html(skyrim_books)
    skyrim_books_df = pd.concat(skyrim_books_df[1:len(skyrim_books_df)])
    skyrim_books_df.drop(columns=['Unnamed: 0', 'Unnamed: 2'], inplace=True)
    # st.write(skyrim_books_df.columns)

    oblivion_books = "https://en.uesp.net/wiki/Oblivion:Books"
    oblivion_books_df = pd.read_html(oblivion_books)
    for i in range(len(oblivion_books_df)):
        oblivion_books_df[i].rename(columns={"Book Name (ID)": "Title (ID)"}, inplace=True)
        oblivion_books_df[i].rename(columns={"Book Name (ID)": "Title (ID)"}, inplace=True)
        oblivion_books_df[i].rename(columns={"Book Title (ID)": "Title (ID)"}, inplace=True)
        oblivion_books_df[i].rename(columns={"Where this book can be found": "Where to find"}, inplace=True)
    oblivion_books_df = pd.concat(oblivion_books_df[0:len(oblivion_books_df)])
    oblivion_books_df.drop(columns=['Unnamed: 0', 'Unnamed: 2'], inplace=True)

    morrowind_books = "https://en.uesp.net/wiki/Morrowind:Books"
    morrowind_books_df = pd.read_html(morrowind_books)
    morrowind_books_df = pd.concat(morrowind_books_df[0:len(morrowind_books_df)])
    morrowind_books_df.drop(columns=['Unnamed: 0', 'Unnamed: 2'], inplace=True)

    daggerfall_books = "https://en.uesp.net/wiki/Daggerfall:Books"
    daggerfall_books_df = pd.read_html(daggerfall_books)
    daggerfall_books_df = pd.concat(daggerfall_books_df[0:len(daggerfall_books_df)])
    daggerfall_books_df.rename(columns={"Title": "Title (ID)"}, inplace=True)

    all_books = pd.concat([skyrim_books_df, oblivion_books_df, morrowind_books_df, daggerfall_books_df]).drop(columns=["Type", "Skill", "Where to find", "Marker"]).drop_duplicates(subset="Description")
    st.write(all_books.count())
    st.write(len(all_books))

elif filter_param0 == "wiki":
    # eso_books = ""
    # eso_books_df = pd.read_html(eso_books)
    # eso_books_df = pd.concat(eso_books_df[0:len(eso_books_df)])

    skyrim_books = "https://elderscrolls.fandom.com/wiki/Books_(Skyrim)"
    skyrim_books_df = pd.read_html(skyrim_books)
    skyrim_books_df = pd.concat(skyrim_books_df[0:len(skyrim_books_df)])

    oblivion_books = "https://elderscrolls.fandom.com/wiki/Books_(Oblivion)"
    oblivion_books_df = pd.read_html(oblivion_books)
    oblivion_books_df = pd.concat(oblivion_books_df[0:len(oblivion_books_df)])

    morrowind_books = "https://elderscrolls.fandom.com/wiki/Books_(Morrowind)"
    morrowind_books_df = pd.read_html(morrowind_books)
    morrowind_books_df = pd.concat(morrowind_books_df[0:len(morrowind_books_df)])

    daggerfall_books = "https://elderscrolls.fandom.com/wiki/Books_(Daggerfall)"
    daggerfall_books_df = pd.read_html(daggerfall_books)
    daggerfall_books_df = pd.concat(daggerfall_books_df[0:len(daggerfall_books_df)])

    all_books = pd.concat([skyrim_books_df, oblivion_books_df, morrowind_books_df, daggerfall_books_df])
elif filter_param0 == "lib":
    all_books = pd.read_csv("data/imperial_library_books.csv").drop(columns="Unnamed: 0")

# ------------

# --- FUNCTIONS ---
# -----------------

# --- PAGE CONTENT ---

st.subheader("All Books:")
st.dataframe(all_books)