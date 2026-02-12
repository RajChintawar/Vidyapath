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