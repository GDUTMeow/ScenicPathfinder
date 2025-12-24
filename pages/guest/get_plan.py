import streamlit as st
from exceptions import SpotIdInvalidError, StandardInvalidError
from models.graph import Spot

data = st.session_state.app_data

st.header("游览路线规划")
st.info("规划一条包含指定必经景点的游览路线")

available_spots = [spot for spot in data.graph.spots if not spot.deleted]
spot_names = [spot.name for spot in available_spots]

if len(spot_names) < 2:
    st.warning("系统中至少需要两个有效景点才能进行路线规划。")
else:
    col1, col2 = st.columns(2)
    with col1:
        start_spot_name = st.selectbox(
            "选择起始景点", options=spot_names, key="tsp_start_spot"
        )
    with col2:
        default_target_index = 0
        if len(spot_names) > 1 and spot_names[0] == start_spot_name:
            default_target_index = 1

        target_spot_name = st.selectbox(
            "选择目标景点",
            options=spot_names,
            key="tsp_target_spot",
            index=default_target_index if default_target_index < len(spot_names) else 0,
        )

    # 筛选必经景点，排除起始和目标景点
    must_pass_options = [
        name for name in spot_names if name not in [start_spot_name, target_spot_name]
    ]
    must_pass_selected_names = st.multiselect(
        "选择必须经过的景点 (可选)",
        options=must_pass_options,
        key="tsp_must_pass_spots",
    )

    weight_type_display = st.radio(
        "选择规划依据 (权重类型)",
        options=["最短距离", "最短时间"],
        key="tsp_weight_type",
    )
    weight_type_model = "distance" if weight_type_display == "最短距离" else "duration"

    if st.button("开始规划"):
        if start_spot_name == target_spot_name:
            st.warning("起始景点和目标景点不能相同。")
        else:
            try:
                start_id = data.graph.find_spot_by_name(start_spot_name).id
                target_id = data.graph.find_spot_by_name(target_spot_name).id

                must_pass_ids = [
                    data.graph.find_spot_by_name(name).id
                    for name in must_pass_selected_names
                ]

                total_cost, planned_path_ids = data.graph.tsp(
                    start_id=start_id,
                    target_id=target_id,
                    must_pass=must_pass_ids,
                    weight_type=weight_type_model,
                )

                st.subheader("规划结果")
                if total_cost == -1:
                    st.error("无法规划出满足条件的路径，部分景点可能不连通或无法经过。")
                else:
                    st.success("成功规划出一条游览路线！")

                    planned_path_names = [
                        data.graph.spots[spot_id].name for spot_id in planned_path_ids
                    ]

                    with st.container(border=True):
                        st.markdown(
                            f"**总{weight_type_display.replace('最短', '')}:** "
                        )
                        if weight_type_model == "distance":
                            st.metric(label="", value=f"{total_cost} 米")
                        else:
                            st.metric(label="", value=f"{total_cost} 分钟")

                        st.markdown("**游览路径:**")
                        st.write(" -> ".join(planned_path_names))

                        if must_pass_selected_names:
                            st.markdown(
                                f"**已包含必经景点:** {', '.join(must_pass_selected_names)}"
                            )

            except SpotIdInvalidError:
                st.error("所选景点ID无效，可能已被删除。")
            except StandardInvalidError as sie:
                st.error(f"规划参数错误: {sie}")
            except Exception as e:
                st.error(f"规划路径失败: {e}")
