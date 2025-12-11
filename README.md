# 🌟 AI Habit Tracker & Wellness Coach  
### An AI-powered behavior analytics, habit prediction, and personalized coaching system

This project is a complete **AI Wellness & Habit Intelligence Suite** built using:

- **FastAPI** backend  
- **Streamlit** frontend  
- **SQLite database**  
- **Machine Learning (Scikit-learn)**  
- **Local LLM (Ollama + Llama 3.2)**  
- **Data visualizations with Plotly**  

It tracks student habits, predicts streak breaks, generates analytics, and provides an AI-powered personal coach.

---

# 🚀 Features

## ✅ **1. Habit Logging System**
Students can log daily habits:

- Sleep hours  
- Study hours  
- Activity time  
- Mood  
- Productivity  
- Screen time  

Data is stored in SQLite.

---

## ✅ **2. AI Habit Break Prediction**
ML model predicts the probability of breaking habit streaks using:

- RandomForestClassifier  
- 7-day trend analysis  
- Break-tomorrow labeling  

Outputs:

- **Break Probability**
- **Risk Label (Low/Medium/High)**

---

## ✅ **3. AI Wellness Coach (LLM + Personality Awareness)**

Uses **Ollama Llama 3.2** to provide coaching such as:

- Mood-based encouragement  
- Personalized study suggestions  
- Streak recovery advice  
- Goal-oriented motivation  

Example prompt fields:

- mood  
- productivity  
- study_hours  
- personality  
- goals  

---

## ✅ **4. Analytics Dashboard**

Shows:

- Average sleep/study/productivity  
- Mood distribution charts  
- Trend comparisons (last 7 vs previous 7 days)  
- Study streak detection  
- Full logs table  
- Interactive graphs  

---

## ✅ **5. Personalized Daily Routine Generator**

AI generates routines based on past behavior:

- Morning study block  
- Exercise recommendation  
- Screen-time management  
- Sleep optimization  

---

## ✅ **6. Offline Recommendation Engine**

Suggests improvements based on last habit entry:

- Sleep improvement  
- Focus strategies  
- Productivity hacks  
- Activity increase suggestions  

---

# 🗂 Project Structure
AIHabitCoach/
│
├── backend/
│ ├── app/
│ │ ├── db.py
│ │ ├── main.py
│ ├── models/
│ ├── routers/
│ ├── schemas/
│ └── ml/
│
├── streamlit_app/
│ └── habit_ui.py
│
├── models/
│ └── habit_predict.joblib (auto-generated)
│
└── README.md


---

# 🛠 Installation & Setup

## 1️⃣ Clone the repo

```sh
git clone https://github.com/rajvib21/AI-HABIT_COACH.git
cd AI-HABIT_COACH

2️⃣ Create virtual environment
python -m venv venv


Activate (Windows):

venv\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Start FastAPI backend
uvicorn backend.app.main:app --reload



5️⃣ Start Streamlit app

Open NEW terminal:

streamlit run streamlit_app/habit_ui.py


6️⃣ Start Ollama (AI Coach)

Install from: https://ollama.com/download

Run model:

ollama pull llama3.2
ollama serve

🎯 Future Enhancements

Gamification (XP, Badges, Streak Fire)

Weekly AI Insights Report

Mood Forecast Model

Voice-based coaching

Personal Habit Timeline

💡 Author

Rajvi Bhatt


