import pandas as pd

def calculate_kpis(data):
    projects = data["Projects"]
    beneficiaries = data["Beneficiaries"]
    performance = data["Performance"]

    active = projects["Project_Status"].astype(str).str.lower().eq("active").sum()
    learners = pd.to_numeric(
        beneficiaries["Number_of_Learners"], errors="coerce"
    ).fillna(0).sum()

    target = pd.to_numeric(
        performance["Target_Learners"], errors="coerce"
    ).fillna(0).sum()
    actual = pd.to_numeric(
        performance["Actual_Learners"], errors="coerce"
    ).fillna(0).sum()

    achievement = (actual / target * 100) if target > 0 else 0

    return {
        "projects": projects["Project_ID"].nunique(),
        "active_projects": int(active),
        "learners": int(learners),
        "achievement": achievement
    }

def performance_summary(performance):
    frame = performance.copy()
    for col in ["Target_Learners", "Actual_Learners",
                "Planned_Activities", "Completed_Activities"]:
        frame[col] = pd.to_numeric(frame[col], errors="coerce").fillna(0)

    frame["Learner_Achievement_Pct"] = (
        frame["Actual_Learners"].div(frame["Target_Learners"].replace(0, pd.NA)) * 100
    )
    frame["Activity_Completion_Pct"] = (
        frame["Completed_Activities"].div(frame["Planned_Activities"].replace(0, pd.NA)) * 100
    )
    return frame
