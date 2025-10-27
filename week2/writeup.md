# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: Zara Rutherford
SUNet ID: 06625318
Citations: Claude

This assignment took me about 2 hours to do. 


## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt:
```
Add a new function extract_action_items_llm() to the extract.py file that uses Ollama to extract action items from text. Use structured outputs with a Pydantic model to get a JSON array of action items. Include error handling that falls back to the heuristic extraction if the LLM fails.
```

Generated Code Snippets:
```
week2/app/services/extract.py:
- Lines 10: Added Pydantic import
- Lines 93-151: Added ActionItems Pydantic model and extract_action_items_llm() function with Ollama integration
```

### Exercise 2: Add Unit Tests
Prompt:
```
Write comprehensive unit tests for extract_action_items_llm() in test_extract.py. Cover multiple scenarios including bullet lists, keyword-prefixed lines (TODO, ACTION), empty input, narrative text with implicit action items, mixed formatting styles, and deduplication of similar items.
```

Generated Code Snippets:
```
week2/tests/test_extract.py:
- Line 4: Added import for extract_action_items_llm
- Lines 22-102: Added 6 unit tests covering various input formats and edge cases for LLM extraction
```

### Exercise 3: Refactor Existing Code for Clarity
Prompt:
```
Refactor the backend code for better clarity. Create a schemas.py file with Pydantic models for all API requests and responses. Add comprehensive error handling and logging throughout the database layer. Update all router endpoints to use the new schemas and add proper error handling. Improve the main.py app lifecycle with a lifespan context manager and better configuration.
```

Generated/Modified Code Snippets:
```
week2/app/schemas.py (new file):
- Lines 1-60: Created Pydantic models for API contracts (ExtractRequest, NoteCreateRequest, MarkDoneRequest, ActionItemResponse, NoteResponse, ExtractResponse, etc.)

week2/app/db.py:
- Lines 1-10: Added logging configuration and imports
- Lines 17-45: Enhanced error handling in ensure_data_directory_exists(), get_connection() with logging
- Lines 48-86: Added comprehensive docstrings and error handling to init_db()
- Lines 89-247: Added detailed docstrings, logging, and try-catch error handling to all database functions (insert_note, list_notes, get_note, insert_action_items, list_action_items, mark_action_item_done)

week2/app/routers/action_items.py:
- Lines 1-17: Added logging, sqlite3 error handling imports, and schema imports
- Lines 24-63: Refactored extract() endpoint to use Pydantic schemas with proper error handling
- Lines 66-94: Refactored list_all() endpoint with schemas and error handling
- Lines 97-117: Refactored mark_done() endpoint with schemas and error handling

week2/app/routers/notes.py:
- Lines 1-12: Added logging, error handling imports, and schema imports
- Lines 17-43: Refactored create_note() endpoint to use Pydantic schemas with comprehensive error handling
- Lines 46-71: Refactored get_single_note() endpoint with schemas and error handling

week2/app/main.py:
- Lines 5-20: Added logging configuration and asynccontextmanager import
- Lines 23-41: Created lifespan context manager for proper app startup/shutdown
- Lines 44-49: Enhanced FastAPI app initialization with better metadata
- Lines 52-71: Added error handling to index() route
```


### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt:
```
Add a new endpoint /action-items/extract-llm that uses the extract_action_items_llm() function. Add an "Extract LLM" button to the frontend that calls this new endpoint. Also add a GET /notes endpoint to retrieve all notes and add a "List Notes" button to the frontend that displays all saved notes with their content and timestamps.
```

Generated Code Snippets:
```
week2/app/routers/action_items.py:
- Line 11: Added import for extract_action_items_llm
- Lines 66-106: Added new /extract-llm POST endpoint that uses LLM extraction

week2/app/routers/notes.py:
- Lines 74-98: Added new GET /notes endpoint to list all notes

week2/frontend/index.html:
- Line 28: Added "Extract LLM" button
- Line 30: Added "List Notes" button
- Line 35: Added notes display area div
- Lines 72-107: Added JavaScript event handler for Extract LLM button
- Lines 113-136: Added JavaScript event handler for List Notes button with note display formatting
```


### Exercise 5: Generate a README from the Codebase
Prompt:
```
Analyze the codebase and generate a comprehensive README.md file. Include a project overview, setup and installation instructions, API endpoints documentation, functionality description, instructions for running tests, project structure, and technical details about the database schema and extraction methods.
```

Generated Code Snippets:
```
week2/README.md (new file):
- Lines 1-118: Complete README with project overview, setup instructions, API documentation, usage guide, testing instructions, project structure diagram, and technical implementation details
```


## SUBMISSION INSTRUCTIONS
1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields. 
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope. 