import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Ready - Sales - 1500fh",
    page_icon="🤖",
)

@st.cache_data
def load_data():
    data = pd.read_excel("planejamento.xlsx")
    return data

df = load_data()