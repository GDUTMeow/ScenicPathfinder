import streamlit as st

data = st.session_state.app_data

if "message" in st.session_state:
    st.toast(st.session_state.message, icon="✔️")
    del st.session_state.message

st.selectbox(
    "选择要删除的景点",
    options=[spot.name for spot in data.graph.spots if not spot.deleted],
    key="spot_name",
)
if st.button("删除景点"):
    spot_name = st.session_state.spot_name
    try:
        # 找到名称对应的节点
        spot_to_delete = next(
            spot
            for spot in data.graph.spots
            if spot.name == spot_name and not spot.deleted
        )

        data.graph.delete_node(spot_to_delete.id)
        data.save()

        st.session_state.message = f"景点 {spot_name} 删除成功！"
        st.rerun()

    except StopIteration:
        st.error(
            f"操作失败：未找到名为 '{spot_name}' 的景点，可能已被删除。请刷新页面重试。"
        )
    except Exception as e:
        st.error(f"删除景点失败: {e}")
