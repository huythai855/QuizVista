from sqlalchemy import Column, Integer, Text

from ..sqlalchemy import get_sqlalchemy

class Tests(get_sqlalchemy().Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(Text, nullable=True)
    class_id = Column(Integer, nullable=True)
    status = Column(Text, nullable=True)
    created_by_id = Column(Integer, nullable=True)
    question_set = Column(Text, nullable=True) # Base64 encoded string
    study_note = Column(Text, nullable=True)
    mindmap = Column(Text, nullable=True)
