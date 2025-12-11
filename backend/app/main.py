from fastapi import FastAPI
from .db import Base, engine

# Import models
from ..models.student import Student
from ..models.habit import HabitLog

# Import routers
from ..routers.students import router as students_router
from ..routers.habits import router as habits_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Habit Tracker & AI Coach")

# Include routers
app.include_router(students_router)
app.include_router(habits_router)
