import streamlit as st

from models.graph import Spot

data = st.session_state.app_data

if "message" in st.session_state:
    st.toast(st.session_state.message, icon="✔️")
    del st.session_state.message

st.write("当前景点信息如下")
for spot in data.graph.spots:
    if not spot.deleted:
        st.write(f"- 名称: {spot.name} \n   - 简介: {spot.description}")

st.text_input("景点名称", key="spot_name")
st.text_input("景点简介", key="spot_description")

if st.button("添加景点"):
    spot = Spot(
        id=len(data.graph.spots),
        name=st.session_state.spot_name,
        description=st.session_state.spot_description,
        deleted=False,
    )
    try:
        data.graph.add_node(spot=spot)
        data.save()
        st.session_state.message = f"景点 {spot.name} 添加成功！"
        st.rerun()
    except Exception as e:
        st.error(f"添加景点失败: {e}")
