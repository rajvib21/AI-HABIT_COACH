import random

def generate_ai_coach_message(mood: str, productivity: float, study_hours: float, personality: str=None, goals: str=None) -> str:
    mood = (mood or "").lower()
    personality = (personality or "").lower()
    base_msgs = []

    # personality-aware intro
    if "procrast" in (personality or ""):
        base_msgs.append("I know starting is the hardest part — small wins matter.")
    elif "disciplined" in (personality or ""):
        base_msgs.append("You have the discipline — let's channel it into focused sprints.")
    elif "anxious" in (personality or ""):
        base_msgs.append("Breathe — we'll make a calm, doable plan for today.")
    else:
        base_msgs.append("You're doing good — here are a few tailored tips.")

    # mood-specific
    if mood == "stressed":
        base_msgs.append("You're stressed. Pause for 5–10 minutes of breathing or a short walk.")
    elif mood == "tired":
        base_msgs.append("You're tired. Try to rest and keep tomorrow's tasks light.")
    elif mood == "happy":
        base_msgs.append("Great energy today — make a small progress step toward your goal.")
    else:
        base_msgs.append("Keep steady — consistency adds up.")

    # productivity guidance
    if productivity < 4:
        base_msgs.append("Try one 25-minute Pomodoro sprint right now. No multitasking.")
    elif productivity < 7:
        base_msgs.append("Two focused sessions with short breaks will help keep momentum.")
    else:
        base_msgs.append("You're productive — schedule one learning challenge to level up.")

    # study hours advice
    if study_hours < 2:
        base_msgs.append("Start with 25 minutes on the easiest topic — build momentum.")
    else:
        base_msgs.append("Good study time — add short reviews next day to retain more.")

    # goal-aware nudges
    if goals:
        base_msgs.append(f"Remember your goal: {goals}. Small daily actions move you closer.")

    # pick 2-3 messages to return as a single coherent msg
    sel = base_msgs[:3] if len(base_msgs)>=3 else base_msgs
    return " ".join(sel)
