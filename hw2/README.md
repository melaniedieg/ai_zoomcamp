# TableTurn

A local restaurant waitlist manager. Built for AI Dev Tools Zoomcamp Homework 2.

## Requirements

Python 3.11+, [uv](https://docs.astral.sh/uv/), and Node.js 20+.

## Start the backend

From `hw2/backend/`:

```bash
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

SQLite data is stored in `backend/tableturn.db`. The API and Swagger docs are at http://127.0.0.1:8000/docs.

## Start the frontend

In another terminal, from `hw2/frontend/`:

```bash
npm install
npm run dev
```

Open http://127.0.0.1:5173. The frontend sends requests to `http://127.0.0.1:8000` by default. Set `VITE_API_URL` before starting Vite to use another backend.

## Tests

From `hw2/backend/`:

```bash
uv run pytest
```

From `hw2/frontend/`:

```bash
npm run build
```

## Layout

- `_docs/specs.md`: product specification and acceptance criteria
- `openapi.yaml`: frontend/backend API contract
- `frontend/`: browser interface and centralized API client
- `backend/`: FastAPI, SQLAlchemy, SQLite, and endpoint tests
- `docs/ai-usage-report.md`: AI development and verification record
