def generate_recommendations(latest_log):
    recs = []
    sleep = latest_log.get("sleep_hours",0)
    study = latest_log.get("study_hours",0)
    activity = latest_log.get("activity_minutes",0)
    screen = latest_log.get("screen_time_hours",0)
    prod = latest_log.get("productivity",5)

    if sleep < 6:
        recs.append("Improve sleep: try wind-down routine, avoid screens 1 hour before bed.")
    if activity < 20:
        recs.append("Increase activity: short 20-min walk daily or light yoga.")
    if study < 2:
        recs.append("Try focused study: 2 × 50-min sessions or Pomodoro 4 × 25 min.")
    if screen > 6:
        recs.append("Reduce screen time: use app-blocker during study hours.")
    if prod < 5:
        recs.append("Micro-goals: set 3 small tasks today and reward completion.")
    if not recs:
        recs.append("Keep going — your routine looks balanced. Maintain consistency.")
    return recs
