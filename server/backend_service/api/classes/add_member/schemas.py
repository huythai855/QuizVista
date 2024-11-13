from pydantic import BaseModel

class AddMemberRequestSchema(BaseModel):
    class_id: int
    user_id: int
    role: str

class AddMemberResponseSchema(BaseModel):
    message: str