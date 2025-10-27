# Action Item Extractor

A FastAPI web application that extracts action items from free-form notes using either heuristic-based pattern matching or LLM-powered extraction via Ollama.

## Project Overview

This application helps convert unstructured notes into organized action items. It supports two extraction methods:
- **Heuristic extraction**: Pattern matching for bullets, keywords, and checkboxes
- **LLM extraction**: AI-powered extraction using Ollama

## Setup and Installation

### Prerequisites
- Python 3.8+
- Poetry for dependency management
- Ollama installed locally
- Conda environment (recommended)

### Installation Steps

1. Activate your conda environment:
```bash
conda activate cs146s
```

2. Install dependencies from project root:
```bash
poetry install
```

3. Set up Ollama and pull a model:
```bash
ollama pull llama3.2
```

4. Run the server:
```bash
poetry run uvicorn week2.app.main:app --reload
```

5. Open browser to http://127.0.0.1:8000/

## API Endpoints

### Action Items
- `POST /action-items/extract` - Extract items using heuristics
- `POST /action-items/extract-llm` - Extract items using LLM
- `GET /action-items` - List all action items (optional: filter by `note_id`)
- `POST /action-items/{id}/done` - Mark item as done/undone

### Notes
- `POST /notes` - Create a new note
- `GET /notes` - List all notes
- `GET /notes/{id}` - Get a specific note

## Functionality

### Web Interface
1. Paste notes in the text area
2. Choose extraction method:
   - **Extract**: Uses heuristic pattern matching
   - **Extract LLM**: Uses AI-powered extraction
3. Check "Save as note" to store in database
4. Click **List Notes** to view all saved notes
5. Check off completed action items

### Example Input
```
Meeting notes:
- [ ] Set up database
- Implement API endpoints
TODO: Write unit tests
We need to refactor the auth module.
```

## Running Tests

Run the test suite:
```bash
poetry run pytest week2/tests/
```

Run with verbose output:
```bash
poetry run pytest week2/tests/ -v
```

## Project Structure

```
week2/
├── app/
│   ├── main.py              # FastAPI app configuration
│   ├── db.py                # Database operations
│   ├── schemas.py           # Pydantic API models
│   ├── routers/
│   │   ├── action_items.py  # Action item endpoints
│   │   └── notes.py         # Notes endpoints
│   └── services/
│       └── extract.py       # Extraction logic
├── frontend/
│   └── index.html           # Web UI
├── tests/
│   └── test_extract.py      # Unit tests
└── data/
    └── app.db               # SQLite database
```

## Technical Details

### Database Schema
- **notes**: id, content, created_at
- **action_items**: id, note_id (FK), text, done, created_at

### Extraction Methods

**Heuristic-based**: Identifies bullets (-, *, •), numbered lists, keyword prefixes (TODO:, ACTION:), checkboxes ([ ]), and imperative sentences.

**LLM-based**: Uses Ollama with structured JSON output via Pydantic models. Falls back to heuristic extraction on errors.

## Error Handling

The application includes comprehensive error handling with:
- Database connection error management
- Input validation with Pydantic schemas
- LLM extraction fallback mechanism
- HTTP error responses with proper status codes
- Logging throughout the application
