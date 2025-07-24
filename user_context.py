from pydantic import BaseModel, Field
from typing import List, Optional

class MealDay(BaseModel):
    day: str
    meals: List[str]

class MealPlan(BaseModel):
    days: List[MealDay]

class ProgressLog(BaseModel):
    date: str
    note: str

class InjuryNotes(BaseModel):
    type: str
    severity: str
    description: str

class Goal(BaseModel):
    type: str
    target: str

class WorkoutPlan(BaseModel):
    days: List[str]
    intensity: str

class UserSessionContext(BaseModel):
    name: str
    uid: int
    goal: Optional[Goal] = None
    diet_preferences: Optional[List[str]] = Field(default_factory=list) # This was previously fixed
    workout_plan: Optional[WorkoutPlan] = None
    meal_plan: Optional[MealPlan] = None # Still an issue, but let's fix injury_notes first

    # --- CHANGE THIS LINE ---
    injury_notes: Optional[List[str]] = Field(default_factory=list) # Changed from Optional[str]
    # ------------------------

    handoff_logs: List[str] = Field(default_factory=list)
    progress_logs: List[ProgressLog] = Field(default_factory=list)