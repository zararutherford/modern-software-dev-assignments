# Week 5 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **TODO** \
SUNet ID: 06625318
Citations: Warp University 

This assignment took me about 1 hours to do. 


## YOUR RESPONSES
### Automation A: Warp Drive saved prompts, rules, MCP servers

a. Design of each automation, including goals, inputs/outputs, steps
I enabled the Git MCP workflow to handle branching, committing, and preparing PR notes non‑interactively. It accepts a branch name and optional commit prefix, runs format/lint/tests, pushes, and generates a PR summary from the diff. I also added a saved “Test runner” prompt that runs pytest quietly with fail‑fast; if tests pass and pytest‑cov is available, it runs coverage and reports gaps.

b. Before vs. after (i.e. manual workflow vs. automated workflow)
Previously I ran ad‑hoc git and test commands; now a single prompt performs consistent branching/commit/PR steps, and one test prompt yields fast results with optional coverage.

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
I granted read/write repo access and network rights to push, constrained actions to week5/. I reviewed diffs and required green format/lint/tests before pushing or preparing PR notes.

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
The MCP workflow standardized branch creation and commit boundaries across agents. Conflicts were minimized by merging search first, then extraction, with frequent small pushes.

e. How you used the automation (what pain point it resolves or accelerates)
These automations shortened feedback cycles and removed manual git overhead, reducing context switches.


### Automation B: Multi‑agent workflows in Warp 

a. Design of each automation, including goals, inputs/outputs, steps
I ran two agents on branches feature/search and feature/extract to implement Task 2 and Task 6 in parallel. Each agent developed on its own branch, used the test prompt, and pushed via MCP; I merged in the order that minimized conflicts.

b. Before vs. after (i.e. manual workflow vs. automated workflow)
Sequential work would have lengthened the cycle; parallel branches cut time and enabled earlier integration checks.

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
Agents could modify week5/ only; commits required passing format/lint/tests; I reviewed diffs before merging.

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
Clear ownership (notes router vs extraction service) avoided most conflicts, and auto‑formatting handled style differences.

e. How you used the automation (what pain point it resolves or accelerates)
This workflow enabled concurrent progress and faster end‑to‑end testing.


### (Optional) Automation C: Any Additional Automations
a. Design of each automation, including goals, inputs/outputs, steps


b. Before vs. after (i.e. manual workflow vs. automated workflow)


c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)


d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures


e. How you used the automation (what pain point it resolves or accelerates)

