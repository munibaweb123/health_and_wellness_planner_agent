from agents import Agent, GuardrailFunctionOutput, RunContextWrapper, Runner, TResponseInputItem, input_guardrail, output_guardrail
from tools.goal_analyzer import goal_analyzer
from tools.tracker import tracker
from tools.meal_planner import meal_planner
from tools.schedular import schedular
from tools.workout_recommender import workout_recommender
from config import openai_model, config
from all_health_agents.escalation_agent import escalation_agent
from all_health_agents.injury_support_agent import injury_support_agent
from all_health_agents.nutrition_expert_agent import nutrition_expert_agent
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import re

# Output schema for the agent
class HealthPlanOutput(BaseModel):
    meal_plan: Optional[List[str]] = None
    workout_plan: Optional[List[str]] = None
    schedule: Optional[List[str]] = None  # <- added for schedular
    tracking_summary: Optional[str] = None  # <- added for tracker
    notes: Optional[str] = None


class Health_Output(BaseModel):
    is_health_and_wellness: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail agent",
    instructions="You are a guardrail agent. You will ensure that the user's input is safe and appropriate for the health and wellness planner agent.",
    model=openai_model,
    output_type=Health_Output
)

@input_guardrail
async def health_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    if isinstance(input, list):
        input_text = " ".join(str(i) for i in input)
    else:
        input_text = input

    goal_pattern = r"(lose|gain|maintain|improve|reduce|increase|build|help|plan|diet|workout|exercise|meal|weight|muscle|fitness)"
    if len(input_text.strip()) < 10:
        return GuardrailFunctionOutput(
            output_info="Your input is too short. Please provide more details.",
            tripwire_triggered=True,
        )

    if not re.search(goal_pattern, input_text.lower()):
        return GuardrailFunctionOutput(
            output_info="Please specify a health-related goal or request (e.g., 'I want to lose weight', 'Help me improve my fitness', 'Suggest a meal plan').",
            tripwire_triggered=True,
        )

    # Optionally, check strict pattern, but do not block or warn
    # strict_pattern = r"(lose|gain|maintain)\s+\d+\s*(kg|lbs|pounds|kilograms)\s+in\s+\d+\s*(days|weeks|months|years)"
    # if not re.search(strict_pattern, input_text.lower()):
    #     pass  # No warning, just allow

    result = await Runner.run(guardrail_agent, input=input, run_config=config)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_health_and_wellness,
    )

@output_guardrail
async def health_output_guardrail(
    ctx: RunContextWrapper, agent: Agent, output
) -> GuardrailFunctionOutput:
    # Optionally, you can run another agent/tool here for validation
    # For demonstration, let's assume you want to check if output is a valid HealthPlanOutput

    # If you want to call another agent for validation, do it here (example commented out):
    # result = await Runner.run(guardrail_agent, output, context=ctx.context, run_config=config)
    # return GuardrailFunctionOutput(
    #     output_info=result.final_output,
    #     tripwire_triggered=not result.final_output.is_health_and_wellness,
    # )

    # Otherwise, just validate output structure
    if isinstance(output, HealthPlanOutput):
        return GuardrailFunctionOutput(
            output_info=output,
            tripwire_triggered=False
        )
    if isinstance(output, dict):
        return GuardrailFunctionOutput(
            output_info=HealthPlanOutput(**output),
            tripwire_triggered=False
        )
    return GuardrailFunctionOutput(
        output_info=HealthPlanOutput(notes="Output was not structured as expected."),
        tripwire_triggered=True
    )

health_agent = Agent(
    name="Health and wellness planner agent",
    instructions="You are a health and wellness planner agent. You will use tools to help users create personalized health and wellness plans based on their goals, preferences, and lifestyle.",
    model=openai_model,
    tools=[goal_analyzer, meal_planner, schedular, tracker, workout_recommender],
    handoffs=[escalation_agent, injury_support_agent, nutrition_expert_agent],
    input_guardrails=[health_guardrail],
    output_type=HealthPlanOutput,
    output_guardrails=[health_output_guardrail]
)