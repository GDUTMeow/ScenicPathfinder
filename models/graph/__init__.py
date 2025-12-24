from __future__ import annotations

import heapq

from pydantic import BaseModel, Field, constr
from typing import Dict, List, Optional, Literal, Tuple

from exceptions import (
    SpotIdInvalidError,
    StandardInvalidError,
    SpotNameInvalidError,
    SpotNameDuplicateError,
)


class Path(BaseModel):
    """
    表示从当前节点到另一个节点的道路的信息

    :param target(int): 目标景点的索引
    :param distance(int): 路径长度
    :param duration(int): 所需时间
    """

    target_id: int = Field(..., description="目标景点的索引")
    distance: int = Field(..., description="路径长度")
    duration: int = Field(..., description="所需时间")


class Spot(BaseModel):
    """
    表示景点节点的信息

    :param id(int): 当前景点的索引
    :param name(str): 景点名称
    :param description(str): 景点简介
    :param deleted(bool): 景点是否已删除
    :param paths(List[Path]): 从当前景点出发的路径列表
    """

    id: int = Field(..., description="景点的整数索引")
    name: str = Field(..., description="景点名称")
    description: str = Field(..., description="景点简介")
    paths: List[Path] = Field(default=[], description="从当前景点出发的路径列表")
    deleted: bool = Field(default=False, description="景点是否已删除")


class TourGraph(BaseModel):
    """
    导览系统封装

    :param spots(List[Spot]): 景点节点列表
    """

    spots: List[Spot] = []

    # 景点数量
    @property
    def nodes(self) -> int:
        return len(self.spots)

    # 道路数量
    @property
    def paths(self) -> int:
        return sum(len(s.paths) for s in self.spots) // 2

    def _is_valid_node(self, node_id: int) -> bool:
        """
        判断节点是否存在或者被软删除

        :param node_id(int): 节点索引
        :return: 节点是否有效
        """
        return 0 <= node_id < len(self.spots) and not self.spots[node_id].deleted

    def _have_same_spot_name(self, name: str) -> bool:
        """
        判断是否存在同名景点

        :param name(str): 景点名称
        :return: 是否存在同名景点
        """
        for spot in self.spots:
            if spot.name == name and not spot.deleted:
                return True
        return False

    def add_node(self, spot: Spot) -> int:
        """
        添加一个新的景点

        :param spot(Spot): 景点节点
        """
        if self._have_same_spot_name(spot.name):
            raise SpotNameDuplicateError(spot.name)
        node_id = len(self.spots)
        spot = Spot(id=node_id, name=spot.name, description=spot.description)
        self.spots.append(spot)
        return node_id

    def add_path(self, from_id: int, to_id: int, distance: int, duration: int) -> None:
        """
        为两个景点之间添加一条道路

        :param from_id(int): 起始景点索引
        :param to_id(int): 目标景点索引
        :param distance(int): 路径长度
        :param duration(int): 所需时间
        """
        from_spot = self.spots[from_id]
        to_spot = self.spots[to_id]
        from_spot.paths.append(
            Path(target_id=to_id, distance=distance, duration=duration)
        )
        to_spot.paths.append(
            Path(target_id=from_id, distance=distance, duration=duration)
        )

    def modify_node(
        self, target_id: int, name: str | None = None, description: str | None = None
    ) -> None:
        """
        修改景点信息

        :param target_id(int): 目标景点索引
        :param name(str | None): 新的景点名称
        :param description(str | None): 新的景点简介
        """
        spot = self.spots[target_id]
        if name is not None:
            spot.name = name
        if description is not None:
            spot.description = description

    def delete_node(self, target_id: int) -> None:
        """
        删除景点

        :param target_id(int): 目标景点索引
        """
        spot = self.spots[target_id]
        spot.deleted = True

    def modify_path(
        self,
        from_id: int,
        to_id: int,
        distance: int | None = None,
        duration: int | None = None,
    ) -> None:
        """
        修改道路信息

        :param from_id(int): 起始景点索引
        :param to_id(int): 目标景点索引
        :param distance(int | None): 新的路径长度
        :param duration(int | None): 新的所需时间
        """
        from_spot = self.spots[from_id]
        to_spot = self.spots[to_id]

        for path in from_spot.paths:
            if path.target_id == to_id:
                if distance is not None:
                    path.distance = distance
                if duration is not None:
                    path.duration = duration
                break

        for path in to_spot.paths:
            if path.target_id == from_id:
                if distance is not None:
                    path.distance = distance
                if duration is not None:
                    path.duration = duration
                break

    def delete_path(self, from_id: int, to_id: int) -> None:
        """
        删除道路

        :param from_id(int): 起始景点索引
        :param to_id(int): 目标景点索引
        """
        from_spot = self.spots[from_id]
        to_spot = self.spots[to_id]

        from_spot.paths = [path for path in from_spot.paths if path.target_id != to_id]
        to_spot.paths = [path for path in to_spot.paths if path.target_id != from_id]

    def dijkstra(
        self,
        start_id: int,
        target_id: int,
        weight_type: Literal["distance", "duration"],
    ) -> Tuple[int, List[int]]:
        """
        利用 dijkstra 算法求从起点到终点的最短路径
        允许以距离或者时间作为权重进行求解

        :param start_id(int): 起始景点索引
        :param target_id(int): 目标景点索引
        :param weight_type(Literal['distance', 'duration']): 权重类型
        :return: 最短路径的总权重和路径经过的景点索引列表
        """
        if not self._is_valid_node(start_id):
            raise SpotIdInvalidError(start_id)
        if not self._is_valid_node(target_id):
            raise SpotIdInvalidError(target_id)

        weights = {
            spot.id: float("inf") for spot in self.spots if not spot.deleted
        }  # 初始化为无穷大
        weights[start_id] = 0  # 自己到自己距离为 0

        previous_nodes: Dict[int, None | int] = {
            spot.id: None for spot in self.spots if not spot.deleted
        }
        pq = [(0, start_id)]  # 优先队列，存储 (距离, 节点索引)

        while pq:
            current_weight, current_id = heapq.heappop(pq)

            if current_id == target_id:
                break  # 找到最短路径，提前退出
            if current_weight > weights[current_id]:  # type: ignore
                continue  # 已经有更短的路径，跳过

            current_spot = self.spots[current_id]
            for path in current_spot.paths:
                if not self._is_valid_node(path.target_id):
                    continue  # 跳过已删除的节点

                weight = path.distance if weight_type == "distance" else path.duration
                new_weight = current_weight + weight

                if new_weight < weights[path.target_id]:  # type: ignore
                    # 找到更短路径，更新权重和前驱节点
                    weights[path.target_id] = new_weight
                    previous_nodes[path.target_id] = current_id
                    heapq.heappush(pq, (new_weight, path.target_id))

        if weights[target_id] == float("inf"):
            # 终点非可达
            return -1, []  # 不可达返回 -1

        path_sequence = []
        current_id = target_id
        while current_id is not None:
            path_sequence.append(current_id)
            current_id = previous_nodes[current_id]

        return (
            int(weights[target_id]),
            path_sequence[::-1],
        )  # 返回总权重和路径序列，因为在这里是肯定找到了
        # 所以可以直接 int 一下，不然 int('inf') 会炸 ValueError

    def _dfs(
        self,
        current: int,
        target: int,
        path: List[int],
        current_distance: int,
        current_duration: int,
        visited: set,
    ) -> List[Tuple[int, int, List[int]]]:
        """
        用来求所有路径的 DFS

        :param current(int): 当前节点索引
        :param target(int): 目标节点索引
        :param path(List[int]): 当前路径
        :param current_dist(int): 当前路径总距离
        :param current_duration(int): 当前路径总时间
        :param visited(set): 已访问节点集合
        :return : List[Tuple[int, int, List[int]]]: 所有路径结果列表
        """
        results = []
        if current == target:
            results.append(
                (current_distance, current_duration, list(path))
            )  # 找到一条路径
            return results

        visited.add(current)
        spot = self.spots[current]
        for p in spot.paths:
            neighbor = p.target_id
            if (
                self._is_valid_node(neighbor) and neighbor not in visited
            ):  # 节点存在且未访问过
                path.append(neighbor)
                sub_paths = self._dfs(
                    neighbor,
                    target,
                    path,
                    current_distance + p.distance,
                    current_duration + p.duration,
                    visited,
                )
                results.extend(sub_paths)  # 收集子路径结果
                path.pop()  # 回溯

        visited.remove(current)  # 回溯时去掉访问状态
        return results

    def find_all_paths(
        self, start_id: int, target_id: int
    ) -> List[Tuple[int, int, List[int]]]:
        """
        利用 DFS 算法求从起点到终点的所有路径

        :param start_id(int): 起始景点索引
        :param target_id(int): 目标景点索引
        :return: 所有路径的列表，每条路径包含 (总距离, 总时间, 路径经过的景点索引列表)
        """
        if not self._is_valid_node(start_id):
            raise SpotIdInvalidError(start_id)
        if not self._is_valid_node(target_id):
            raise SpotIdInvalidError(target_id)

        result = self._dfs(
            start_id,
            target_id,
            path=[start_id],
            current_distance=0,
            current_duration=0,
            visited=set(),
        )
        return result

    def tsp(
        self,
        start_id: int,
        target_id: int,
        must_pass: List[int],
        weight_type: Literal["distance", "duration"],
    ) -> Tuple[int, List[int]]:
        """
        贪心算法解决旅行商问题
        懒，没办法，不想写 DP 啥的那么复杂的东西了，就这样吧，毁灭吧

        :param start_id(int): 起始景点索引
        :param target_id(int): 目标景点索引
        :param must_pass(List[int]): 必须经过的景点索引列表
        :param weight_type(Literal['distance', 'duration']): 权重类型
        :return: 最短路径的总权重和路径经过的景点索引列表
        """
        if not self._is_valid_node(start_id):
            raise SpotIdInvalidError(start_id)
        if not self._is_valid_node(target_id):
            raise SpotIdInvalidError(target_id)

        if weight_type not in ["distance", "duration"]:
            raise StandardInvalidError("weight_type must be 'distance' or 'duration'")

        # 构建必须访问的节点列表
        to_visit = set()
        for pid in must_pass:
            if self._is_valid_node(pid) and pid != start_id and pid != target_id:
                to_visit.add(pid)

        current_node = start_id
        total_cost = 0
        full_path: List[int] = []

        full_path.append(start_id)  # 加入起点

        # 寻找未访问过的节点
        while to_visit:
            best_next_node = -1
            min_dist = float("inf")
            best_segment_path = []

            for candidate in to_visit:
                # 找距离当前位置最近的必经点
                dist, path = self.dijkstra(current_node, candidate, weight_type)

                # 连通且距离短
                if dist != -1 and dist < min_dist:
                    min_dist = dist
                    best_next_node = candidate
                    best_segment_path = path

            # 不连通
            if best_next_node == -1:
                return -1, []

            # 累加距离
            total_cost += int(min_dist)

            # 拼接路径
            if not full_path:
                full_path.extend(best_segment_path)
            else:
                full_path.extend(best_segment_path[1:])

            # 更改当前位置并在未访问列表中删除
            current_node = best_next_node
            to_visit.remove(current_node)

        # 从当前点前往终点
        dist_to_end, path_to_end = self.dijkstra(current_node, target_id, weight_type)

        if dist_to_end == -1:
            return -1, []

        total_cost += int(dist_to_end)

        if not full_path:
            full_path.extend(path_to_end)
        else:
            full_path.extend(path_to_end[1:])

        return total_cost, full_path

    def find_spot_by_name(self, name: str) -> Spot:
        """
        根据景点名称查找景点

        :param name(str): 景点名称
        :return: 找到的景点对象
        """
        for spot in self.spots:
            if spot.name == name and not spot.deleted:
                return spot
        raise SpotNameInvalidError(name)
