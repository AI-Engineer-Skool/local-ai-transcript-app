#!/usr/bin/env python3
"""
Transcription service using Whisper + PydanticAI agent.

This version uses PydanticAI for type-safe, validated LLM interactions
instead of raw OpenAI function calling.
"""

from pathlib import Path

from faster_whisper import WhisperModel
from openai import OpenAI

from agent import process_transcript

PROMPT_FILE = Path(__file__).parent / "system_prompt.txt"
SYSTEM_PROMPT = PROMPT_FILE.read_text().strip()


class TranscriptionService:
    """Transcription service using Whisper + PydanticAI agent."""

    def __init__(
        self, whisper_model: str, llm_base_url: str, llm_api_key: str, llm_model: str
    ):
        print(f"🔄 Loading Whisper model '{whisper_model}'...")
        self.whisper = WhisperModel(
            whisper_model,
            device="auto",
            compute_type="int8",
        )
        print(f"✅ Whisper model '{whisper_model}' loaded!")

        print(f"🔄 Connecting to LLM at {llm_base_url}...")
        print(f"    Using model: {llm_model}")

        # Keep OpenAI client for simple LLM cleaning (non-agentic)
        self.llm_client = OpenAI(base_url=llm_base_url, api_key=llm_api_key)
        self.llm_model = llm_model

        try:
            # Skip model listing for OpenRouter (not supported)
            if "openrouter.ai" not in llm_base_url:
                self.llm_client.models.list()
            print("✅ Connected to LLM API!")
        except Exception as e:
            print(f"⚠️  Warning: Could not connect to LLM: {e}")
            print(f"   Make sure your LLM server is running at {llm_base_url}")

        # PydanticAI agent is initialized lazily in agent.py
        print("🤖 PydanticAI agent ready (lazy initialization)")
        print("✅ Service ready!\n")

    def transcribe(self, audio_file):
        """Transcribe audio to text using Whisper."""
        print("🔄 Transcribing...")

        segments, _info = self.whisper.transcribe(
            audio_file, beam_size=5, language="en", condition_on_previous_text=False
        )

        text = " ".join([segment.text for segment in segments]).strip()
        print(f"📝 Raw: {text}")
        return text

    def get_default_system_prompt(self):
        """Get the default system prompt for text cleaning."""
        return SYSTEM_PROMPT

    async def process_with_agent(self, text: str) -> dict:
        """Process transcript using PydanticAI agent.

        This is now async because PydanticAI uses async/await.
        The agent automatically:
        - Analyzes the transcript
        - Selects appropriate tools
        - Validates inputs with Pydantic models
        - Executes tools and generates summary
        """
        return await process_transcript(text)

    def clean_with_llm(self, text, system_prompt=None):
        """Simple LLM cleaning (non-agentic, for basic transcript cleanup)."""
        if not text:
            return ""

        prompt_to_use = system_prompt if system_prompt else SYSTEM_PROMPT

        print("🤖 Cleaning with LLM...")

        try:
            response = self.llm_client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": prompt_to_use},
                    {"role": "user", "content": text},
                ],
                temperature=0.3,
                max_tokens=200,
            )

            cleaned = response.choices[0].message.content.strip()
            print(f"✨ Cleaned: {cleaned}")
            return cleaned

        except Exception as e:
            print(f"⚠️  LLM error: {e}")
            return text

    def transcribe_file(self, audio_file_path: str, use_llm: bool = True) -> dict:
        """Transcribe audio file and optionally clean with LLM."""
        raw_text = self.transcribe(audio_file_path)

        result = {"raw_text": raw_text}

        if use_llm and raw_text:
            cleaned_text = self.clean_with_llm(raw_text)
            result["cleaned_text"] = cleaned_text
        else:
            result["cleaned_text"] = raw_text

        return result
