import os

from src.chatbot.prompts import ANALYST_SYSTEM_PROMPT, build_analyst_prompt


DEFAULT_OPENAI_MODEL = "gpt-4.1-mini"


def is_openai_available():
    return bool(os.getenv("OPENAI_API_KEY")) and _get_openai_client_class() is not None


def generate_ai_summary(question, analytics_context, fallback_text, model=DEFAULT_OPENAI_MODEL):
    """Use OpenAI to polish a computed cricket insight when configured."""
    client_class = _get_openai_client_class()

    if not os.getenv("OPENAI_API_KEY") or client_class is None:
        return fallback_text

    try:
        client = client_class()
        response = client.responses.create(
            model=model,
            instructions=ANALYST_SYSTEM_PROMPT,
            input=build_analyst_prompt(question, analytics_context),
            max_output_tokens=450,
        )
        return response.output_text.strip()
    except Exception:
        return fallback_text


def _get_openai_client_class():
    try:
        from openai import OpenAI

        return OpenAI
    except ImportError:
        return None
