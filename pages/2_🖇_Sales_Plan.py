import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError
from repository.plann import load_data, load_data_historico, load_data_ofertas

st.set_page_config(page_title="Sales Plan", page_icon="🖇")

st.markdown("# Sales Plan")

try:
    df = load_data()
    df_hist = load_data_historico()
    df_hist['mes'] = df_hist['data'].dt.month
    df_ofertas = load_data_ofertas()

    customers = st.selectbox(
        "Choose the customer", list(df['Cliente'].unique())
    )

    data = df_hist.loc[df_hist['Cliente'] == customers]
    resultado_agrupado = data.groupby(['Cliente', 'mes'])['Valor'].sum().reset_index()   
    df_transposto = resultado_agrupado.pivot(index='Cliente', columns='mes', values='Valor')
    st.dataframe(df_transposto, hide_index=True)

    # # chart = st.line_chart(resultado_agrupado, x="mes", y="Valor")
    #     chart = (
    #         alt.Chart(resultado_agrupado)
    #         .mark_area(opacity=0.3)
    #         .encode(
    #             x="month:T",
    #             y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
    #             color="Region:N",
    #         )
    #     )
    #     st.altair_chart(chart, use_container_width=True)

    st.markdown("## Offers")
    df_offers = df.loc[df['Cliente'] == customers]
    df_resultado = pd.merge(df_offers, df_ofertas, on='Oferta', how='left')
    st.dataframe(df_resultado[['Oferta', 'Valor', 'Justificativa', 'Argumentacao']], hide_index=True)

    st.markdown("## Information to Collect")
    st.dataframe(df_resultado[['Perguntas']], hide_index=True)

except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )    