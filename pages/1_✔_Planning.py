import streamlit as st
import pandas as pd
from urllib.error import URLError

def load_data():
    data = pd.read_excel("planejamento.xlsx")
    return data

def reset():
    if 'key' in st.session_state:
        st.session_state.key += 1

st.set_page_config(page_title="Planning", page_icon="✔")

st.markdown("# Planning")
st.write(
    """
    Here you can check the prioritization suggested and repriorize it as your needed
    """
)

try:
    if 'df' not in st.session_state:
        df = load_data()
        st.session_state.df = df
        st.session_state.key = 0

    df = st.session_state.df

    edited_df = st.data_editor(df, hide_index=True, disabled=['Customer', 'Offer', 'Value', 'Justification', 'Acc Sales', 'Prior. Suggested'],
                               key=f'editor_{st.session_state.key}') # 👈 An editable dataframe

    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

    with col1:
        if st.button("Save", type="primary"):
            edited_df.to_excel("planejamento.xlsx", index=False)
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
