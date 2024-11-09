from pydantic import BaseModel
from typing import Optional

class LoginRequestSchema(BaseModel):
    username: str
    password: str

class LoginResponseSchema(BaseModel):
    message: str
    user_id: Optional[int] = None
    username: Optional[str] = None
    fullname: Optional[str] =  None