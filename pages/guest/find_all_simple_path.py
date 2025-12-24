import streamlit as st
from exceptions import SpotIdInvalidError
from models.graph import Spot

data = st.session_state.app_data

st.header("所有简单路径查询")
st.info("查询任意两个景点之间的所有不重复的简单路径")

available_spots = [spot for spot in data.graph.spots if not spot.deleted]
spot_names = [spot.name for spot in available_spots]

if len(spot_names) < 2:
    st.warning("系统中至少需要两个有效景点才能进行所有路径查询。")
else:
    col1, col2 = st.columns(2)
    with col1:
        start_spot_name = st.selectbox(
            "选择起始景点", options=spot_names, key="all_paths_start_spot"
        )
    with col2:
        default_target_index = 0
        if len(spot_names) > 1 and spot_names[0] == start_spot_name:
            default_target_index = 1

        target_spot_name = st.selectbox(
            "选择目标景点",
            options=spot_names,
            key="all_paths_target_spot",
            index=default_target_index if default_target_index < len(spot_names) else 0,
        )

    if st.button("查询所有路径"):
        if start_spot_name == target_spot_name:
            st.warning("起始景点和目标景点不能相同。")
        else:
            try:
                start_id = data.graph.find_spot_by_name(start_spot_name).id
                target_id = data.graph.find_spot_by_name(target_spot_name).id

                all_paths_results = data.graph.find_all_paths(start_id, target_id)

                st.subheader("查询结果")
                if not all_paths_results:
                    st.info(
                        f"从 **{start_spot_name}** 到 **{target_spot_name}** 没有找到任何简单路径。"
                    )
                else:
                    st.success(
                        f"找到了 {len(all_paths_results)} 条从 **{start_spot_name}** 到 **{target_spot_name}** 的简单路径。"
                    )

                    # 按总距离排序路径，以便于查看
                    sorted_paths = sorted(all_paths_results, key=lambda x: x[0])

                    for i, (total_dist, total_duration, path_ids) in enumerate(
                        sorted_paths
                    ):
                        with st.container(border=True):
                            st.markdown(f"#### 路径 {i+1}")
                            path_names = [
                                data.graph.spots[spot_id].name for spot_id in path_ids
                            ]
                            st.write(f"**路径:** {' -> '.join(path_names)}")
                            col1, col2 = st.columns(2)
                            col1.metric("总距离", f"{total_dist} 米")
                            col2.metric("总时间", f"{total_duration} 分钟")

            except SpotIdInvalidError:
                st.error("所选景点ID无效，可能已被删除。")
            except Exception as e:
                st.error(f"查询所有路径失败: {e}")
