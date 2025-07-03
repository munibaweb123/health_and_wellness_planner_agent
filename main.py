from config import config
from agents import Runner

from health_agent import health_agent  # Import the agent instance

if __name__ == "__main__":
    result = Runner.run_sync(
        health_agent,  # Now this is the agent instance
        "I want to lose 5kg in 2 months and improve my fitness. I prefer a balanced diet and regular exercise. Can you help me create a personalized health and wellness plan?",
        run_config=config
    )
    print(result.final_output)