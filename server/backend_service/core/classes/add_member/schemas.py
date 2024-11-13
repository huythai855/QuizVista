from pydantic import BaseModel

class AddMemberRequest(BaseModel):
    class_id: int
    user_id: int
    role: str

class AddMemberResponse(BaseModel):
    message: str
