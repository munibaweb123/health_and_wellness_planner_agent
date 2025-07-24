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
from tools.tracker import tracker
from pydantic import BaseModel

# -----------------------------
# 📦 Output model
# -----------------------------
class InjurySupportOutput(BaseModel):
    message: str
    requires_follow_up: bool

# -----------------------------
# ✅ Input Guardrail Function
# -----------------------------
@input_guardrail
async def injury_input_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[str]
) -> GuardrailFunctionOutput:
    if isinstance(input, list):
        input_text = " ".join(input)
    else:
        input_text = input.strip()

    if len(input_text) < 10:
        return GuardrailFunctionOutput(
            output_info="❌ Input too short. Please describe your injury or issue in more detail.",
            tripwire_triggered=True
        )

    if "diagnose" in input_text.lower() or "what is wrong with me" in input_text.lower():
        return GuardrailFunctionOutput(
            output_info="⚠️ I cannot provide a medical diagnosis. Please consult a professional.",
            tripwire_triggered=True
        )

    return GuardrailFunctionOutput(output_info="✅ Input accepted for injury support.", tripwire_triggered=False)

# -----------------------------
# ✅ Output Guardrail Function
# -----------------------------
@output_guardrail
async def injury_output_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, output: InjurySupportOutput
) -> GuardrailFunctionOutput:
    if "diagnosis" in output.message.lower():
        return GuardrailFunctionOutput(
            output_info="❌ Output contains diagnosis, which is not allowed.",
            tripwire_triggered=True
        )

    if output.requires_follow_up:
        return GuardrailFunctionOutput(
            output_info="🚨 Follow-up action may be necessary. Please ensure user is guided appropriately.",
            tripwire_triggered=True
        )

    return GuardrailFunctionOutput(output_info="✅ Output passed all checks.", tripwire_triggered=False)

# -----------------------------
# 🤖 Injury Support Agent
# -----------------------------
injury_support_agent = Agent(
    name="Injury Support Agent",
    instructions=(
        "You are an injury support agent. You will provide personalized advice and support for users "
        "dealing with injuries, including recovery tips, rehabilitation exercises, and emotional support."
    ),
    model=openai_model,
    tools=[goal_analyzer, meal_planner, tracker],
    input_guardrails=[injury_input_guardrail],
    output_guardrails=[injury_output_guardrail],
    output_type=InjurySupportOutput
)

# -----------------------------
# Optional: Guardrail Agent for Input (Agent-based)
# -----------------------------
class InjuryInputCheck(BaseModel):
    input_text: str
    is_valid: bool
    reason: str

injury_input_guardrail_agent = Agent(
    name="Injury Input Guardrail Agent",
    instructions="""
You are a guardrail agent that reviews whether user input is suitable for injury support.
Reject if the input is too vague or is requesting a medical diagnosis.
""",
    model=openai_model,
    output_type=InjuryInputCheck
)

# -----------------------------
# Optional: Guardrail Agent for Output (Agent-based)
# -----------------------------
class InjuryOutputCheck(BaseModel):
    output_summary: str
    requires_follow_up: bool
    reason: str

injury_output_guardrail_agent = Agent(
    name="Injury Output Guardrail Agent",
    instructions="""
You are a guardrail agent that checks whether the injury support output contains any inappropriate content like diagnoses,
or whether it requires user follow-up. Flag if output needs attention.
""",
    model=openai_model,
    output_type=InjuryOutputCheck
)
