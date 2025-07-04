import streamlit as st
import asyncio
import json
from agents import Runner
from health_agent import health_agent
from config import config

st.title("Health & Wellness Planner Agent")

st.markdown(
    """
    **Tip:** For best results, include a clear goal and your preferences in your prompt.
    - Example: `"I want to lose 5kg in 2 months. I prefer a vegetarian diet and low-impact workouts."`
    - Example: `"Help me gain muscle in 3 months. I have a nut allergy."`
    """
)

sample_prompts = [
    "I want to lose 5kg in 2 months. Give me a 7-day meal plan and fitness schedule for a busy office worker.",
    "I want to gain 3kg in 3 months. I prefer a high-protein vegetarian diet.",
    "I want to lose 4kg in 1 month. I have a knee injury. Suggest safe exercises and a healthy meal plan for weight loss.",
    "I want to maintain my weight in 6 months. Create a balanced diet and workout plan for managing diabetes.",
    "I want to lose 3kg in 1 month. I want a gluten-free meal plan and low-impact workouts."
]

selected_prompt = st.selectbox(
    "Or select a sample prompt for quick response:",
    options=sample_prompts
)

user_input = st.text_area(
    "Enter your health goal and preferences:",
    selected_prompt
)

def try_parse_json(text):
    try:
        return json.loads(text)
    except Exception:
        return None

if st.button("Get Plan"):
    async def get_response():
        try:
            result = Runner.run_streamed(
                health_agent,
                input=user_input,
                context=None,
                run_config=config
            )
            output = ""
            async for event in result.stream_events():
                delta = getattr(getattr(event, "data", None), "delta", None)
                if delta is not None:
                    output += delta
            return output, None
        except Exception as e:
            # Return the error message for display
            return None, str(e)

    response, error = asyncio.run(get_response())

    if error:
        if "Guardrail InputGuardrail triggered tripwire" in error:
            st.error(
                "⚠️ Your input was rejected by the system's safety checks.\n\n"
                "Please make sure your prompt includes a clear health-related goal (e.g., 'I want to lose 5kg in 2 months.')."
            )
        else:
            st.error(f"⚠️ {error}")
    elif response:
        # Try to parse as JSON/dict for structured output
        parsed = try_parse_json(response)
        if parsed and isinstance(parsed, dict):
            if parsed.get("notes"):
                st.info(parsed["notes"])
            if parsed.get("meal_plan"):
                st.subheader("Meal Plan")
                for meal in parsed["meal_plan"]:
                    st.markdown(f"- {meal}")
            if parsed.get("workout_plan"):
                st.subheader("Workout Plan")
                for workout in parsed["workout_plan"]:
                    st.markdown(f"- {workout}")
        else:
            # Fallback: just display as markdown
            st.markdown(response)