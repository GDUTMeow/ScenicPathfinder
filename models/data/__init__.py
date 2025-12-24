import os

from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from models.graph import TourGraph
from context import get_workdir


class ApplicationData(BaseModel):
    graph: TourGraph = Field(default_factory=lambda: TourGraph(spots=[]))
    file: str = Field(
        default_factory=lambda: os.path.join(get_workdir(), "data/graph.json")
    )

    def save(self, filepath: str | None = None):
        if filepath is None:
            filepath = str(self.file)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.graph.model_dump_json(indent=4))

    def read(self, filepath: str | None = None):
        if filepath is None:
            filepath = str(self.file)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                self.graph = TourGraph.model_validate_json(f.read())
        else:
            self.graph = TourGraph(spots=[])


data = ApplicationData()
