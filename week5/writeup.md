# Week 5 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: Zara Rutherford
SUNet ID: 06625318
Citations: Warp University 

This assignment took me about 1 hours to do. 


## YOUR RESPONSES
### Automation A: Warp Drive saved prompts, rules, MCP servers

a. Design of each automation, including goals, inputs/outputs, steps
Git MCP workflow (enabled): goals: branch, stage, commit, open PR notes headlessly; inputs: branch name, commit message prefix; outputs: branch refs and PR body text; steps: create branch, apply changes, run make format && make lint && make test, commit and push, generate PR notes from diff.
Test runner prompt (saved): goals: run pytest with optional path/marker, on pass rerun with coverage; inputs: marker/path; outputs: summary, coverage; steps: pytest -q --maxfail=1 -x, then pytest --cov=backend/app --cov-report=term-missing.

b. Before vs. after (i.e. manual workflow vs. automated workflow)
-efore: manual git branching/commits and ad-hoc test invocations; After: single prompt to branch/commit/prepare PR notes; single prompt to run tests + coverage consistently.

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
Read/write on repo; network for pushing branches; constrained to week5/ paths; dry-run preview before final push; user confirmation gates for push/PR steps.

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
MCP used to coordinate branch creation and commit boundaries across agents; wins: reduced merge conflicts; risk: concurrent edits to shared files mitigated by merge order (search → extract) and frequent pushes.

e. How you used the automation (what pain point it resolves or accelerates)
Rapid test-feedback loops and frictionless branching/PR prep, reducing context switches.


### Automation B: Multi‑agent workflows in Warp 

a. Design of each automation, including goals, inputs/outputs, steps
Agents: A (feature/search), B (feature/extract). Goals: implement Task 2 and Task 6 concurrently. Inputs: task specs; Outputs: code changes + passing tests. Steps: create branches, implement, run saved test prompt, push via MCP, merge in order (extract after search only touches different modules; merge order enforced by MCP).

b. Before vs. after (i.e. manual workflow vs. automated workflow)
Before: single-threaded implementation; After: concurrent workstreams with isolated branches using MCP for git hygiene.

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
Code write access limited to week5/; test and lint required to pass before MCP commit; human review of diffs prior to merge.

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
Clear file ownership (notes router vs extract service) minimized conflicts; occasional formatting conflicts resolved automatically by ruff/black in pre-commit step.

e. How you used the automation (what pain point it resolves or accelerates)
Parallelization reduced cycle time and enabled faster integration testing.


### (Optional) Automation C: Any Additional Automations
a. Design of each automation, including goals, inputs/outputs, steps


b. Before vs. after (i.e. manual workflow vs. automated workflow)


c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)


d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures


e. How you used the automation (what pain point it resolves or accelerates)

