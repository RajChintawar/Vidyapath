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
            "userId": user_id,
            "plan": plan
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