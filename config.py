from agents import OpenAIChatCompletionsModel, RunConfig
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

external_client = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

openai_model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model="gemini-2.0-flash",
)

config = RunConfig(
    model=openai_model,
    tracing_disabled=True,
    model_provider=external_client
)