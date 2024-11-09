from pydantic import BaseModel
from typing import List

class TestHistory(BaseModel):
    id: int
    exam_id: int
    taken_by_id: int
    taken_date: str
    score: float

class GetTestHistoryRequestSchema(BaseModel):
    pass

class GetTestHistoryResponseSchema(BaseModel):
    message: str
    test_taken: List[TestHistory]