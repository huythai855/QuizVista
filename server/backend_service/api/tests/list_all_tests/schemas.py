from pydantic import BaseModel
from typing import List

class TestInfo(BaseModel):
    id: int
    name: str
    description: str

class ListAllTestsRequestSchema(BaseModel):
    pass

class ListAllTestsResponseSchema(BaseModel):
    tests: List[TestInfo]