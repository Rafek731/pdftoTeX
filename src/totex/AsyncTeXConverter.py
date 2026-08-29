import asyncio
import logging
from dataclasses import dataclass
from pathlib import Path

from google import genai
from google.genai.errors import APIError

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AsyncTeXConverter:
    """Asynchronous converter transforming documents and images into LaTeX code using Gemini models.

    Attributes:
        client: An instance of `genai.Client` for communicating with the Gemini API.
        model: The model variant (e.g., gemini-3.1-pro) to be used for generation.
        max_parallel_files: Maximum number of concurrent requests sent to the API.
        prompt: User prompt content.
        system_prompt: System prompt instructions.
    """

    client: genai.Client
    model: str
    prompt: str
    system_prompt: str
    max_parallel_files: int = 3

    async def convert_single(
        self, filepath: Path, output_path: Path, semaphore: asyncio.Semaphore
    ) -> Path | None:
        """Convert a single local file to LaTeX within the given concurrency limit.

        Args:
            filepath: Path to the source file to process.
            output_path: Target path where the generated .tex file will be saved.
            semaphore: Concurrency limiter shared across conversion tasks.

        Returns:
            The Path to the saved file if successful, or None if conversion failed.
        """
        async with semaphore:
            logger.info(f"Processing file '{filepath.name}' with model '{self.model}'")
            try:
                latex_code = await self.ask_llm(filepath)
                saved_path = self._save(latex_code, output_path)
                logger.info(f"Successfully saved output to '{saved_path.name}'")
                return saved_path
            except (APIError, FileNotFoundError, RuntimeError) as exc:
                logger.error(f"Failed to generate LaTeX for '{filepath.name}': {exc}")
                return None
            except OSError as exc:
                logger.error(f"Failed to save output for '{filepath.name}' to '{output_path}': {exc}")
                return None
            except Exception as exc:
                logger.error(f"Unexpected error during conversion of '{filepath.name}': {exc}", exc_info=exc)
                return None
        

    async def convert_batch(self, files: list[Path], output_dir: Path) -> list[Path]:
        """Convert a collection of files asynchronously in parallel.

        Args:
            files: List of file paths to be converted.
            output_dir: Destination directory for all output .tex files.

        Returns:
            List of Paths pointing to successfully converted and saved .tex files.
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        semaphore = asyncio.Semaphore(self.max_parallel_files)

        tasks = [
            self.convert_single(file, output_dir / f"{file.stem}.tex", semaphore)
            for file in files
        ]

        results = await asyncio.gather(*tasks)
        return [path for path in results if path is not None]

    @staticmethod
    def clear_response(code: str) -> str:
        return code.removeprefix("```").removeprefix("latex").removesuffix("```")


    async def ask_llm(self, filepath: Path) -> str:
        """Upload a local file, request LaTeX transcription from Gemini, and delete the remote asset.

        Args:
            filepath: Path to the local file (e.g., PDF or image).

        Returns:
            Sanitized LaTeX code extracted from the model's response.

        Raises:
            FileNotFoundError: If the source file does not exist on disk.
            APIError: If the upload or generation request fails via Gemini API.
            RuntimeError: If the model returns an empty payload or missing candidate text.
        """
        if not filepath.is_file():
            raise FileNotFoundError(f"Source file not found: {filepath.resolve()}")

        try:
            uploaded_file = await self.client.aio.files.upload(
                file=filepath,
                config={"display_name": filepath.stem},
            )
        except APIError:
            raise
        except Exception as exc:
            raise RuntimeError(f"Failed to upload '{filepath.name}' to Gemini Files API: {exc}") from exc

        if not uploaded_file.name:
            raise RuntimeError(f"Upload succeeded but received no file identifier for '{filepath.name}'.")

        try:
            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=[uploaded_file, self.prompt],
                config={
                    "system_instruction": self.system_prompt,
                    "temperature": 0.1,
                },
            )

            if not response.text:
                raise RuntimeError(f"Model returned an empty response for '{filepath.name}'.")

            return self.clear_response(response.text)

        finally:
            try:
                await self.client.aio.files.delete(name=uploaded_file.name)
            except Exception as cleanup_err:
                logger.warning(f"Failed to delete remote file '{uploaded_file.name}' ({filepath.name}): {cleanup_err}")


    @staticmethod
    def _save(code: str, output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(code, "utf-8")
        return output_path
