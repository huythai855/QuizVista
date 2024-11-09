from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    message: str
    user_id: Optional[int] = None
    username: Optional[str] = None
    fullname: Optional[str] = None