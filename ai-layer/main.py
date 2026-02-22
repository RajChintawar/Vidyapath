
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