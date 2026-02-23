from datetime import datetime, timedelta
from bson import ObjectId
from common.db import db


def generate_study_plan(user_id: str):

    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise Exception("User not found")

    daily_hours = user["studyHoursPerDay"]

    today = datetime.today().date()

    # Fetch pending tasks
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
            days_left = 1  # avoid division by zero

        difficulty_map = {
            "Low": 1,
            "Medium": 2,
            "High": 3
        }

        difficulty_weight = difficulty_map.get(subject["difficulty"], 1)

        urgency_score = 1 / days_left

        priority = urgency_score * difficulty_weight

        enriched_tasks.append({
            "task": task,
            "priority": priority,
            "exam_date": exam_date
        })

    # Sort by priority descending
    enriched_tasks.sort(key=lambda x: x["priority"], reverse=True)

    plan = {}
    current_date = today
    remaining_hours_today = daily_hours

    for item in enriched_tasks:

        task = item["task"]
        exam_date = item["exam_date"]
        hours_left = task["estimatedHours"]

        while hours_left > 0:

            if current_date > exam_date:
                break  # do not schedule beyond exam

            date_str = current_date.isoformat()

            if date_str not in plan:
                plan[date_str] = []

            allocatable = min(hours_left, remaining_hours_today)

            plan[date_str].append({
                "taskId": str(task["_id"]),
                "allocatedHours": allocatable
            })

            hours_left -= allocatable
            remaining_hours_today -= allocatable

            if remaining_hours_today == 0:
                current_date += timedelta(days=1)
                remaining_hours_today = daily_hours

    return plan

# from datetime import datetime
# from bson import ObjectId
# from common.db import db


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