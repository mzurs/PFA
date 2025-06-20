import os

from agents import AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from dotenv import load_dotenv


def model_config():
    # Load the environment variables from the .env file
    load_dotenv()

    gemini_api_key = os.getenv("GEMINI_API_KEY")

    # Check if the API key is present; if not, raise an error
    if not gemini_api_key:
        raise ValueError(
            "GEMINI_API_KEY is not set. Please ensure it is defined in your .env file."
        )

    # Reference: https://ai.google.dev/gemini-api/docs/openai
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash", openai_client=external_client
    )

    config = RunConfig(
        model=model, model_provider=external_client, tracing_disabled=True
    )

    return (config, model)


def is_valid_hex_key(key: str) -> bool:
    try:
        int(key, 16)
        return True
    except ValueError:
        return False
