import streamlit as st
import pandas as pd
from urllib.error import URLError

st.set_page_config(page_title="Planning", page_icon="✔")

st.markdown("# Planning")
st.write(
    """
    Here you can check the prioritization suggested and repriorize it as your needed
    """
)

@st.cache_data
def load_data():
    data = pd.read_excel("planejamento.xlsx")
    return data

try:
    df = load_data()
    edited_df = st.data_editor(df, hide_index=True, disabled=['Cliente', 'Oferta', 'Valor', 'Justificativa', 'Venda Acum', 'Prior Sugerida Cliente']) # 👈 An editable dataframe

except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )    
