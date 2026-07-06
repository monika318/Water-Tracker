from fastapi import FastAPI
from pydantic import BaseModel
from src.agent import WaterIntakeAgent
from src.database import log_water_intake, get_intake_history
from src.logger import log_message

app = FastAPI()
agent = WaterIntakeAgent()

class WaterIntakeRequest(BaseModel):
    user_id: str
    intake_ml   : int


@app.post("/log_intake")
async def log_intake(request: WaterIntakeRequest):
    log_water_intake(request.user_id, request.intake_ml)
    analysis = agent.analyze_intake( request.intake_ml)
    log_message(f"Logged {request.intake_ml} ml of water intake for user {request.user_id}.")
    return {"message": f"Logged {request.intake_ml} ml of water intake for user {request.user_id}.", "analysis": analysis}

@app.get("/intake_history/{user_id}")
async def get_water_history(user_id: str):
    history = get_intake_history(user_id)
    log_message(f"Retrieved water intake history for user {user_id}.")
    return {"user_id": user_id, "history": history}

