from pydantic import BaseModel
from typing import List

class ClassJoinInfo(BaseModel):
    id: int
    class_id: int
    joined_by_id: int
    fullname: str
    role: str

class ListAllMembersRequestSchema(BaseModel):
    class_id: int

class ListAllMembersResponseSchema(BaseModel):
    members: List[ClassJoinInfo]