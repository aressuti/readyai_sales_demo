import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    data = pd.read_excel("planejamento.xlsx")
    return data

@st.cache_data
def load_data_historico():
    data = pd.read_excel("historico.xlsx")
    return data

@st.cache_data
def load_data_ofertas():
    data = pd.read_excel("ofertas.xlsx")
    return data
