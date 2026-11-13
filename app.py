from __future__ import annotations

import os
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from capri.brain import ModelFactory, MemoryStore

app = FastAPI(title="CAPRI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

memory_store = MemoryStore()
brain = ModelFactory.create()

SYSTEM_PROMPT = (
    "You are CAPRI, a highly capable AI companion. "
    "Your name is CAPRI and your activation code is hiro. "
    "Remain honest, helpful, multilingual, and clear. "
    "When you do not know something, say so instead of inventing information. "
    "Use context from previous messages, reason carefully, and answer in the user's language."
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(os.path.dirname(BASE_DIR), "web")


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    session_id: str | None = None
    activation_code: str = ""
    history: List[Dict[str, str]] = []


@app.get("/api/health")
def health_check() -> Dict[str, str]:
    return {"status": "ok", "name": os.getenv("CAPRI_NAME", "CAPRI")}


@app.post("/api/chat")
def chat(request: ChatRequest):
    if request.activation_code.strip() != os.getenv("CAPRI_ACTIVATION_CODE", "hiro"):
        raise HTTPException(status_code=401, detail="Invalid activation code.")

    session_id = request.session_id or "default"
    prior_history = memory_store.get(session_id)
    full_history = prior_history + request.history

    try:
        response = brain.generate(SYSTEM_PROMPT, full_history, request.message)
    except RuntimeError as exc:
        response = (
            "CAPRI is ready, but the model API has not been configured yet. "
            "Set OPENAI_API_KEY in your environment to activate the full AI brain."
        )

    memory_store.add_turn(session_id, "user", request.message)
    memory_store.add_turn(session_id, "assistant", response)

    return {"reply": response, "session_id": session_id}


@app.get("/")
def serve_index():
    return FileResponse(os.path.join(WEB_DIR, "index.html"))


app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")
