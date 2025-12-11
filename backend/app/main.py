from fastapi import FastAPI
from .db import Base, engine

# Import models so SQLAlchemy creates tables
from ..models import student, habit

# Import routers (IMPORTANT: router object, not module)
from ..routers.students import router as students_router
from ..routers.habits import router as habits_router

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Habit Tracker & Coach")

# REGISTER ROUTERS
app.include_router(students_router)
app.include_router(habits_router)

