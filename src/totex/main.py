import asyncio
import logging
from pathlib import Path

from google import genai

from totex.AsyncTeXConverter import AsyncTeXConverter
from totex.utils import cli

logger = logging.getLogger(__name__)

async def run_program():
    logger.info("Setting up...")    
    args = cli.parse_arguments()
    API_KEY = args.api_key
    client = genai.Client(api_key=API_KEY)
    PROMTPS_DIR = Path(__file__).parent.parent / "prompts"
    prompt = (PROMTPS_DIR / "prompt.txt").read_text("utf-8")
    prompt = prompt.replace("@LANGUAGE", args.language)
    system_prompt = (PROMTPS_DIR / "system_prompt.txt").read_text("utf-8")
    
    converter = AsyncTeXConverter(
        client, 
        args.model,
        prompt,
        system_prompt,
        args.max_parallel_files
    )
    logger.info("Done")

    logger.info("\nStarting conversion...")
    await converter.convert_batch(args.input, args.output)
    logger.info("Done")

def main():
    asyncio.run(run_program())