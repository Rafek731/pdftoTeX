import argparse
import logging
from pathlib import Path

from .validate_args import validate

logger = logging.getLogger(__name__)

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="totex",
        usage="totex FILE1 FILE2... "
        "[-o|--output OUTPUT] "
        "[-n|--max-parallel-files MAX_PARALLEL_FILES] "
        "[-m|--model MODEL] "
        "[-l|--language LANGUAGE]",
        description="Generates LaTeX code that will most resemble given documents.",
    )
    parser.add_argument(
        "input",
        type=Path,
        nargs="+",
        help="Files to converto to LaTeX code"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path.cwd(),
        help="Destination path to save the files. Defaults to '.'",
    )
    parser.add_argument(
        "-n",
        "--max-parallel-files",
        type=int,
        default=3
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default="gemini-3.5-flash-lite"
    )
    parser.add_argument(
        "-l",
        "--language",
        type=str,
        default="english"
    )
    parser.add_argument(
        "-a",
        "--api-key",
        type=str,
        default="",
    )
    return validate(parser.parse_args())
