from sqlalchemy import Column, Text, Date, Integer
from ..sqlalchemy import get_sqlalchemy

class ClassJoin(get_sqlalchemy().Base):
    __tablename__ = "class_join"

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, nullable=True)
    joined_by_id = Column(Integer, nullable=True)
    role = Column(Text, nullable=True)

