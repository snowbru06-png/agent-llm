# Agent LLM – Starter Repo (FastAPI + Mémoire + Outils)

Agent autonome (plan → acte → observe) avec mémoire et outils. Convient pour POC et mise en prod légère.

## Démarrer en local
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

### Endpoint
- `POST /chat` → `{ "user_id", "session_id", "message" }`

### Docker
```bash
docker compose up --build
```
