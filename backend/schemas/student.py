from pydantic import BaseModel

# -----------------------------
# SCHEMA: Create Student
# -----------------------------
class StudentCreate(BaseModel):
    name: str
    roll_no: str
    age: int | None = None
    goals: str | None = None
    personality: str | None = None


# -----------------------------
# SCHEMA: Update Student
# -----------------------------
class StudentUpdate(BaseModel):
    name: str | None = None
    roll_no: str | None = None
    age: int | None = None
    goals: str | None = None
    personality: str | None = None


# -----------------------------
# SCHEMA: Output Student
# -----------------------------
class StudentOut(BaseModel):
    id: int
    name: str
    roll_no: str
    age: int | None = None
    goals: str | None = None
    personality: str | None = None

    # REQUIRED FOR Pydantic v2 to read SQLAlchemy objects
    class Config:
        from_attributes = True
