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

