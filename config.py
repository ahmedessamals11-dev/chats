import os
from dotenv import load_dotenv

# Loads variables from a local .env file if present.
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

if not OPENROUTER_API_KEY:
    raise RuntimeError(
        "OPENROUTER_API_KEY is not set.\n\n"
        "1) Copy .env.example to .env\n"
        "2) Put your OpenRouter API key in it\n"
        "3) Re-run the app\n\n"
        "Never hardcode API keys directly in source files."
    )
