from datetime import datetime, timedelta
from bson import ObjectId  # type: ignore
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
# Reliability Function
# ==============================
def get_task_reliability(task_id):

    logs = list(
        db.activitylogs
        .find({"taskId": task_id})
        .sort("timestamp", -1)
        .limit(10)
    )

    if not logs:
        return 0.5

    score = 0
    weight = 1.0
    decay = 0.8

    for log in logs:

        if log["action"] == "completed":
            score += 1 * weight

        elif log["action"] == "missed":
            score += 0 * weight

        weight *= decay

    reliability = score / sum(decay ** i for i in range(len(logs)))

    return round(reliability, 2)


# ==============================
# Risk Function
# ==============================
def get_risk_level(confidence):

    if confidence >= 0.75:
        return "LOW"
    elif confidence >= 0.5:
        return "MEDIUM"
    else:
        return "HIGH"


# ==============================
# Study Plan Generator
# ==============================
def generate_study_plan(user_id: str):

    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise Exception("User not found")

    daily_hours = user["studyHoursPerDay"]
    today = datetime.utcnow().date()
    # ✅ get subjects of this user
    subjects = list(
    db.subjects.find({"userId": ObjectId(user_id)})
)

    subject_ids = []
    for s in subjects:
     subject_ids.append(ObjectId(s["_id"]))

    raw_tasks = list(
    db.tasks.find({
        "subjectId": {
            "$in": subject_ids
        },
        "status": "pending"
    })
)
    print("RAW TASKS:", raw_tasks)

    enriched_tasks = []

    for task in raw_tasks:

        subject = db.subjects.find_one(
            {"_id": task["subjectId"]}
        )

        if not subject:
            continue

    deadline_field = task["deadline"]

    if isinstance(deadline_field, datetime):
        deadline = deadline_field.date()
    else:
       deadline = datetime.fromisoformat(
        str(deadline_field).replace("Z", "")
    ).date()

    exam_field = subject["examDate"]

    if isinstance(exam_field, datetime):
       exam_date = exam_field.date()
    else:
       exam_date = datetime.fromisoformat(
        str(exam_field)
    ).date()

       days_left = (deadline - today).days

    if days_left <= 0:
            days_left = 1

    difficulty_map = {
            "Low": 1,
            "Medium": 2,
            "High": 3
        }

    difficulty_weight = difficulty_map.get(
            subject["difficulty"],
            1
        )

    urgency_score = 1 / days_left

    performance_boost = get_task_performance_boost(
            task["_id"]
        )

    reliability = get_task_reliability(
            task["_id"]
        )

    priority = (
            urgency_score
            * difficulty_weight
            * performance_boost
            * (1 + (1 - reliability))
        )

    enriched_tasks.append({
            "task": task,
            "priority": priority,
            "exam_date": exam_date,
            "difficulty": subject["difficulty"],
            "explanation": {
                "difficulty": subject["difficulty"],
                "daysLeft": days_left,
                "urgencyScore": urgency_score,
                "performanceBoost": performance_boost,
                "reliability": reliability,
                "finalPriority": priority
            }
        })

    enriched_tasks.sort(key=lambda x: x["priority"], reverse=True)

    plan = {}
    current_date = datetime.utcnow().date()
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
            "difficulty": item["difficulty"],
            "explanation": item["explanation"]
        })

    loop_guard = 0

    while any(t["hours_left"] > 0 for t in task_pool):

        loop_guard += 1
        if loop_guard > 1000:
            print("Loop guard triggered")
            break
        progress_made = False
        for t in task_pool:

            if t["hours_left"] <= 0:
                continue

            if current_date > t["exam_date"]:
                    t["hours_left"] = 0
                    continue

            if remaining_hours_today <= 0:
                current_date += timedelta(days=1)
                remaining_hours_today = daily_hours

            chunk_size = int(difficulty_chunk_map.get(t["difficulty"], 1))
            allocatable = min(chunk_size, t["hours_left"], remaining_hours_today)

            if allocatable <= 0:
             current_date += timedelta(days=1)
             remaining_hours_today = daily_hours
             continue


            date_str = current_date.isoformat()

            if date_str not in plan:
                plan[date_str] = []

            plan[date_str].append({
                "taskId": str(t["task"]["_id"]),
                "allocatedHours": allocatable,
                "explanation": t["explanation"]
            })

            t["hours_left"] = max(0, t["hours_left"] - allocatable)
            remaining_hours_today -= allocatable
            progress_made = True 

            if not progress_made:
             print("No progress possible, breaking loop")
             break

    # merge duplicates
    for date in plan:

        merged = {}
        explanation_map = {}

        for entry in plan[date]:

            tid = entry["taskId"]

            if tid not in merged:
                merged[tid] = 0
                explanation_map[tid] = entry["explanation"]

            merged[tid] += entry["allocatedHours"]

        plan[date] = [
            {
                "taskId": tid,
                "allocatedHours": hrs,
                "explanation": explanation_map[tid]
            }
            for tid, hrs in merged.items()
        ]


    # confidence + risk
    final_plan = {}

    for date, tasks in plan.items():

        total_reliability = 0
        count = 0

        for task in tasks:
            task_id = ObjectId(task["taskId"])
            reliability = get_task_reliability(task_id)

            total_reliability += reliability
            count += 1

        if count > 0:
            confidence = round(total_reliability / count, 2)
        else:
            confidence = 0.5

        risk = get_risk_level(confidence)

        final_plan[date] = {
            "tasks": tasks,
            "confidence": confidence,
            "risk": risk
        }

    print("FINAL PLAN:", final_plan)
    return final_plan


# ==============================
# Save Study Plan
# ==============================
def save_study_plan(user_id: str, plan: dict):

    user_object_id = ObjectId(user_id)

    for date_str, day_data in plan.items():

        tasks = day_data["tasks"]
        confidence = day_data.get("confidence", 0.5)
        risk = day_data.get("risk", "MEDIUM")

        studyplan_doc = {
            "userId": user_object_id,
            "date": date_str,
            "confidence": confidence,
            "risk": risk,
            "tasks": [
                {
                    "taskId": ObjectId(t["taskId"]),
                    "allocatedHours": t["allocatedHours"]
                }
                for t in tasks
            ],
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        }

        db.studyplans.insert_one(studyplan_doc)

        print(f"Inserted study plan for {date_str}")