# AI Money Mentor

Run guide (UV + Bun).

## Backend (Python via UV)
```bash
cd backend
uv init
uv venv
source .venv/bin/activate
uv add -r requirements.txt
```

Start backend (choose one):
```bash
uv run uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload
```
or
```bash
uv run python api_server.py
```

## Frontend (Bun)
```bash
cd frontend
bun install
bunx prisma generate
bun run dev
```

## URLs
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
