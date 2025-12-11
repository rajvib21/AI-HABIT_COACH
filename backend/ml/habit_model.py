import os
import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

MODEL_DIR = "models"
HABIT_MODEL_PATH = os.path.join(MODEL_DIR, "habit_predict.joblib")
MOOD_MODEL_PATH = os.path.join(MODEL_DIR, "mood_predict.joblib")

FEATURE_COLUMNS = ["sleep_hours","study_hours","activity_minutes","screen_time_hours","productivity"]

class HabitModel:
    def __init__(self):
        os.makedirs(MODEL_DIR, exist_ok=True)
        self.model = None
        self.mood_model = None
        if os.path.exists(HABIT_MODEL_PATH):
            self.model = joblib.load(HABIT_MODEL_PATH)
        if os.path.exists(MOOD_MODEL_PATH):
            self.mood_model = joblib.load(MOOD_MODEL_PATH)

    def featurize_row(self, row):
        return np.array([row.get(c,0) for c in FEATURE_COLUMNS]).reshape(1,-1)

    def predict_break(self, log):
        if not self.model or not hasattr(self.model, "classes_"):
            return 0.5
        x = self.featurize_row(log)
        p = self.model.predict_proba(x)[0][1]
        return float(p)

    def predict_mood(self, log):
        if not self.mood_model or not hasattr(self.mood_model, "classes_"):
            return "neutral"
        x = self.featurize_row(log)
        pred = self.mood_model.predict(x)[0]
        return str(pred)

    def train_from_dataframe(self, df):
        """
        df: pandas DataFrame with feature columns and 'break_tomorrow' (0/1) and 'mood' labels
        """
        # Train habit break model
        X = df[FEATURE_COLUMNS].fillna(0).values
        y = df["break_tomorrow"].values
        if len(y) < 10:
            return {"error":"not enough data to train"}
        X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)
        clf = RandomForestClassifier(n_estimators=100, random_state=42)
        clf.fit(X_train,y_train)
        preds = clf.predict(X_test)
        acc = accuracy_score(y_test,preds)
        joblib.dump(clf, HABIT_MODEL_PATH)
        self.model = clf

        # Train mood predictor if 'mood' exists
        mood_info = {}
        if "mood" in df.columns and df["mood"].notna().sum()>10:
            X2 = df[FEATURE_COLUMNS].fillna(0).values
            y2 = df["mood"].astype(str).values
            X2_train,X2_test,y2_train,y2_test = train_test_split(X2,y2,test_size=0.2,random_state=42)
            mclf = RandomForestClassifier(n_estimators=100, random_state=42)
            mclf.fit(X2_train,y2_train)
            macc = accuracy_score(y2_test, mclf.predict(X2_test))
            joblib.dump(mclf, MOOD_MODEL_PATH)
            self.mood_model = mclf
            mood_info = {"mood_acc": round(float(macc),3)}

        return {"habit_acc": round(float(acc),3), **mood_info}

habit_model = HabitModel()
