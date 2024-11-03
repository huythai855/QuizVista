from numpy import integer
from pydantic import BaseModel
import datetime

class CreateClassRequestSchema(BaseModel):
    id: int
    name: str
    description: str

class CreateClassResponseSchema(BaseModel):
    id: int
    name: str
    description: str
    # updated_at: datetime
    # created_at: datetime