from typing import Optional
from pydantic import BaseModel

class GetTestDetailRequest(BaseModel):
    id: str

class GetTestDetailResponse(BaseModel):
    message: str
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[str] = None
    class_id: Optional[int] = None
    status: Optional[str] = None
    created_by_id: Optional[int] = None
    question_set: Optional[str] = None
    study_note: Optional[str] = None
    mindmap: Optional[str] = None