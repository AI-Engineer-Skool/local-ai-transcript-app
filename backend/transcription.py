#!/usr/bin/env python3
"""
Uses OpenAI API format, compatible with Ollama, OpenAI, LM Studio, and other providers.
Configuration is loaded from .env file.
"""

import json
from pathlib import Path

from faster_whisper import WhisperModel
from openai import OpenAI

# Edit system_prompt.txt to change how the LLM cleans transcriptions
PROMPT_FILE = Path(__file__).parent / "system_prompt.txt"
SYSTEM_PROMPT = PROMPT_FILE.read_text().strip()

# Used to recognise an Ollama server, so we can print the exact download command
OLLAMA_DEFAULT_PORT = "11434"
MAX_MODELS_SHOWN = 10


class TranscriptionService:
    """Uses OpenAI-compatible API, works with any provider (Ollama, OpenAI, LM Studio, etc.)."""

    def __init__(
        self, whisper_model: str, llm_base_url: str, llm_api_key: str, llm_model: str
    ):
        print(f"🔄 Loading Whisper model '{whisper_model}'...")
        self.whisper = WhisperModel(
            whisper_model,
            device="auto",  # Auto-detect: Metal (Mac), CUDA (NVIDIA), or CPU
            compute_type="int8",
        )
        print(f"✅ Whisper model '{whisper_model}' loaded!")

        print(f"🔄 Connecting to LLM at {llm_base_url}...")
        self.llm_client = OpenAI(base_url=llm_base_url, api_key=llm_api_key)
        self.llm_base_url = llm_base_url
        self.llm_model = llm_model

        if self.check_llm_model():
            print(f"✅ Connected to LLM API, model '{llm_model}' is available!")

    def check_llm_model(self) -> bool:
        """Return True if the LLM server has LLM_MODEL; otherwise print how to fix it.

        Being able to reach the server isn't enough: a model that was never
        downloaded only shows up later, as a 404 on the first cleaning request.
        """
        try:
            available_models = sorted(
                model.id for model in self.llm_client.models.list()
            )
        except Exception as e:
            print(f"⚠️  Warning: Could not connect to LLM: {e}")
            print(f"   Make sure your LLM server is running at {self.llm_base_url}")
            return False

        # Ollama treats a name without a tag ("gemma3") as "gemma3:latest"
        if {self.llm_model, f"{self.llm_model}:latest"} & set(available_models):
            return True

        shown = ", ".join(available_models[:MAX_MODELS_SHOWN]) or "none yet"
        if len(available_models) > MAX_MODELS_SHOWN:
            shown += ", ..."
        print(f"⚠️  Warning: The LLM server has no model named '{self.llm_model}'")
        print(f"   Models it has: {shown}")
        if OLLAMA_DEFAULT_PORT in self.llm_base_url:
            ollama_url = self.llm_base_url.rstrip("/").removesuffix("/v1")
            pull_request = json.dumps({"model": self.llm_model})
            print(f"   Download it:   curl {ollama_url}/api/pull -d '{pull_request}'")
        print("   Or set LLM_MODEL in backend/.env to a model the server has.")
        return False

    def transcribe(self, audio_file):
        print("🔄 Transcribing...")

        segments, info = self.whisper.transcribe(
            audio_file, beam_size=5, language="en", condition_on_previous_text=False
        )

        text = " ".join([segment.text for segment in segments]).strip()
        print(f"📝 Raw: {text}")
        return text

    def get_default_system_prompt(self):
        return SYSTEM_PROMPT

    def clean_with_llm(self, text, system_prompt=None):
        if not text:
            return ""

        # Use custom prompt or fall back to default
        prompt_to_use = system_prompt if system_prompt else SYSTEM_PROMPT

        print("🤖 Cleaning with LLM...")

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

    def transcribe_file(self, audio_file_path: str, use_llm: bool = True) -> dict:
        raw_text = self.transcribe(audio_file_path)

        result = {"raw_text": raw_text}

        if use_llm and raw_text:
            cleaned_text = self.clean_with_llm(raw_text)
            result["cleaned_text"] = cleaned_text
        else:
            result["cleaned_text"] = raw_text

        return result
