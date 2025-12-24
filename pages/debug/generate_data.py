import streamlit as st
import random
from models.graph import Spot

data = st.session_state.app_data

st.header("⚙️ 调试功能：自动生成测试数据")
st.info("此页面用于快速填充系统数据，方便进行功能测试。")

st.subheader("当前数据概览")
col1, col2 = st.columns(2)
col1.metric("景点数量 (Nodes)", value=data.graph.nodes)
col2.metric("道路数量 (Paths)", value=data.graph.paths)

with st.expander("点击查看当前原始 JSON 数据"):
    st.json(data.model_dump_json())

st.divider()

st.subheader("生成新的随机数据")

st.warning(
    "⚠️ **注意：** 此操作将首先 **清空所有** 现有的景点和道路数据，然后生成全新的随机数据。此过程不可逆！"
)

if st.button("生成 8 个景点和 15 条随机道路", type="primary"):
    try:
        data.graph.spots.clear()

        spot_names = [
            "游客中心",
            "行政楼",
            "变电站",
            "小变电站",
            "军营",
            "水泥厂",
            "坝顶",
            "建筑工地",
        ]

        for i, name in enumerate(spot_names):
            new_spot = Spot(
                id=i, name=name, description=f"这里是 {name} 的详细介绍", deleted=False
            )
            data.graph.spots.append(new_spot)

        num_spots = len(data.graph.spots)
        generated_paths = set()

        while len(generated_paths) < 15:
            from_id, to_id = random.sample(range(num_spots), 2)

            path_key = tuple(sorted((from_id, to_id)))

            if path_key not in generated_paths:
                generated_paths.add(path_key)

                distance = random.randint(100, 1500)
                duration = random.randint(5, 25)

                data.graph.add_path(from_id, to_id, distance, duration)

        data.save()
        st.toast("测试数据生成成功！", icon="🎉")
        st.rerun()

    except Exception as e:
        st.error(f"生成数据时发生错误: {e}")
