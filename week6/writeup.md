# Week 6 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: Zara Rutherford
SUNet ID: 06625318
Citations: Claude code and semgrep docs

This assignment took me about 1 hour to do. 


## Brief findings overview
Semgrep found 6 issues in the codebase: SQL injection, XSS, insecure CORS, and three vulnerable debug endpoints (eval, subprocess with shell=True, dynamic urllib). I fixed the first three since they affect the main application. 

## Fix #1
a. File and line(s)
backend/app/routers/notes.py:71-79

b. Rule/category Semgrep flagged
python.sqlalchemy.security.audit.avoid-sqlalchemy-text.avoid-sqlalchemy-text

c. Brief risk description
The search function builds SQL queries using f-strings, which lets attackers inject arbitrary SQL commands. Someone could search for `' OR '1'='1` and dump the whole database or worse.

d. Your change (short code diff or explanation, AI coding tool usage)
Changed from `f"WHERE title LIKE '%{q}%'"` to parameterized query using `WHERE title LIKE :pattern` and passing `{"pattern": f"%{q}%"}` to execute(). Used Claude Code to make the fix.

e. Why this mitigates the issue
SQLAlchemy handles the parameter binding and escaping automatically, so user input can't be interpreted as SQL code anymore.

## Fix #2
a. File and line(s)
frontend/app.js:14

b. Rule/category Semgrep flagged
javascript.browser.security.insecure-document-method.insecure-document-method

c. Brief risk description
Using innerHTML with user-controlled data means if someone creates a note with `<script>alert('xss')</script>` as the title, it executes when the page loads. This could steal session tokens or do anything the user can do.

d. Your change (short code diff or explanation, AI coding tool usage)
Replaced `li.innerHTML = '<strong>${n.title}</strong>: ${n.content}'` with createElement('strong'), textContent assignments, and appendChild() calls. Used Claude Code for the refactor.

e. Why this mitigates the issue
textContent treats everything as plain text instead of HTML, so script tags just show up as literal text instead of running.

## Fix #3
a. File and line(s)
backend/app/main.py:24

b. Rule/category Semgrep flagged
python.fastapi.security.wildcard-cors.wildcard-cors

c. Brief risk description
Having `allow_origins=["*"]` with `allow_credentials=True` means any website can make authenticated requests to the API. A malicious site could trick users into making requests that change or delete their data.

d. Your change (short code diff or explanation, AI coding tool usage)
Changed `allow_origins=["*"]` to `allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"]`. Used Claude Code for the change.

e. Why this mitigates the issue
Now only the local development server can make credentialed requests, so random websites can't abuse the API on behalf of logged-in users.
