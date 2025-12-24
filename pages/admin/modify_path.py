import streamlit as st

data = st.session_state.app_data

if "message" in st.session_state:
    st.toast(st.session_state.message, icon="✔️")
    del st.session_state.message

if "editing_path_key" not in st.session_state:
    st.session_state.editing_path_key = None

st.header("修改已存在的道路信息")

if st.session_state.editing_path_key:
    try:
        from_spot_name, to_spot_name = st.session_state.editing_path_key.split(" <-> ")
        from_spot = data.graph.find_spot_by_name(from_spot_name)

        current_path = next(
            p
            for p in from_spot.paths
            if p.target_id == data.graph.find_spot_by_name(to_spot_name).id
        )

        st.info(f"正在修改道路: **{from_spot_name}** <-> **{to_spot_name}**")

        new_distance = st.number_input(
            "新的道路距离 (米)", value=current_path.distance, min_value=1, step=1
        )
        new_duration = st.number_input(
            "新的所需时间 (分钟)", value=current_path.duration, min_value=1, step=1
        )

        if st.button("保存修改"):
            try:
                data.graph.modify_path(
                    from_id=from_spot.id,
                    to_id=current_path.target_id,
                    distance=new_distance,
                    duration=new_duration,
                )
                data.save()
                st.session_state.message = (
                    f"道路 {from_spot_name} <-> {to_spot_name} 修改成功！"
                )
                st.session_state.editing_path_key = None
                st.rerun()
            except Exception as e:
                st.error(f"修改道路失败: {e}")

    except (ValueError, StopIteration, Exception) as e:
        st.error(f"加载待编辑道路信息时出错: {e}。将返回选择列表。")
        st.session_state.editing_path_key = None
        st.rerun()

else:
    st.write("请先选择一条需要修改的道路")

    path_options = []
    processed_paths = set()
    for spot in data.graph.spots:
        if not spot.deleted:
            for path in spot.paths:
                pair_key = tuple(sorted((spot.id, path.target_id)))
                if pair_key not in processed_paths:
                    target_spot = data.graph.spots[path.target_id]
                    path_options.append(f"{spot.name} <-> {target_spot.name}")
                    processed_paths.add(pair_key)

    if not path_options:
        st.warning("当前没有可供修改的道路")
    else:
        selected_path = st.selectbox(
            "选择道路", options=path_options, key="path_to_modify"
        )
        if st.button("确认选择并编辑"):
            st.session_state.editing_path_key = selected_path
            st.rerun()
