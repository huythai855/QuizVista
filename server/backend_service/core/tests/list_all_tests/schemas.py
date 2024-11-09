from pydantic import BaseModel
from typing import List

class TestInfo(BaseModel):
    id: int
    name: str
    description: str

class ListAllTestsRequest(BaseModel):
    pass

class ListAllTestsResponse(BaseModel):
    tests: List[TestInfo]