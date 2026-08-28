import argparse
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

DEFAULT_PROMPT_DIR = Path(__file__).parent.parent.parent / "prompts"

class Validator:

    @staticmethod
    def language(args: argparse.Namespace) -> argparse.Namespace:
        return args

    @staticmethod
    def input(args: argparse.Namespace) -> argparse.Namespace:
        valid_files: list[Path] = []
        for file in args.input:
            if not file.is_file():
                logger.warning(f"File {file} does not exist - skipping")
                continue
            valid_files.append(file)

        if not valid_files:
            raise ValueError("No input files were given")

        args.input = valid_files
        return args

    @staticmethod
    def output(args: argparse.Namespace) -> argparse.Namespace:
        if not (args.output.is_dir() or args.output.is_file()):
            raise ValueError("Invlid file(s) destination")
        return args

    @staticmethod
    def model(args: argparse.Namespace) -> argparse.Namespace:
        return args

    @staticmethod
    def max_parallel_files(args: argparse.Namespace) -> argparse.Namespace:
        args.max_parallel_files = max(1, args.max_parallel_files)
        return args

def validate(args: argparse.Namespace) -> argparse.Namespace:
    args = Validator.language(args)
    args = Validator.input(args)
    args = Validator.output(args)
    args = Validator.model(args)
    args = Validator.max_parallel_files(args)
    
    return args
