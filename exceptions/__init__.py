class ScenicPathfinderError(Exception):
    """程序基类异常"""

    ...

class GraphError(ScenicPathfinderError):
    """图相关异常"""

    ...


class SpotIdInvalidError(GraphError):
    """景点无效异常"""

    def __init__(self, spot_id: int):
        self.spot_id = spot_id
        super().__init__(f"景点 ID {spot_id} 无效或已被删除")

class SpotNameInvalidError(GraphError):
    """景点名称无效异常"""

    def __init__(self, spot_name: str):
        self.spot_name = spot_name
        super().__init__(f"景点名称 {spot_name} 无效或已被删除")

class SpotNameDuplicateError(GraphError):
    """景点名称重复异常"""

    def __init__(self, spot_name: str):
        self.spot_name = spot_name
        super().__init__(f"景点名称 {spot_name} 已存在，不能重复添加")

class StandardInvalidError(GraphError):
    """标准无效异常"""

    def __init__(self, standard: str):
        self.standard = standard
        super().__init__(f"搜索标准 {standard} 无效，必须为 `distance` 或者 `duration`")
