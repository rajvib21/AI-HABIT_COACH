from sqlalchemy import Column, Integer, String
from ..app.db import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    roll_no = Column(String, unique=True, nullable=False)

    age = Column(Integer, nullable=True)        
    goals = Column(String, nullable=True)
    personality = Column(String, nullable=True)
