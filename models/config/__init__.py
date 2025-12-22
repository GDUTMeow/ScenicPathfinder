from pydantic import BaseModel

__all__ = ["metadata"]

class metadata(BaseModel):
    appname: str = "ScenicPathfinder"
    version: str = "1.0.0"
    author: str = "GamerNoTitle"