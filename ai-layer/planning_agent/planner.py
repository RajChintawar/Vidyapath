from datetime import datetime, timedelta
from bson import ObjectId
from common.db import db


def generate_study_plan(user_id: str):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise Exception("User not found")

    daily_hours = user["studyHoursPerDay"]

    tasks = list(
        db.tasks.find({"status": "pending"}).sort("deadline", 1)
    )

    plan = {}
    current_date = datetime.today().date()
    remaining_hours_today = daily_hours

    for task in tasks:
        hours_left = task["estimatedHours"]

        while hours_left > 0:
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

from datetime import datetime
from bson import ObjectId
from common.db import db


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