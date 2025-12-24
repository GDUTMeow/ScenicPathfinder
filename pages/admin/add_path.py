import streamlit as st

# 从 session_state 获取数据模型实例
data = st.session_state.app_data

if "message" in st.session_state:
    st.toast(st.session_state.message, icon="✔️")
    del st.session_state.message

available_spots = [spot for spot in data.graph.spots if not spot.deleted]
spot_names = [spot.name for spot in available_spots]

if len(spot_names) < 2:
    st.warning("系统中至少需要有两个有效景点才能添加道路")
else:
    st.write("请选择需要连接的两个景点，并提供道路信息")

    col1, col2 = st.columns(2)
    with col1:
        from_spot_name = st.selectbox(
            "起始景点", options=spot_names, key="path_from_spot_name", index=0
        )
    with col2:
        default_index = 1 if len(spot_names) > 1 else 0
        to_spot_name = st.selectbox(
            "目标景点", options=spot_names, key="path_to_spot_name", index=default_index
        )

    distance = st.number_input(
        "道路距离 (米)", min_value=1, step=1, key="path_distance"
    )
    duration = st.number_input(
        "所需时间 (分钟)", min_value=1, step=1, key="path_duration"
    )

    if st.button("确认添加道路"):
        if from_spot_name == to_spot_name:
            st.error("起始景点和目标景点不能是同一个")
        else:
            try:
                from_spot_id = data.graph.find_spot_by_name(from_spot_name).id
                to_spot_id = data.graph.find_spot_by_name(to_spot_name).id

                data.graph.add_path(
                    from_id=from_spot_id,
                    to_id=to_spot_id,
                    distance=distance,
                    duration=duration,
                )

                data.save()

                st.session_state.message = (
                    f"成功添加从 {from_spot_name} 到 {to_spot_name} 的道路！"
                )
                st.rerun()

            except Exception as e:
                st.error(f"添加道路失败: {e}")


st.divider()
st.subheader("当前已存在的道路")

path_exists = False
processed_paths = set()
for spot in data.graph.spots:
    if not spot.deleted:
        for path in spot.paths:
            pair_key = tuple(sorted((spot.id, path.target_id)))
            if pair_key not in processed_paths:
                target_spot = data.graph.spots[path.target_id]
                st.write(
                    f"- **{spot.name}** <-> **{target_spot.name}** (距离: {path.distance}米, 时间: {path.duration}分钟)"
                )
                processed_paths.add(pair_key)
                path_exists = True

if not path_exists:
    st.info("当前系统中还没有任何道路")
