from sqlalchemy import Column, Text, Integer
from ..sqlalchemy import get_sqlalchemy



class Classes(get_sqlalchemy().Base):
    __tablename__ = "classes"

    id = Column(Text, primary_key=True, index=True)
    name = Column(Text, nullable=True)
    description = Column(Text, nullable=True)