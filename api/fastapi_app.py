# api/fastapi_app.py
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from user_context import UserSessionContext
from agents import Runner
from main import health_agent  # ✅ import agent logic
from config import config
from utils.db import save_progress_to_db, get_user_logs
from utils.pdf_export import generate_user_progress_pdf
from tools.tracker import tracker_logic
from fastapi.staticfiles import StaticFiles



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-plan")
async def generate_plan(payload: dict = Body(...)):
    input_text = payload["input"]
    context = UserSessionContext(name=payload["name"], uid=payload["uid"])
    result = await Runner.run(health_agent, input=input_text, context=context, run_config=config)
    return result.final_output.dict()

@app.post("/track-progress")
def track_progress(payload: dict = Body(...)):
    save_progress_to_db(str(payload["uid"]), payload["name"], payload["update"])
    context = UserSessionContext(name=payload["name"], uid=payload["uid"])
    return tracker_logic(payload["uid"], payload["update"], context)

@app.get("/progress/{user_id}")
def get_logs(user_id: str):
    return get_user_logs(user_id)

@app.get("/report/{user_id}")
def get_pdf(user_id: str):
    path = generate_user_progress_pdf(user_id)
    return {"url": f"/static/{path}"}
