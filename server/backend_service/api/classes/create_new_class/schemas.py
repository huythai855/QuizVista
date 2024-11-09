from pydantic import BaseModel

class CreateNewClassRequestSchema(BaseModel):
    name: str
    description: str
    created_at: str
    created_by_id: int

class CreateNewClassResponseSchema(BaseModel):
    message: str
    id: int
    name: str
    description: str
    created_at: str
    created_by_id: int