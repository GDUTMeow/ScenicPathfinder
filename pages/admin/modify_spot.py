import streamlit as st

from models.graph import Spot

data = st.session_state.app_data

if "message" in st.session_state:
    st.toast(st.session_state.message, icon="✔️")
    del st.session_state.message

st.selectbox(
    "选择需要修改的景点",
    options=[spot.name for spot in data.graph.spots if not spot.deleted],
    key="spot_name",
)

if st.button("确认选择"):
    st.session_state.selected_spot_to_modify = True
    st.rerun()

if (
    hasattr(st.session_state, "selected_spot_to_modify")
    and st.session_state.selected_spot_to_modify
):
    spot_to_modify: Spot = next(
        spot
        for spot in data.graph.spots
        if spot.name == st.session_state.spot_name and not spot.deleted
    )
    st.text_input("景点名称", value=spot_to_modify.name, key="new_spot_name")
    st.text_input(
        "景点简介", value=spot_to_modify.description, key="new_spot_description"
    )
    if st.button("保存"):
        try:
            data.graph.modify_node(
                target_id=spot_to_modify.id,
                name=st.session_state.new_spot_name,
                description=st.session_state.new_spot_description,
            )
            data.save()
            st.session_state.message = f"景点 {spot_to_modify.name} 修改成功！"
            st.session_state.selected_spot_to_modify = False
            st.rerun()
        except Exception as e:
            st.error(f"修改景点失败: {e}")
