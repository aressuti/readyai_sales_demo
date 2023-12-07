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
        "Choose the customer", list(df['Customer'].unique())
    )

    st.markdown("## Offers")
    df_offers = df.loc[df['Customer'] == customers]
    st.dataframe(df_offers['Offer'], hide_index=True)

    st.markdown("## Feedback")
    d = st.date_input("Visit date: ", format="DD/MM/YYYY", key=f'date_{st.session_state.key}')
    p = st.text_input("Who did you visit?", key=f'name_{st.session_state.key}')

    df_resultado = pd.merge(df_offers, df_ofertas, on='Offer', how='left')
    df_resultado['Answers'] = None

    edited_df = st.data_editor(df_resultado[['Questions', 'Answers']], hide_index=True, disabled=['Questions'],
        key=f'editor_{st.session_state.key}')

    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

    with col1:
        if st.button("Save", type="primary"):
            # Nome do arquivo Excel existente
            arquivo_excel_existente = 'visitas.xlsx'

            # Carregue a planilha existente
            df_existente = pd.read_excel(arquivo_excel_existente)

            dados_visita = {'Customer': [customers], 'Date': [d], 'Contact': [p]}
            df_novos_dados = pd.DataFrame(dados_visita)
            dados_oferta = df_offers[['Customer', 'Offer']]
            df_join_1 = pd.merge(df_novos_dados, dados_oferta, on='Customer', how='left')
            df_join_2 = pd.merge(df_join_1, df_resultado[['Offer', 'Questions']], on='Offer', how='left')
            df_join_3 = pd.merge(df_join_2, edited_df, on='Questions', how='left')

            # Acrescente os novos dados ao DataFrame existente
            df_existente = pd.concat([df_existente, df_join_3], ignore_index=True)

            df_existente.to_excel("visitas.xlsx", index=False)
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