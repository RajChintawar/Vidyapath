from datetime import datetime, timedelta
from bson import ObjectId
from common.db import db


# ==============================
# Performance Boost Function
# ==============================
def get_task_performance_boost(task_id):
    logs = list(db.activitylogs.find({"taskId": task_id}))

    if not logs:
        return 1

    boost = 1

    for log in logs:
        if log["action"] == "missed":
            boost += 0.5
        elif log["action"] == "completed":
            boost -= 0.2

    return max(boost, 0.5)


# ==============================
# Study Plan Generator
# ==============================
def generate_study_plan(user_id: str):

    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise Exception("User not found")

    daily_hours = user["studyHoursPerDay"]
    today = datetime.today().date()

    raw_tasks = list(db.tasks.find({"status": "pending"}))
    enriched_tasks = []

    for task in raw_tasks:

        subject = db.subjects.find_one({"_id": task["subjectId"]})
        if not subject:
            continue

        deadline = task["deadline"].date()
        exam_date = datetime.strptime(subject["examDate"], "%Y-%m-%d").date()

        days_left = (deadline - today).days
        if days_left <= 0:
            days_left = 1

        difficulty_map = {
            "Low": 1,
            "Medium": 2,
            "High": 3
        }

        difficulty_weight = difficulty_map.get(subject["difficulty"], 1)
        urgency_score = 1 / days_left

        performance_boost = get_task_performance_boost(task["_id"])
        priority = urgency_score * difficulty_weight * performance_boost

        enriched_tasks.append({
            "task": task,
            "priority": priority,
            "exam_date": exam_date,
            "difficulty": subject["difficulty"]
        })

    # Sort by priority descending
    enriched_tasks.sort(key=lambda x: x["priority"], reverse=True)

    plan = {}
    current_date = today
    remaining_hours_today = daily_hours

    difficulty_chunk_map = {
        "Low": 2,
        "Medium": 1.5,
        "High": 1
    }

    task_pool = []

    for item in enriched_tasks:
        task_pool.append({
            "task": item["task"],
            "hours_left": item["task"]["estimatedHours"],
            "exam_date": item["exam_date"],
            "difficulty": item["difficulty"]
        })

    while any(t["hours_left"] > 0 for t in task_pool):

        for t in task_pool:

            if t["hours_left"] <= 0:
                continue

            if current_date > t["exam_date"]:
                continue

            if remaining_hours_today <= 0:
                current_date += timedelta(days=1)
                remaining_hours_today = daily_hours

            chunk_size = difficulty_chunk_map.get(t["difficulty"], 1)

            allocatable = min(chunk_size, t["hours_left"], remaining_hours_today)

            if allocatable <= 0:
                continue

            date_str = current_date.isoformat()

            if date_str not in plan:
                plan[date_str] = []

            plan[date_str].append({
                "taskId": str(t["task"]["_id"]),
                "allocatedHours": allocatable
            })

            t["hours_left"] -= allocatable
            remaining_hours_today -= allocatable

    # Merge duplicate entries per day
    for date in plan:
        merged = {}
        for entry in plan[date]:
            tid = entry["taskId"]
            merged[tid] = merged.get(tid, 0) + entry["allocatedHours"]

        plan[date] = [
            {"taskId": tid, "allocatedHours": hrs}
            for tid, hrs in merged.items()
        ]

    return plan


# ==============================
# Save Study Plan
# ==============================
def save_study_plan(user_id: str, plan: dict):

    user_object_id = ObjectId(user_id)

    for date_str, tasks in plan.items():

        existing_plan = db.studyplans.find_one({
            "userId": user_object_id,
            "date": date_str
        })

        studyplan_doc = {
            "userId": user_object_id,
            "date": date_str,
            "tasks": [
                {
                    "taskId": ObjectId(t["taskId"]),
                    "allocatedHours": t["allocatedHours"]
                }
                for t in tasks
            ],
            "updatedAt": datetime.utcnow()
        }

        if existing_plan:
            db.studyplans.update_one(
                {"_id": existing_plan["_id"]},
                {"$set": studyplan_doc}
            )
            print(f"Updated study plan for {date_str}")

        else:
            studyplan_doc["createdAt"] = datetime.utcnow()
            db.studyplans.insert_one(studyplan_doc)
            print(f"Inserted study plan for {date_str}")