import sys
from bson import ObjectId # type: ignore
from common.db import db
from planning_agent.planner import generate_study_plan, save_study_plan
from datetime import datetime


def seed_data():
    print("Seeding test data...")

    user = db.users.find_one({})
    if not user:
        print("No user found.")
        return

    subject = db.subjects.insert_one({
        "userId": user["_id"],
        "subjectName": "Seed Subject",
        "difficulty": "Medium",
        "examDate": "2026-04-01"
    })

    task = db.tasks.insert_one({
        "subjectId": subject.inserted_id,
        "topic": "Seed Topic",
        "deadline": datetime(2026, 3, 20),
        "estimatedHours": 4,
        "status": "pending"
    })

    print("Inserted Subject:", subject.inserted_id)
    print("Inserted Task:", task.inserted_id)


def run_planner():
    user = db.users.find_one({})
    if not user:
        print("No user found.")
        return

    user_id = str(user["_id"])
    print("Using user:", user_id)

    plan = generate_study_plan(user_id)

    print("\nGenerated Study Plan:")
    print(plan)

    if plan:
        save_study_plan(user_id, plan)
        print("\nStudy Plan Saved to DB.")
    else:
        print("No pending tasks. Nothing saved.")


def run_replanner():
    print("Replanner not implemented yet.")


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python main.py [seed | plan | replan]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "seed":
        seed_data()

    elif command == "plan":
        run_planner()

    elif command == "replan":
        run_replanner()

    else:
        print("Unknown command.")

