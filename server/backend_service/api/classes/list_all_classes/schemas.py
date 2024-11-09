from pydantic import BaseModel
from typing import List

class ClassInfo(BaseModel):
    id: int
    name: str
    description: str
    created_at: str
    created_by_id: int

class ListAllClassesRequestSchema(BaseModel):
    pass

class ListAllClassesResponseSchema(BaseModel):
    message: str
    classes: List[ClassInfo]