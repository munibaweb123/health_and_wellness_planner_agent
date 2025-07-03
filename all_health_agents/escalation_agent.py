from agents import Agent
from config import openai_model
from tools.goal_analyzer import goal_analyzer
from tools.meal_planner import meal_planner
from tools.tracker import tracker

escalation_agent = Agent(
    name="Escalation Agent",
    instructions="You are an escalation agent. You will handle cases that require additional support or expertise beyond the capabilities of the primary health and wellness planner agent.",
    model=openai_model,
    tools=[goal_analyzer, meal_planner, tracker],
    input_guardrails=[]
)