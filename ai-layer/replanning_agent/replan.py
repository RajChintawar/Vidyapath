from datetime import datetime, timedelta
from bson import ObjectId# type: ignore 
from common.db import db
from planning_agent.planner import generate_study_plan, save_study_plan


def detect_missed_tasks(user_id):
    yesterday = datetime.today().date() - timedelta(days=1)

    logs = list(db.activitylogs.find({
        "action": "missed",
        "timestamp": {
            "$gte": datetime.combine(yesterday, datetime.min.time()),
            "$lte": datetime.combine(yesterday, datetime.max.time())
        }
    }))

    return logs


def delete_future_plans(user_id):
    tomorrow = datetime.today().date() + timedelta(days=1)

    result = db.studyplans.delete_many({
        "userId": ObjectId(user_id),
        "date": {"$gte": tomorrow.isoformat()}
    })

    print(f"Deleted {result.deleted_count} future study plans.")


def run_replanner(user_id):
    print("Running Replanning Agent...")

    missed_logs = detect_missed_tasks(user_id)

    if not missed_logs:
        print("No missed tasks yesterday. No replanning needed.")
        return

    print(f"Detected {len(missed_logs)} missed tasks.")

    delete_future_plans(user_id)

    new_plan = generate_study_plan(user_id)

    if new_plan:
        save_study_plan(user_id, new_plan)
        print("Replanning completed successfully.")
    else:
        print("No new plan generated.")