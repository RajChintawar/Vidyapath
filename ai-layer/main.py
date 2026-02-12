
from planning_agent.planner import generate_study_plan
from common.db import db

# automatically fetch first user
user = db.users.find_one({})
print("Using user:", user["_id"])

plan = generate_study_plan(str(user["_id"]))

print("\nGenerated Study Plan:")
print(plan)