import streamlit as st

data = st.session_state.app_data

with st.expander("点击查看当前原始 JSON 数据"):
    st.json(data.model_dump_json())
