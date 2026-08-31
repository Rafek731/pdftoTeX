import asyncio
import logging

from google import genai

from totex.AsyncTeXConverter import AsyncTeXConverter
from totex.utils import cli, load_api_key
from totex.utils.configure import PROMPT_DIR, configure

logger = logging.getLogger(__name__)

async def run_program():
    logger.info("Setting up...")    
    args = cli.parse_arguments()
    configure(api_key=args.api_key)

    API_KEY = load_api_key()

    client = genai.Client(api_key=API_KEY)

    prompt = (PROMPT_DIR / "prompt.txt").read_text("utf-8")
    prompt = prompt.replace("@LANGUAGE", args.language)
    system_prompt = (PROMPT_DIR / "system_prompt.txt").read_text("utf-8")
    
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