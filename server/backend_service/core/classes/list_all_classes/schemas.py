from pydantic import BaseModel
from typing import List

class ClassInfo(BaseModel):
    id: int
    name: str
    description: str
    created_at: str
    created_by_id: int

class ListAllClassesRequest(BaseModel):
    pass

class ListAllClassesResponse(BaseModel):
    message: str
    classes: List[ClassInfo]