# CAPRI

CAPRI is an advanced AI companion project designed to be modular, multilingual, and ready for a real AI model API.

## Features

- Modular AI brain with pluggable model adapters
- Separation between frontend and backend
- Persistent in-memory conversation context for each session
- Built for French and multilingual conversations
- Activation code: `hiro`
- Ready to integrate with OpenAI-compatible APIs

## Quick start

1. Create a Python virtual environment
2. Install dependencies
3. Set your environment variables
4. Run the app

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app:app --reload
```

Then open http://localhost:8000

## Environment variables

```env
OPENAI_API_KEY=your_key_here
CAPRI_MODEL=gpt-4o-mini
CAPRI_NAME=CAPRI
CAPRI_ACTIVATION_CODE=hiro
```

## Production note

This project is intentionally structured so the AI model can be replaced without touching the UI or chat logic. The backend uses an adapter pattern and the frontend is a standalone interface.
