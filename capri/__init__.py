from __future__ import annotations

from collections import defaultdict, deque
from typing import Deque, Dict, List, Optional


class ConversationMemory:
    def __init__(self, max_turns: int = 12):
        self.max_turns = max_turns
        self._history: Deque[Dict[str, str]] = deque(maxlen=max_turns)

    def add(self, role: str, content: str) -> None:
        self._history.append({"role": role, "content": content})

    def snapshot(self) -> List[Dict[str, str]]:
        return list(self._history)

    def clear(self) -> None:
        self._history.clear()


class MemoryStore:
    def __init__(self):
        self._sessions: Dict[str, ConversationMemory] = defaultdict(ConversationMemory)

    def get_or_create(self, session_id: str) -> ConversationMemory:
        return self._sessions[session_id]

    def get(self, session_id: Optional[str]) -> List[Dict[str, str]]:
        if not session_id:
            return []
        return self._sessions.get(session_id, ConversationMemory()).snapshot()

    def add_turn(self, session_id: str, role: str, content: str) -> None:
        self.get_or_create(session_id).add(role, content)
