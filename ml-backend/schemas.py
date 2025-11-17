from pydantic import BaseModel
from typing import List

class TrainRequest(BaseModel):
    samples: List[List[int]]   # Example: [[1,0,1,0,1,0], ... ]

class PredictionRequest(BaseModel):
    values: List[int]          # Example: [1,0,1,0,0,1]
