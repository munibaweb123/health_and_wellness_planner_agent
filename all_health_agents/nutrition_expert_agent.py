from agents import (
    Agent,
    RunContextWrapper,
    GuardrailFunctionOutput,
    input_guardrail,
    output_guardrail
)
from config import openai_model
from tools.goal_analyzer import goal_analyzer
from tools.meal_planner import meal_planner
from pydantic import BaseModel

# -----------------------------
# 📦 Output Schema
# -----------------------------
class NutritionAdviceOutput(BaseModel):
    message: str
    follow_up_required: bool

# -----------------------------
# ✅ Input Guardrail
# -----------------------------
@input_guardrail
async def nutrition_input_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[str]
) -> GuardrailFunctionOutput:
    if isinstance(input, list):
        input_text = " ".join(input)
    else:
        input_text = input.strip()

    if len(input_text) < 10:
        return GuardrailFunctionOutput(
            output_info="❌ Please provide more details about your nutrition goals or concerns.",
            tripwire_triggered=True
        )

    relevant_keywords = ["diet", "nutrition", "meal", "calories", "weight", "protein", "vegan", "keto"]
    if not any(keyword in input_text.lower() for keyword in relevant_keywords):
        return GuardrailFunctionOutput(
            output_info="⚠️ Input does not seem to be about nutrition or meal planning.",
            tripwire_triggered=True
        )

    return GuardrailFunctionOutput(output_info="✅ Input accepted for nutrition expert.", tripwire_triggered=False)

# -----------------------------
# ✅ Output Guardrail
# -----------------------------
@output_guardrail
async def nutrition_output_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, output: NutritionAdviceOutput
) -> GuardrailFunctionOutput:
    prohibited_claims = ["cure", "treat", "heal disease", "reverse diabetes", "stop cancer"]

    if any(claim in output.message.lower() for claim in prohibited_claims):
        return GuardrailFunctionOutput(
            output_info="❌ Output contains unverified or prohibited medical claims.",
            tripwire_triggered=True
        )

    if output.follow_up_required:
        return GuardrailFunctionOutput(
            output_info="🚨 Follow-up may be needed. Recommend speaking to a licensed nutritionist.",
            tripwire_triggered=True
        )

    return GuardrailFunctionOutput(output_info="✅ Output is safe and appropriate.", tripwire_triggered=False)

# -----------------------------
# 🤖 Nutrition Expert Agent
# -----------------------------
nutrition_expert_agent = Agent(
    name="Nutrition Expert Agent",
    instructions="You are a nutrition expert agent. You will provide personalized nutrition advice, meal planning, and dietary recommendations based on user preferences and health goals.",
    model=openai_model,
    tools=[goal_analyzer, meal_planner],
    input_guardrails=[nutrition_input_guardrail],
    output_guardrails=[nutrition_output_guardrail],
    output_type=NutritionAdviceOutput
)

# -----------------------------
# (Optional) Guardrail Agents
# -----------------------------
class NutritionInputCheck(BaseModel):
    input_text: str
    is_valid: bool
    reason: str

nutrition_input_guardrail_agent = Agent(
    name="Nutrition Input Guardrail Agent",
    instructions="""
You are a nutrition input guardrail agent. Review whether the user's input is relevant and complete.
Reject inputs that are vague or off-topic.
""",
    model=openai_model,
    output_type=NutritionInputCheck
)

class NutritionOutputCheck(BaseModel):
    output_summary: str
    follow_up_required: bool
    reason: str

nutrition_output_guardrail_agent = Agent(
    name="Nutrition Output Guardrail Agent",
    instructions="""
You are a nutrition output guardrail agent. Ensure the response is safe, contains no medical claims,
and determine if professional follow-up is needed.
""",
    model=openai_model,
    output_type=NutritionOutputCheck
)
