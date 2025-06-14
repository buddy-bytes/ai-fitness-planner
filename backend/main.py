from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .core import get_plan, evaluate_plan

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GoalRequest(BaseModel):
    goal: str


class EvaluateRequest(BaseModel):
    goal: str
    plan: str

@app.post("/generate")
async def generate(req: GoalRequest):
    try:
        plan = get_plan(req.goal)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"plan": plan}


@app.post("/evaluate")
async def evaluate(req: EvaluateRequest):
    try:
        feedback = evaluate_plan(req.goal, req.plan)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"feedback": feedback}

