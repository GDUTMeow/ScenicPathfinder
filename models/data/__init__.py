import os

from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from models.graph import TourGraph
from context import get_workdir

class ApplicationData(BaseModel):
    graph: TourGraph
    last_updated: datetime
    file: str = Field(default_factory=lambda: os.path.join(get_workdir(), "data/graph.json"))
    
    def save(self, filepath: str = file):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as f:
            f.write(self.graph.model_dump_json())
            
    def read(self, filepath: str = file):
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                self.graph = TourGraph.model_validate_json(f.read())
        else:
            self.graph = TourGraph(spots=[])
            self.last_updated = datetime.now()
