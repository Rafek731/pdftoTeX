import logging
import os
from pathlib import Path

import dotenv

logger = logging.getLogger(__name__)

CONFIG_DIR = Path.home() / ".config" / "totex"
API_KEY_FILE = CONFIG_DIR / "api_key"

def save_api_key(api_key: str) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    API_KEY_FILE.write_text(api_key.strip(), "utf-8")
    logger.info("API key saved for future use")
    try:
        API_KEY_FILE.chmod(0o600)
    except OSError:
        pass


def load_api_key() -> str:
    """Loads Gemini API key from .env file into environment variable

    Raises:
        ValueError: if a key is missing from .env file or config file

    Returns:
        str: api key
    """
    dotenv.load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if api_key is None and API_KEY_FILE.is_file():
        api_key = API_KEY_FILE.read_text("utf-8")
    
    if not api_key:      
        raise ValueError("GEMINI_API_KEY is non-existent")
    
    return api_key
