from typing import Optional

from pydantic import BaseModel

class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str
    registered_at: str
    fullname: str
    gender: str
    dob: str


class RegisterResponse(BaseModel):
    message: str
    username: Optional[str] = None
    user_id: Optional[int] = None
    fullname: Optional[str] = None