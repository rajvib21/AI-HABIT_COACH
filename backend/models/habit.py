from sqlalchemy import Column, Integer, Float, String, Date
from ..app.db import Base

class HabitLog(Base):
    __tablename__ = "habit_logs"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, index=True)
    date = Column(Date, nullable=False)

    sleep_hours = Column(Float)
    study_hours = Column(Float)
    activity_minutes = Column(Integer)
    mood = Column(String)
    screen_time_hours = Column(Float)
    productivity = Column(Float)
