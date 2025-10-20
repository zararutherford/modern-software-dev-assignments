# Week 4 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: Zara Rutherford
SUNet ID: 06625318
Citations: https://www.anthropic.com/engineering/claude-code-best-practices
docs.anthropic.com/en/docs/claude-code/sub-agents
Claude for extra detail in CLAUDE.md

This assignment took me about 2 hours to do. 


## YOUR RESPONSES
### Automation #1

a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
The Claude Code best practices article recommends creating focused slash commands for repeated workflows. This command implements that pattern by combining test execution with coverage analysis. The fail-fast approach using `--maxfail=1 -x` stops immediately on errors to save time during development.

b. Design of each automation, including goals, inputs/outputs, steps
This automation streamlines running pytest and generating coverage reports. It accepts optional arguments for test markers or specific paths (defaulting to all tests in backend/tests). The command runs pytest in quiet mode with fail-fast flags, then conditionally runs coverage analysis only if tests pass. Test results are summarized with failure details when relevant, and coverage percentages highlight files below 80%.

c. How to run it (exact commands), expected outputs, and rollback/safety notes
Run `/tests` for all tests, `/tests -m integration` for marked tests, or `/tests backend/tests/test_notes.py` for a specific file. On success, you'll see a pass count followed by coverage percentages. On failure, you get the failing test name and assertion. This is read-only and configured in headless mode with restricted tool access (Bash and Read only).

d. Before vs. after (i.e. manual workflow vs. automated workflow)
Previously I had to navigate to week4/, activate the conda environment, set PYTHONPATH, run pytest manually, check results, then separately run coverage if tests passed. Now `/tests` handles all of that in one command, saving 2-3 minutes per run and reducing context switching.

e. How you used the automation to enhance the starter application
I ran `/tests` to verify the starter application before making any changes. All 3 tests passed, confirming the notes and action items endpoints work correctly. This baseline check gave me confidence to proceed with documentation work.


### Automation #2

a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
The best practices docs describe CLAUDE.md as living documentation that provides project context automatically. This guidance file acts like a project handbook that gets loaded at conversation start, eliminating the need to repeatedly explain structure and conventions.

b. Design of each automation, including goals, inputs/outputs, steps
This file provides comprehensive repository context without requiring explicit invocation. It documents the project structure, available make commands, safe versus dangerous operations, TDD workflows for adding endpoints, database seeding details, current API endpoints, and code style requirements. Claude Code reads this automatically when starting a conversation in week4/.

c. How to run it (exact commands), expected outputs, and rollback/safety notes
No command needed - it loads automatically when working in week4/. The file guides Claude to use appropriate make commands, avoid destructive operations like deleting the database, follow TDD patterns when adding endpoints, and run formatting checks after changes. Since it's documentation only, there's no risk and it can be updated as the project evolves.

d. Before vs. after (i.e. manual workflow vs. automated workflow)
Without CLAUDE.md, I had to explain how to run tests, start the server, and where files lived every time. Claude would explore with ls and grep commands, sometimes using inefficient paths. Now Claude knows the layout immediately, uses make commands correctly from the start, and follows established patterns without prompting. This saves 5-10 minutes per session and improves code quality.

e. How you used the automation to enhance the starter application
The CLAUDE.md file documented the existing project structure and established workflows. It provides context about the backend structure, where routers live, and how testing works. This makes it easier to work on the project without having to repeatedly explain these details.
