from pydantic import BaseModel
from datetime import date

class HabitCreate(BaseModel):
    student_id: int
    date: date
    sleep_hours: float
    study_hours: float
    activity_minutes: int
    mood: str
    screen_time_hours: float
    productivity: float

class HabitOut(HabitCreate):
    id: int

    class Config:
        from_attributes = True  # REQUIRED for SQLAlchemy models (Pydantic v2)

class PredictionOut(BaseModel):
    break_probability: float
    label: str

class CoachOutput(BaseModel):
    message: str

class RoutineOutput(BaseModel):
    routine: dict

