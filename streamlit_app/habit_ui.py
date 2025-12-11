import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time

FASTAPI_BASE = "http://localhost:8000"

st.set_page_config(page_title="AI Habit Suite", layout="wide")
st.title("🌟 AI Habit Tracker & Wellness Coach — Dashboard")

# Sidebar student selection & profile quick create
st.sidebar.header("Student")
student_id = st.sidebar.number_input("Student ID", min_value=1, value=1, step=1)
with st.sidebar.expander("Create quick student"):
    name = st.text_input("Name", value="Test Student")
    roll = st.text_input("Roll No", value=f"R{student_id:03d}")
    if st.button("Create student"):
        payload = {"name": name, "roll_no": roll}
        r = requests.post(f"{FASTAPI_BASE}/students/", json=payload)
        if r.status_code == 200:
            st.success("Student created")
        else:
            st.error(r.text)

tabs = st.tabs(["Dashboard","Log Habit","Analytics","AI Coach","Routine","Train Model"])

# ---------- Dashboard ----------
with tabs[0]:
    st.header("Overview")
    col1, col2, col3 = st.columns(3)
    try:
        r = requests.get(f"{FASTAPI_BASE}/habits/predict/{student_id}")
        if r.ok:
            d = r.json()
            col1.metric("Break Prob", f"{d['break_probability']*100:.1f}%")
            col1.write("Risk:", d["label"])
    except:
        col1.write("No prediction available")

    try:
        r = requests.get(f"{FASTAPI_BASE}/habits/recommend/{student_id}")
        if r.ok:
            recs = r.json().get("recommendations",[])
            col2.write("Top Recommendations")
            for rtxt in recs:
                col2.write("-", rtxt)
    except:
        col2.write("No recommendations")

    try:
        r = requests.get(f"{FASTAPI_BASE}/habits/analytics/{student_id}")
        if r.ok:
            stats = r.json()
            col3.metric("Avg Study (7d)", stats.get("avg_study","-"))
            col3.metric("Avg Sleep (7d)", stats.get("avg_sleep","-"))
            st.write("Mood counts:", stats.get("mood_counts",{}))
    except:
        col3.write("No analytics available")

# ---------- Log Habit ----------
with tabs[1]:
    st.subheader("Log Today's Habit")
    with st.form("log_form"):
        c1,c2,c3 = st.columns(3)
        with c1:
            sleep_hours = st.number_input("Sleep hours", 0.0, 24.0, 7.0)
            study_hours = st.number_input("Study hours", 0.0, 24.0, 2.0)
        with c2:
            activity_minutes = st.number_input("Activity minutes", 0, 300, 20)
            screen_time_hours = st.number_input("Screen time hours", 0.0, 24.0, 4.0)
        with c3:
            mood = st.selectbox("Mood", ["happy","neutral","stressed","tired"])
            productivity = st.slider("Productivity (1-10)", 1, 10, 6)
        date = st.date_input("Date")
        if st.form_submit_button("Save"):
            payload = {
                "student_id": int(student_id),
                "date": str(date),
                "sleep_hours": float(sleep_hours),
                "study_hours": float(study_hours),
                "activity_minutes": int(activity_minutes),
                "mood": mood,
                "screen_time_hours": float(screen_time_hours),
                "productivity": float(productivity)
            }
            r = requests.post(f"{FASTAPI_BASE}/habits/log", json=payload)
            if r.ok:
                st.success("Saved")
            else:
                st.error(r.text)

# ---------- Analytics ----------
with tabs[2]:
    st.subheader("History & Charts")
    if st.button("Load last 30 logs"):
        r = requests.get(f"{FASTAPI_BASE}/habits/analytics/{student_id}")
        if r.ok:
            stats = r.json()
            st.json(stats)
        else:
            st.error(r.text)
    # also show full logs table
    r2 = requests.get(f"{FASTAPI_BASE}/habits/logs/{student_id}")
    if r2.ok:
        df = pd.DataFrame(r2.json())
        if not df.empty:
            df["date"] = pd.to_datetime(df["date"])
            st.dataframe(df)
            fig = px.line(df, x="date", y="study_hours", title="Study Hours")
            st.plotly_chart(fig)
            fig2 = px.line(df, x="date", y="sleep_hours", title="Sleep Hours")
            st.plotly_chart(fig2)

# ---------- AI Coach ----------
with tabs[3]:
    st.subheader("Get AI Coach Advice")
    if st.button("Get Advice"):
        r = requests.get(f"{FASTAPI_BASE}/habits/coach/{student_id}")
        if r.ok:
            st.success(r.json().get("message"))
        else:
            st.error(r.text)

# ---------- Routine ----------
with tabs[4]:
    st.subheader("Personalized Routine")
    if st.button("Generate Routine"):
        r = requests.get(f"{FASTAPI_BASE}/habits/routine/{student_id}")
        if r.ok:
            st.json(r.json().get("routine"))
        else:
            st.error(r.text)

# ---------- Train Model ----------
with tabs[5]:
    st.subheader("Train Habit & Mood Models")
    st.write("This will pull logs and train models. Need at least ~20 rows for reasonable result.")
    if st.button("Train Models Now"):
        with st.spinner("Training..."):
            r = requests.post(f"{FASTAPI_BASE}/habits/train")
            if r.ok:
                st.success("Training completed")
                st.json(r.json())
            else:
                st.error(r.text)
