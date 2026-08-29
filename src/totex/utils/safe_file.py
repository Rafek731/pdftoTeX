from pathlib import Path
from tempfile import TemporaryDirectory

import anyascii

_TMP_DIR = TemporaryDirectory()
TMP_PATH = Path(_TMP_DIR.name)

def make_safe(file: Path) -> Path:
    """Copy file to temporary directory with safe ASCII name"""
    safe_name = anyascii.anyascii(file.name).replace(" ", "_")
    if not safe_name:
        safe_name = f"doc_{file.suffix}"

    tmp_file = TMP_PATH / safe_name
    file.copy(tmp_file)
    
    return tmp_file
