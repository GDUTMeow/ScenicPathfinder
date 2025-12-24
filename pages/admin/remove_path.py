# pages/admin_delete_path.py

import streamlit as st

data = st.session_state.app_data

if "message" in st.session_state:
    st.toast(st.session_state.message, icon="✔️")
    del st.session_state.message

path_options = []
processed_paths = set()
for spot in data.graph.spots:
    if not spot.deleted:
        for path in spot.paths:
            pair_key = tuple(sorted((spot.id, path.target_id)))
            if pair_key not in processed_paths:
                target_spot = data.graph.spots[path.target_id]
                # 创建一个用户友好的显示名称
                path_options.append(f"{spot.name} <-> {target_spot.name}")
                processed_paths.add(pair_key)

if not path_options:
    st.warning("当前系统中没有可供删除的道路")
else:
    st.write("请从下方选择希望永久删除的道路")

    path_to_delete_str = st.selectbox(
        "选择要删除的道路", options=path_options, key="path_to_delete"
    )

    if st.button("确认删除道路", type="primary"):
        try:
            from_spot_name, to_spot_name = path_to_delete_str.split(" <-> ")

            from_id = data.graph.find_spot_by_name(from_spot_name).id
            to_id = data.graph.find_spot_by_name(to_spot_name).id

            data.graph.delete_path(from_id, to_id)
            data.save()

            st.session_state.message = f"道路 {path_to_delete_str} 已成功删除！"
            st.rerun()

        except Exception as e:
            st.error(f"删除道路失败: {e}")
