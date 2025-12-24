import streamlit as st
from models.graph import Spot

data = st.session_state.app_data

st.header("景点信息查询")

if "queried_spot_name" not in st.session_state:
    st.session_state.queried_spot_name = None

if st.session_state.queried_spot_name:
    try:
        spot_info: Spot = data.graph.find_spot_by_name(
            st.session_state.queried_spot_name
        )

        st.subheader(f"📍 {spot_info.name}")

        st.markdown(f"{spot_info.description}")

        st.divider()

        st.subheader("🚶 从这里出发，您可以前往...")

        if not spot_info.paths:
            st.info("这个景点目前没有连接任何道路。")
        else:
            for path in spot_info.paths:
                if data.graph._is_valid_node(path.target_id):
                    target_spot = data.graph.spots[path.target_id]

                    with st.container(border=True):
                        st.markdown(f"#### 前往: **{target_spot.name}**")
                        col1, col2 = st.columns(2)
                        col1.metric(label="📏 道路距离", value=f"{path.distance} 米")
                        col2.metric(label="⏱️ 预计时间", value=f"{path.duration} 分钟")

        if st.button("返回查询其他景点"):
            st.session_state.queried_spot_name = None
            st.rerun()

    except Exception as e:
        st.error(f"查询时发生错误: {e}")
        # 如果出错，重置状态以避免卡在错误页面
        st.session_state.queried_spot_name = None
        st.rerun()

else:
    available_spots = [spot.name for spot in data.graph.spots if not spot.deleted]

    if available_spots:
        st.info("请从下面的列表中选择一个您感兴趣的景点进行查询。")

        st.selectbox(
            "选择要查询的景点",
            options=available_spots,
            key="spot_name_to_query",
        )

        if st.button("查询"):
            st.session_state.queried_spot_name = st.session_state.spot_name_to_query
            st.rerun()
    else:
        st.error("系统内目前不存在任何景点，请联系景区管理员！")
