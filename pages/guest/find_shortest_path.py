import streamlit as st
from exceptions import SpotIdInvalidError
from models.graph import Spot

data = st.session_state.app_data

st.header("最短路径查询")
st.info("查询任意两个景点之间的最短路径，可以选择以距离或时间为权重")

available_spots = [spot for spot in data.graph.spots if not spot.deleted]
spot_names = [spot.name for spot in available_spots]

if len(spot_names) < 2:
    st.warning("系统中至少需要两个有效景点且有连接道路才能进行最短路径查询")
else:
    col1, col2 = st.columns(2)
    with col1:
        start_spot_name = st.selectbox(
            "选择起始景点", options=spot_names, key="shortest_path_start_spot"
        )
    with col2:
        default_target_index = 0
        if len(spot_names) > 1 and spot_names[0] == start_spot_name:
            default_target_index = 1
        elif len(spot_names) > 1 and spot_names[0] != start_spot_name:
            default_target_index = (
                0
            )

        target_spot_name = st.selectbox(
            "选择目标景点",
            options=spot_names,
            key="shortest_path_target_spot",
            index=(
                default_target_index if default_target_index < len(spot_names) else 0
            ),
        )

    weight_type_display = st.radio(
        "选择权重类型", options=["距离", "时间"], key="shortest_path_weight_type"
    )

    weight_type_model = "distance" if weight_type_display == "距离" else "duration"

    if st.button("查询最短路径"):
        if start_spot_name == target_spot_name:
            st.warning("起始景点和目标景点不能相同。")
        else:
            try:
                start_id = data.graph.find_spot_by_name(start_spot_name).id
                target_id = data.graph.find_spot_by_name(target_spot_name).id

                total_weight, path_ids = data.graph.dijkstra(
                    start_id, target_id, weight_type_model
                )

                st.subheader("查询结果")
                if total_weight == -1:
                    st.error(
                        f"从 **{start_spot_name}** 到 **{target_spot_name}** 的路径不可达"
                    )
                else:
                    st.success(
                        f"找到了从 **{start_spot_name}** 到 **{target_spot_name}** 的最短路径！"
                    )

                    path_names = [
                        data.graph.spots[spot_id].name for spot_id in path_ids
                    ]

                    with st.container(border=True):
                        st.markdown(f"**总{weight_type_display}:** ")
                        if weight_type_model == "distance":
                            st.metric(label="", value=f"{total_weight} 米")
                        else:
                            st.metric(label="", value=f"{total_weight} 分钟")

                        st.markdown("**路径详情:**")
                        st.write(" -> ".join(path_names))

                        with st.expander("查看分段路径信息"):
                            for i in range(len(path_ids) - 1):
                                current_id = path_ids[i]
                                next_id = path_ids[i + 1]

                                current_spot = data.graph.spots[current_id]
                                next_spot = data.graph.spots[next_id]

                                # 找到当前景点到下一个景点的路径详细信息
                                segment_path = next(
                                    p
                                    for p in current_spot.paths
                                    if p.target_id == next_id
                                )
                                st.markdown(
                                    f"- 从 **{current_spot.name}** 到 **{next_spot.name}**:"
                                )
                                st.write(
                                    f"  距离: {segment_path.distance} 米, 时间: {segment_path.duration} 分钟"
                                )

            except SpotIdInvalidError:
                st.error("所选景点ID无效，可能已被删除。")
            except Exception as e:
                st.error(f"查询最短路径失败: {e}")
