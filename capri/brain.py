from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import Any, List, Dict

from openai import OpenAI


class AIModelAdapter(ABC):
    @abstractmethod
    def generate(self, system_prompt: str, history: List[Dict[str, str]], user_message: str) -> str:
        """Return a model response for a chat turn."""


class OpenAIChatAdapter(AIModelAdapter):
    def __init__(self, api_key: str | None = None, model: str = "gpt-4o-mini") -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("CAPRI_MODEL", "gpt-4o-mini")

    def generate(self, system_prompt: str, history: List[Dict[str, str]], user_message: str) -> str:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured.")

        client = OpenAI(api_key=self.api_key)

        messages = [{"role": "system", "content": system_prompt}]
        for item in history:
            if item.get("role") in {"user", "assistant"}:
                messages.append({"role": item["role"], "content": item["content"]})
        messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.8,
            max_tokens=1000,
        )

        return response.choices[0].message.content.strip() or "Je n'ai pas de réponse à cette demande."


class DemoAdapter(AIModelAdapter):
    def generate(self, system_prompt: str, history: List[Dict[str, str]], user_message: str) -> str:
        if "fr" in user_message.lower():
            return "Bonjour ! CAPRI est prêt à aider en français et dans d'autres langues. Ajoute ta clé OpenAI pour activer la vraie intelligence.")
        return "Hello! CAPRI is ready to help. Add your OpenAI API key to activate the full AI brain."


class ModelFactory:
    @staticmethod
    def create() -> AIModelAdapter:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            return OpenAIChatAdapter(api_key=api_key, model=os.getenv("CAPRI_MODEL", "gpt-4o-mini"))
        return DemoAdapter()
