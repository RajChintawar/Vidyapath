from common.db import db
from bson import ObjectId # type: ignore
from fastapi import FastAPI, HTTPException # type: ignore
from planning_agent.planner import generate_study_plan, save_study_plan
from replanning_agent.replan import run_replanner 

app = FastAPI(title="Vidyapath AI Engine")


@app.get("/")
def health_check():
    return {"status": "AI Engine Running"}


@app.post("/generate-plan/{user_id}")
def generate_plan(user_id: str):
    try:
        plan = generate_study_plan(user_id)

        if plan:
            save_study_plan(user_id, plan)

            return {
        "message": "Plan generated",
        "days": plan
    }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/replan/{user_id}")
def replan(user_id: str):
    try:
        run_replanner(user_id)
        return {"message": "Replanning executed"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@app.get("/studyplan/{user_id}")
def get_studyplan(user_id: str):

    plans = list(
        db.studyplans.find(
            {"userId": ObjectId(user_id)}
        )
    )

    result = []

    for p in plans:

        p["_id"] = str(p["_id"])
        p["userId"] = str(p["userId"])

        if "tasks" in p:
            for t in p["tasks"]:
                t["taskId"] = str(t["taskId"])

        result.append(p)

    return result

@app.get("/progress/{user_id}")
def get_progress(user_id: str):

    from bson import ObjectId # type: ignore

    uid = ObjectId(user_id)

    total = db.tasks.count_documents({})
    completed = db.tasks.count_documents({"status": "completed"})
    pending = db.tasks.count_documents({"status": "pending"})

    missed = db.activitylogs.count_documents({
        "action": "missed"
    })

    plans = list(
        db.studyplans.find({"userId": uid})
    )

    avg_conf = 0
    risk = "UNKNOWN"

    if plans:

        conf_values = [
            p.get("confidence", 0.5)
            for p in plans
            if "confidence" in p
        ]

        if conf_values:
            avg_conf = sum(conf_values) / len(conf_values)

        risk = plans[-1].get("risk", "UNKNOWN")

    return {
        "totalTasks": total,
        "completed": completed,
        "pending": pending,
        "missed": missed,
        "avgConfidence": round(avg_conf, 2),
        "latestRisk": risk
    }

@app.get("/studyplan/latest/{user_id}")
def get_latest_plan(user_id: str):

    from bson import ObjectId # type: ignore
    from common.db import db

    uid = ObjectId(user_id)

    plan = db.studyplans.find_one(
        {"userId": uid},
        sort=[("date", -1)]
    )

    if not plan:
        return {"message": "No plan found"}

    plan["_id"] = str(plan["_id"])
    plan["userId"] = str(plan["userId"])

    if "tasks" in plan:
        for t in plan["tasks"]:
            t["taskId"] = str(t["taskId"])

    return plan

@app.get("/subjects/{user_id}")
def get_subjects(user_id: str):

    from bson import ObjectId # type: ignore
    from common.db import db

    uid = ObjectId(user_id)

    subjects = list(
        db.subjects.find(
            {"userId": uid}
        )
    )

    result = []

    for s in subjects:

        s["_id"] = str(s["_id"])
        s["userId"] = str(s["userId"])

        result.append(s)

    return result


@app.get("/tasks/{user_id}")
def get_tasks(user_id: str):

    from bson import ObjectId # type: ignore
    from common.db import db

    uid = ObjectId(user_id)

    subjects = list(
        db.subjects.find({"userId": uid})
    )

    subject_ids = [s["_id"] for s in subjects]

    tasks = list(
        db.tasks.find(
            {"subjectId": {"$in": subject_ids}}
        )
    )

    result = []

    for t in tasks:

        t["_id"] = str(t["_id"])
        t["subjectId"] = str(t["subjectId"])

        result.append(t)

    return result


@app.post("/activitylog")
def add_log(data: dict):

    from common.db import db
    from bson import ObjectId # type: ignore
    from datetime import datetime

    log = {
        "taskId": ObjectId(data["taskId"]),
        "action": data["action"],
        "timestamp": datetime.utcnow()
    }

    db.activitylogs.insert_one(log)

    return {"status": "ok"}