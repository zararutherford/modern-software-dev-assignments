# Claude Code Guidance for Week 4 Starter Application

## Project Overview
This is a minimal full-stack "developer's command center" with:
- **Backend**: FastAPI with SQLite (SQLAlchemy ORM)
- **Frontend**: Static HTML/CSS/JS served by FastAPI
- **Testing**: pytest
- **Code Quality**: pre-commit hooks (black, ruff)

## Project Structure
```
week4/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app entry point
│   │   ├── db.py            # Database setup and seeding
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── routers/         # API route handlers
│   │   │   ├── notes.py
│   │   │   └── action_items.py
│   │   └── services/        # Business logic
│   │       └── extract.py   # Note extraction logic
│   └── tests/               # pytest tests
│       ├── conftest.py      # Test fixtures
│       ├── test_notes.py
│       ├── test_action_items.py
│       └── test_extract.py
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── styles.css
├── data/
│   ├── seed.sql             # Initial database data
│   └── app.db               # SQLite database (generated)
└── docs/
    └── TASKS.md             # Development tasks
```

## How to Run

### Start the application
```bash
cd week4/
make run
```
- Frontend: http://localhost:8000
- API docs: http://localhost:8000/docs
- OpenAPI schema: http://localhost:8000/openapi.json

### Run tests
```bash
cd week4/
make test
```

### Format and lint
```bash
make format  # Auto-format with black and ruff --fix
make lint    # Check with ruff (no auto-fix)
```

### Pre-commit hooks
```bash
pre-commit install           # Install hooks
pre-commit run --all-files   # Run on all files
```

## Code Style and Safety Guardrails

### Required Tools
Code must pass black (line length 88) and ruff checks before committing. Run `make format` and `make lint` before any commit.

### Safe Commands
Use these freely: `make run`, `make test`, `make format`, `make lint`, `pytest backend/tests -v`, `pytest backend/tests --cov=backend/app`, and general file reading/exploration.

### Commands to Avoid
Do not use: `rm -rf data/app.db` (destroys database), `DROP TABLE` SQL commands (data loss), direct `.git/` directory modification, or package installation without confirmation.

## Development Workflow

### When adding a new API endpoint:
Write failing test first in `backend/tests/test_*.py`, implement endpoint in appropriate router under `backend/app/routers/*.py`, update schemas in `backend/app/schemas.py` if needed, run `make test`, then `make format` and `make lint`. Test manually at http://localhost:8000/docs.

### When adding a new model:
Define model in `backend/app/models.py` (SQLAlchemy), define schema in `backend/app/schemas.py` (Pydantic), update seed data in `data/seed.sql` if needed, delete old DB with `rm data/app.db` (recreated on startup), write tests for new model operations, run full test suite with `make test`.

### When refactoring:
Ensure all tests pass first with `make test`, make incremental changes, run tests after each change, format and lint with `make format && make lint`, verify application still runs with `make run`.

## Database Information
SQLite database at `data/app.db` with automatic seeding on startup if empty (see `backend/app/db.py`). Seed data in `data/seed.sql`. Models defined in `backend/app/models.py`: Note (id, title, content, created_at) and ActionItem (id, task, completed, created_at).

## Current API Endpoints

### Notes
- `GET /notes` - List all notes
- `POST /notes` - Create a new note
- `GET /notes/{id}` - Get a specific note

### Action Items
- `GET /action-items` - List all action items
- `POST /action-items` - Create a new action item
- `GET /action-items/{id}` - Get a specific action item

## Testing Expectations
Tests in `backend/tests/` with fixtures in `conftest.py`. Aim for >80% coverage on new code. Run with coverage: `pytest backend/tests --cov=backend/app --cov-report=term-missing`

## Outstanding Tasks
See `docs/TASKS.md` for planned enhancements including search endpoint for notes, complete action item flow, improved extraction logic, CRUD enhancements, request validation, and API documentation.

## Custom Slash Commands
`/tests [marker|path]` - Run tests with optional coverage report

## Tips
Always run from `week4/` directory for Make commands. Set `PYTHONPATH=.` when running pytest/uvicorn directly. Pre-commit hooks auto-format on commit. FastAPI auto-reloads on file changes when using `make run`. Use `/docs` endpoint to test API changes interactively.
