from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
import pandas as pd

from ..app.db import get_db
from ..models.habit import HabitLog
from ..models.student import Student
from ..schemas.habit import (
    HabitCreate,
    HabitOut,
    PredictionOut,
    CoachOutput,
    RoutineOutput,
)
from ..ml.habit_model import habit_model
from ..ml.coach_llm import generate_ai_coach_message
from ..ml.recommender import generate_recommendations
from ..ml.train_habit_model import load_logs_to_df

router = APIRouter(prefix="/habits", tags=["habits"])

# basic CRUD from before (create_log, get_logs, predict, coach, routine) - keep as is
@router.post("/log", response_model=HabitOut)
def create_log(data: HabitCreate, db: Session = Depends(get_db)):
    log = HabitLog(**data.dict())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

@router.get("/logs/{student_id}", response_model=List[HabitOut])
def get_logs(student_id: int, db: Session = Depends(get_db)):
    logs = db.query(HabitLog).filter(HabitLog.student_id == student_id).order_by(HabitLog.date).all()
    return logs

@router.get("/predict/{student_id}", response_model=PredictionOut)
def predict_break(student_id: int, db: Session = Depends(get_db)):
    log = db.query(HabitLog).filter(HabitLog.student_id == student_id).order_by(HabitLog.date.desc()).first()
    if not log:
        raise HTTPException(status_code=404, detail="No habit logs found")
    prob = habit_model.predict_break({
        "sleep_hours": log.sleep_hours,
        "study_hours": log.study_hours,
        "activity_minutes": log.activity_minutes,
        "screen_time_hours": log.screen_time_hours,
        "productivity": log.productivity
    })
    label = "Low Risk" if prob < 0.4 else "Medium Risk" if prob < 0.7 else "High Risk"
    return PredictionOut(break_probability=round(prob,3), label=label)

@router.get("/coach/{student_id}", response_model=CoachOutput)
def coach(student_id: int, db: Session = Depends(get_db)):
    log = db.query(HabitLog).filter(HabitLog.student_id == student_id).order_by(HabitLog.date.desc()).first()
    if not log:
        raise HTTPException(status_code=404, detail="No habit logs found")
    student = db.query(Student).filter(Student.id == student_id).first()
    personality = student.personality if student else None
    message = generate_ai_coach_message(
        mood=log.mood,
        productivity=log.productivity,
        study_hours=log.study_hours,
        personality=personality,
        goals=(student.goals if student else None)
    )
    return CoachOutput(message=message)

@router.get("/routine/{student_id}", response_model=RoutineOutput)
def routine(student_id: int, db: Session = Depends(get_db)):
    # compute 7-day averages
    logs = db.query(HabitLog).filter(HabitLog.student_id == student_id).order_by(HabitLog.date.desc()).limit(7).all()
    if not logs:
        raise HTTPException(status_code=404, detail="No habit logs found")
    avg = lambda attr: sum((getattr(l,attr) or 0) for l in logs)/len(logs)
    routine = {
        "wake_up": "7:00 AM",
        "morning_study": f"{max(1, int(avg('study_hours')))} hour focused study",
        "exercise": "20-minute walk" if avg('activity_minutes') < 20 else "Maintain current routine",
        "afternoon_focus": "4 × 25-minute Pomodoro sessions",
        "evening_unwind": "Avoid screens 45 minutes before sleep",
        "sleep": "Aim for 7–8 hours"
    }
    # add personalized tweak
    if avg("sleep_hours") < 6:
        routine["sleep_tip"] = "Cut late-night caffeine, wind down 60 minutes before bed"
    if avg("screen_time_hours") > 6:
        routine["screen_tip"] = "Schedule 2 'no-screen' focus blocks of 50 minutes"
    return RoutineOutput(routine=routine)

# ---------------- Analytics ----------------
@router.get("/analytics/{student_id}")
def analytics(student_id: int, db: Session = Depends(get_db)):
    logs = db.query(HabitLog).filter(HabitLog.student_id == student_id).order_by(HabitLog.date.desc()).limit(30).all()
    if not logs:
        raise HTTPException(status_code=404, detail="No habit logs found")
    df = pd.DataFrame([{
        "date": l.date.isoformat(),
        "sleep_hours": l.sleep_hours,
        "study_hours": l.study_hours,
        "activity_minutes": l.activity_minutes,
        "screen_time_hours": l.screen_time_hours,
        "productivity": l.productivity,
        "mood": l.mood
    } for l in logs])
    df["date"] = pd.to_datetime(df["date"])
    stats = {
        "avg_sleep": round(df["sleep_hours"].mean(),2),
        "avg_study": round(df["study_hours"].mean(),2),
        "avg_activity": round(df["activity_minutes"].mean(),2),
        "avg_productivity": round(df["productivity"].mean(),2),
        "mood_counts": df["mood"].value_counts().to_dict()
    }
    # trends (compare last 7 vs previous 7)
    if len(df)>=14:
        last7 = df.head(7)
        prev7 = df.iloc[7:14]
        stats["study_trend"] = round(last7["study_hours"].mean() - prev7["study_hours"].mean(),3)
        stats["sleep_trend"] = round(last7["sleep_hours"].mean() - prev7["sleep_hours"].mean(),3)
    # streaks
    streaks = {}
    # study streak: consecutive days with study_hours >= 1 starting from most recent
    cons_study = 0
    for _, row in df.iterrows():
        if row["study_hours"] >= 1:
            cons_study += 1
        else:
            break
    streaks["study_streak"] = cons_study
    stats["streaks"] = streaks
    return stats

# ---------------- Recommendations ----------------
@router.get("/recommend/{student_id}")
def recommend(student_id: int, db: Session = Depends(get_db)):
    log = db.query(HabitLog).filter(HabitLog.student_id == student_id).order_by(HabitLog.date.desc()).first()
    if not log:
        raise HTTPException(status_code=404, detail="No habit logs found")
    latest = {
        "sleep_hours": log.sleep_hours,
        "study_hours": log.study_hours,
        "activity_minutes": log.activity_minutes,
        "screen_time_hours": log.screen_time_hours,
        "productivity": log.productivity
    }
    recs = generate_recommendations(latest)
    return {"recommendations": recs}

# ---------------- Training endpoint ----------------
@router.post("/train")
def train_model(db: Session = Depends(get_db)):
    df = load_logs_to_df(db)
    if df.empty:
        raise HTTPException(status_code=400, detail="Not enough habit logs to train")
    res = habit_model.train_from_dataframe(df)
    return {"result": res}
