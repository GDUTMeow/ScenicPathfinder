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
