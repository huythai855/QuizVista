from sqlalchemy import Column, Integer, Text, Float

from ..sqlalchemy import get_sqlalchemy

class TestTaken(get_sqlalchemy().Base):
    __tablename__ = "test_taken"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, nullable=True)
    taken_by_id = Column(Integer, nullable=True)
    taken_date = Column(Text, nullable=True)
    score = Column(Float, nullable=True)
