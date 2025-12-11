import pandas as pd
from .habit_model import habit_model, FEATURE_COLUMNS

def load_logs_to_df(db_session):
    """
    Query habit_logs and construct dataframe with yesterday->today mapping to compute break_tomorrow labels.
    """
    from ..models.habit import HabitLog
    logs = db_session.query(HabitLog).order_by(HabitLog.student_id, HabitLog.date).all()
    rows = []
    for l in logs:
        rows.append({
            "student_id": l.student_id,
            "date": l.date.isoformat(),
            **{c: getattr(l, c) for c in FEATURE_COLUMNS},
            "mood": getattr(l, "mood", None)
        })
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows)
    # compute break_tomorrow: if next day's productivity == 0 or study_hours ==0 -> consider break
    df = df.sort_values(["student_id","date"])
    df["break_tomorrow"] = 0
    for sid in df["student_id"].unique():
        s = df[df["student_id"]==sid].reset_index(drop=True)
        for i in range(len(s)-1):
            # simplistic rule: if next day productivity < 3 or study_hours==0 => break
            next_prod = s.loc[i+1,"productivity"] or 0
            next_study = s.loc[i+1,"study_hours"] or 0
            df.loc[s.index[i],"break_tomorrow"] = 1 if (next_prod < 3 or next_study == 0) else 0
    return df
