from tools.goal_analyzer import goal_analyzer
from tools.meal_planner import meal_planner
from tools.tracker import tracker
from agents import Agent
from config import openai_model
injury_support_agent = Agent(
    name="Injury Support Agent",
    instructions="You are an injury support agent. You will provide personalized advice and support for users dealing with injuries, including recovery tips, rehabilitation exercises, and emotional support.",
    model=openai_model,
    tools=[goal_analyzer, meal_planner, tracker],
    input_guardrails=[]
)