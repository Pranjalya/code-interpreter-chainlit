import os
from dotenv import load_dotenv

api_keys = {"openai": "OPENAI_API_KEY", "huggingface": "HF_API_KEY"}


def load_env_variables(tool="openai"):
    load_dotenv()
    api_key = os.getenv(api_keys[tool])
    if not api_key:
        raise ValueError(f"{api_keys[tool]} not found in environment variables.")
    return api_key
