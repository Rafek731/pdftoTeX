import os

import dotenv


def load_api_key() -> str:
    """Loads Gemini API key from .env file into environment variable

    Raises:
        ValueError: if a key is missing from .env file

    Returns:
        str: api key
    """
    dotenv.load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key is None:
        raise ValueError("GEMINI_API_KEY is non-existent")
    return api_key
