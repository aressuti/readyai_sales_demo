import streamlit as st
from urllib.error import URLError
from repository.plann import load_data, load_data_ofertas
import datetime
import pandas as pd
import numpy as np

st.set_page_config(page_title="Feedback", page_icon="🧐")

st.markdown("# Feedback")

def reset():
    if 'key' in st.session_state:
        st.session_state.key += 1

try:
    if 'df' not in st.session_state:
        df = load_data()
        st.session_state.df = df
        st.session_state.key = 0

    df = st.session_state.df

    df_ofertas = load_data_ofertas()
    customers = st.selectbox(
        "Choose the customer", list(df['Cliente'].unique())
    )

    st.markdown("## Offers")
    df_offers = df.loc[df['Cliente'] == customers]
    st.dataframe(df_offers['Oferta'], hide_index=True)

    st.markdown("## Feedback")
    d = st.date_input("Visit date: ", format="DD/MM/YYYY", key=f'date_{st.session_state.key}')
    p = st.text_input("Who did you visit?", key=f'name_{st.session_state.key}')

    df_resultado = pd.merge(df_offers, df_ofertas, on='Oferta', how='left')
    df_resultado['Answers'] = None

    edited_df = st.data_editor(df_resultado[['Perguntas', 'Answers']], hide_index=True, disabled=['Perguntas'],
        key=f'editor_{st.session_state.key}')

    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

    with col1:
        if st.button("Save", type="primary"):
            # edited_df.to_excel("planejamento.xlsx", index=False)
            st.dataframe(edited_df)
            del st.session_state['key']
            del st.session_state['df']

    with col2:
        st.button("Cancel", on_click=reset)

except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )        