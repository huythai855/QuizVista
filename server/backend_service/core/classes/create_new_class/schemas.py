from pydantic import BaseModel

class CreateNewClassRequest(BaseModel):
    name: str
    description: str
    created_at: str
    created_by_id: int

class CreateNewClassResponse(BaseModel):
    message: str
    id: int
    name: str
    description: str
    created_at: str
    created_by_id: int