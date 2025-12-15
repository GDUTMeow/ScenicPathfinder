from __future__ import annotations
from pydantic import BaseModel, Field, constr
from typing import Dict, List

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
    deleted: bool = Field(False, description="景点是否已删除")
    paths: List[Path] = [] 

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

    def add_node(self, spot: Spot) -> None:
        """
        添加一个新的景点
        
        :param spot(Spot): 景点节点
        """
        self.spots.append(spot)
        
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
        from_spot.paths.append(Path(target_id=to_id, distance=distance, duration=duration))
        to_spot.paths.append(Path(target_id=from_id, distance=distance, duration=duration))
        
    def modify_node(self, target_id: int, name: str | None = None, description: str | None = None) -> None:
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
        
    def modify_path(self, from_id: int, to_id: int, distance: int | None = None, duration: int | None = None) -> None:
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