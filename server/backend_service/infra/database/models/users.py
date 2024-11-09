from sqlalchemy import Column, Text, Date, Integer
from ..sqlalchemy import get_sqlalchemy

class Users(get_sqlalchemy().Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(Text, nullable=True)
    password = Column(Text, nullable=True)
    role = Column(Text, nullable=True)
    registered_at = Column(Text, nullable=True)
    fullname = Column(Text, nullable=True)
    gender = Column(Text, nullable=True)
    dob = Column(Text, nullable=True)

