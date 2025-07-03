from typing import Optional, List
from pydantic import BaseModel, Field

class Goal(BaseModel):
    type: Optional[str] = None
    target: Optional[str] = None
    duration: Optional[str] = None

class WorkoutPlan(BaseModel):
    days: Optional[List[str]] = None
    details: Optional[str] = None

class ProgressLog(BaseModel):
    date: Optional[str] = None
    note: Optional[str] = None

class UserSessionContext(BaseModel):
    name: str
    uid: int
    goal: Optional[Goal] = None
    diet_preferences: Optional[str] = None
    workout_plan: Optional[WorkoutPlan] = None
    meal_plan: Optional[List[str]] = None
    injury_notes: Optional[str] = None
    handoff_logs: List[str] = Field(default_factory=list)
    progress_logs: List[ProgressLog] = Field(default_factory=list)