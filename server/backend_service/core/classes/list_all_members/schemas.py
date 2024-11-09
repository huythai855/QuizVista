from pydantic import BaseModel
from typing import List

class ClassJoinInfo(BaseModel):
    id: int
    class_id: int
    joined_by_id: int
    fullname: str
    role: str

class ListAllMembersRequest(BaseModel):
    class_id: int

class ListAllMembersResponse(BaseModel):
    members: List[ClassJoinInfo]