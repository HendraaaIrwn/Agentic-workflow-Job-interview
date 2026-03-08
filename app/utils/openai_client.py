import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


DEFAULT_MODEL = os.getenv("OPENAI_DEFAULT_MODEL", "gpt-5-mini")
REPORT_MODEL = os.getenv("OPENAI_REPORT_MODEL", DEFAULT_MODEL)


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    return OpenAI(api_key=api_key)


openai_client: OpenAI = get_openai_client()
