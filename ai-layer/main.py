
from planning_agent.planner import generate_study_plan, save_study_plan
from common.db import db

user = db.users.find_one({})
print("Using user:", user["_id"])

plan = generate_study_plan(str(user["_id"]))

print("\nGenerated Study Plan:")
print(plan)

if plan:
    save_study_plan(str(user["_id"]), plan)
    print("\nStudy Plan Saved to DB.")
else:
    print("\nNo pending tasks. Nothing saved.")


from common.db import db
from bson import ObjectId # type: ignore
from datetime import datetime

# Replace with your real user id
USER_ID = ObjectId("698579cbefbf271b6d5933d0")

# 1️⃣ Insert new subject
new_subject = {
    "userId": USER_ID,
    "subjectName": "Mathematics",
    "difficulty": "Low",
    "examDate": "2026-03-10"
}

subject_result = db.subjects.insert_one(new_subject)
print("Inserted Subject ID:", subject_result.inserted_id)

# 2️⃣ Insert new task for that subject
new_task = {
    "subjectId": subject_result.inserted_id,
    "topic": "Linear Algebra",
    "deadline": datetime(2026, 2, 28),
    "estimatedHours": 4,
    "status": "pending"
}

task_result = db.tasks.insert_one(new_task)
print("Inserted Task ID:", task_result.inserted_id)


