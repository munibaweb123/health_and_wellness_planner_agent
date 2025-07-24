from agents import (
    Agent,
    RunContextWrapper,
    GuardrailFunctionOutput,
    input_guardrail,
    output_guardrail,
)
from config import openai_model
from tools.goal_analyzer import goal_analyzer
from tools.meal_planner import meal_planner
from tools.tracker import tracker
from pydantic import BaseModel

# -----------------------------
# 📦 Output model for escalation agent
# -----------------------------
class EscalationOutput(BaseModel):
    message: str
    action_required: bool

# -----------------------------
# ✅ Input Guardrail Function
# -----------------------------
@input_guardrail
async def escalation_input_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[str]
) -> GuardrailFunctionOutput:
    if isinstance(input, list):
        input_text = " ".join(input)
    else:
        input_text = input

    if len(input_text.strip()) < 10:
        return GuardrailFunctionOutput(
            output_info="❌ Your input is too short. Please provide more details.",
            tripwire_triggered=True,
        )

    escalation_keywords = ["urgent", "immediate", "critical", "emergency"]
    if any(keyword in input_text.lower() for keyword in escalation_keywords):
        return GuardrailFunctionOutput(
            output_info="⚠️ Input indicates urgency. Escalating with caution.",
            tripwire_triggered=True,
        )

    return GuardrailFunctionOutput(output_info="✅ Input is appropriate.", tripwire_triggered=False)

# -----------------------------
# ✅ Output Guardrail Function
# -----------------------------
@output_guardrail
async def escalation_output_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, output: EscalationOutput
) -> GuardrailFunctionOutput:
    if output.action_required:
        return GuardrailFunctionOutput(
            output_info="🚨 Action required. Escalation needs follow-up.",
            tripwire_triggered=True,
        )
    return GuardrailFunctionOutput(output_info="✅ Output is valid.", tripwire_triggered=False)

# -----------------------------
# 🤖 Main Escalation Agent
# -----------------------------
escalation_agent = Agent(
    name="Escalation Agent",
    instructions="You are an escalation agent. You will handle cases that require additional support or expertise beyond the capabilities of the primary health and wellness planner agent.",
    model=openai_model,
    tools=[goal_analyzer, meal_planner, tracker],
    input_guardrails=[escalation_input_guardrail],
    output_guardrails=[escalation_output_guardrail],
    output_type=EscalationOutput,
)

# -----------------------------
# 🤖 Input Guardrail Agent
# -----------------------------
class EscalationInputCheck(BaseModel):
    input_text: str
    is_valid: bool
    reason: str

escalation_input_guardrail_agent = Agent(
    name="Escalation Input Guardrail Agent",
    instructions="""
You are a guardrail agent. Your job is to evaluate whether a user's input message is suitable for escalation.
Return is_valid=True only if it's detailed enough and relevant. Otherwise explain the reason.
""",
    model=openai_model,
    output_type=EscalationInputCheck,
)

# -----------------------------
# 🤖 Output Guardrail Agent
# -----------------------------
class EscalationOutputCheck(BaseModel):
    output_summary: str
    action_required: bool
    reason: str

escalation_output_guardrail_agent = Agent(
    name="Escalation Output Guardrail Agent",
    instructions="""
You are a guardrail agent that reviews the output of the escalation agent.
Decide whether further action is required and explain the reason.
""",
    model=openai_model,
    output_type=EscalationOutputCheck,
)
