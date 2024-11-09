from typing import Optional

from pydantic import BaseModel

class RegisterRequestSchema(BaseModel):
    username: str
    password: str
    role: str
    registered_at: str
    fullname: str
    gender: str
    dob: str


class RegisterResponseSchema(BaseModel):
    message: str
    username: Optional[str]
    user_id: Optional[int]
    fullname: Optional[str]