---
description: Run pytest with optional marker/path, then coverage if tests pass
allowedTools:
  - Bash
  - Read
headless: true
---

# Test Runner with Coverage

You are a test automation specialist. Your task is to run tests and optionally generate coverage reports.

## Steps to Execute

1. **Parse Arguments**: Check if `$ARGUMENTS` is provided:
   - If empty: Run all tests in `week4/backend/tests`
   - If provided: Use as marker (e.g., `-m slow`) or path (e.g., `backend/tests/test_notes.py`)

2. **Run Tests**:
   - Change to `week4/` directory
   - Execute: `pytest -q backend/tests $ARGUMENTS --maxfail=1 -x`
   - The `-q` flag provides quiet output
   - The `--maxfail=1 -x` flags stop on first failure

3. **Analyze Results**:
   - If tests fail:
     - Summarize the failure(s)
     - Suggest next steps (e.g., "Fix the failing assertion in test_create_note")
     - Stop here (do NOT run coverage)
   - If all tests pass:
     - Proceed to step 4

4. **Run Coverage** (only if tests passed):
   - First check if pytest-cov is installed
   - If not installed, inform the user that coverage is skipped (requires `pip install pytest-cov`)
   - If installed, execute: `pytest backend/tests $ARGUMENTS --cov=backend/app --cov-report=term-missing`
   - Show coverage percentage for each module
   - Highlight any files with <80% coverage

5. **Summary Output**:
   - Provide a concise summary:
     - Number of tests passed/failed
     - If passed: Coverage percentages
     - If failed: What to fix next
     - Files with low coverage (if any)

## Safety Notes
- This command only reads and runs tests, it does not modify code
- The `--maxfail=1 -x` ensures we fail fast
- Coverage is only run if tests pass to save time

## Example Usage
```
/tests
/tests -m integration
/tests backend/tests/test_notes.py
```
