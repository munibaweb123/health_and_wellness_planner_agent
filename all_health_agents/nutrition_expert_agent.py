from agents import Agent
from config import openai_model

from tools.goal_analyzer import goal_analyzer
from tools.meal_planner import meal_planner

nutrition_expert_agent = Agent(
    name="Nutrition Expert Agent",
    instructions="You are a nutrition expert agent. You will provide personalized nutrition advice, meal planning, and dietary recommendations based on user preferences and health goals.",
    model=openai_model,
    tools=[goal_analyzer, meal_planner],
    input_guardrails=[]
)