from pathlib import Path

from .api_key import save_api_key

CONFIG_DIR = Path.home() / ".config" / "totex"
PROMPT_PATH = CONFIG_DIR / "prompt.txt"
SYSTEM_PROMPT_PATH = CONFIG_DIR / "system_prompt.txt"

def configure(api_key: str|None = None) -> None:
    api_key_cfg_file = CONFIG_DIR / "api_key"
    prompt_cfg_file = CONFIG_DIR / "prompt.txt"
    system_prompt_cfg_file = CONFIG_DIR / "system_prompt.txt"

    api_key_cfg_file.touch()
    prompt_cfg_file.touch()
    system_prompt_cfg_file.touch()

    prompt_content = prompt_cfg_file.read_text("utf-8")
    system_prompt_content = system_prompt_cfg_file.read_text("utf-8")

    if not prompt_content or prompt_content.isspace():
        PROMPT_PATH.copy(prompt_cfg_file) 

    if not system_prompt_content or prompt_content.isspace():
        SYSTEM_PROMPT_PATH.copy(system_prompt_cfg_file)

    save_api_key(api_key)
    