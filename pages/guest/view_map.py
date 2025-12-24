import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from streamlit_agraph import agraph, Node, Edge, Config

data = st.session_state.app_data

st.header("景区地图")


def create_graph_from_data(graph_data):
    """
    将 TourGraph 数据转换为 networkx 图对象
    """
    G = nx.Graph()

    # 添加节点
    for spot in graph_data.spots:
        if not spot.deleted:
            G.add_node(spot.id, label=spot.name, title=spot.description)

    # 添加边
    processed_edges = set()
    for spot in graph_data.spots:
        if not spot.deleted:
            for path in spot.paths:
                # 检查边的另一端是否也是有效节点
                if graph_data._is_valid_node(path.target_id):
                    edge_key = tuple(sorted((spot.id, path.target_id)))

                    if edge_key not in processed_edges:
                        G.add_edge(
                            spot.id,
                            path.target_id,
                            label=f"{path.distance}m / {path.duration}min",
                            title=f"距离: {path.distance}m, 时间: {path.duration}min",
                        )
                        processed_edges.add(edge_key)
    return G


if not any(not spot.deleted for spot in data.graph.spots):
    st.warning("当前系统中没有任何有效景点，无法生成地图，请联系景区管理员")
else:
    if "tour_nx_graph" not in locals():
        tour_nx_graph = create_graph_from_data(data.graph)

    pos = nx.spring_layout(tour_nx_graph, k=0.8, iterations=50, seed=42)
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    fig, ax = plt.subplots(figsize=(25, 15))

    # 提取节点和边的标签
    node_labels = nx.get_node_attributes(tour_nx_graph, "label")
    edge_labels = nx.get_edge_attributes(tour_nx_graph, "label")

    # 绘制节点
    nx.draw_networkx_nodes(
        tour_nx_graph, pos, node_size=3000, node_color="skyblue", ax=ax
    )
    # 绘制节点标签
    nx.draw_networkx_labels(
        tour_nx_graph,
        pos,
        labels=node_labels,
        font_size=12,
        font_family="sans-serif",
        ax=ax,
    )
    # 绘制边
    nx.draw_networkx_edges(
        tour_nx_graph, pos, edge_color="lightcoral", width=1.5, ax=ax
    )
    # 绘制边的标签
    nx.draw_networkx_edge_labels(
        tour_nx_graph, pos, edge_labels=edge_labels, font_size=12, ax=ax
    )

    ax.margins(0.1)
    plt.axis("off")
    st.pyplot(fig)
