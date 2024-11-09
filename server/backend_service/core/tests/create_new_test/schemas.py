from pydantic import BaseModel
from typing import Optional

class CreateNewTestRequest(BaseModel):
    name: str
    description: str
    created_at: str
    class_id: int
    status: str
    created_by_id: int
    question_set: str
    study_note: str
    mindmap: str

class CreateNewTestResponse(BaseModel):
    message: str
    id: Optional[int]
    name: Optional[str]
    description: Optional[str]