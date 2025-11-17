# Week 7 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: Zara Rutherford \
SUNet ID: 06625318 \
Citations: Claude, Graphite

This assignment took me about 2 hours to do. 


## Task 1: Add more endpoints and validations
a. Links to relevant commits/issues
Commit: 48d7320

b. PR Description
Added DELETE endpoints for notes and action items (returns 204 on success, 404 if not found). Implemented Pydantic Field validators with min_length=1 on all text inputs and max_length=200 on note titles. Added 7 tests for DELETE operations and validation edge cases (empty strings, too-long titles).

c. Graphite Diamond generated code review
This PR adds solid DELETE functionality and input validation. The implementation is consistent across both routers with proper 404 handling and appropriate 204 status codes. The Pydantic Field validators are well-placed on both create and patch schemas, preventing empty strings and enforcing reasonable limits. Test coverage is thorough, including edge cases like nonexistent resources and boundary validation. One minor note: the DELETE endpoints use db.flush() rather than db.commit() - this is fine if transactions are managed at a higher level, but verify this aligns with your transaction handling strategy. Overall, clean and well-tested changes.

## Task 2: Extend extraction logic
a. Links to relevant commits/issues
Commit: e6f9d36

b. PR Description
Extended action item extraction with regex patterns for checkboxes ([x], [ ]), priority markers (HIGH:, P0:), @mentions, and due date keywords (by, due, deadline). Improved list marker handling to strip -, *, •, and numbered lists. Added 5 test functions covering all new patterns. All 16 tests pass.

c. Graphite Diamond generated code review
This is a well-structured PR with strong test coverage for the new extraction patterns. The regex-based approach cleanly handles the 6 different action item patterns, and the list marker stripping is a nice touch. One concern: the @mention pattern (line 27) will match any email address (like test@example.com), which may create false positives for non-assignment contexts. Consider tightening this to match only @username patterns at word boundaries or in assignment contexts. The test suite is comprehensive, though test_extract_numbered_lists could benefit from explicit assertions that plain numbered items don't match. Overall, solid implementation that significantly enhances the extraction capabilities.

## Task 3: Try adding a new model and relationships
a. Links to relevant commits/issues
Commit: 22a1ee7

b. PR Description
Created Tag model with many-to-many relationship to Notes using association table note_tags. Added unique constraint on tag names (max 50 chars). Built REST API for tags with CRUD operations plus endpoints to add/remove tags from notes. Added 5 tests covering tag operations and relationships. All 21 tests pass.

c. Graphite Diamond generated code review
This PR implements a clean many-to-many relationship between Notes and Tags with proper association table setup and bidirectional relationships. The REST API is well-structured with comprehensive CRUD operations plus relationship management endpoints, following existing router patterns. Good error handling for edge cases (duplicate tags, missing resources), proper validation constraints, and solid test coverage across all operations. The unique constraint on tag names prevents duplicates at the database level, and the tests verify both happy paths and error conditions effectively.

## Task 4: Improve tests for pagination and sorting
a. Links to relevant commits/issues
Commit: e20d4a4

b. PR Description
Created comprehensive test suite for pagination and sorting edge cases. Tests cover: skip beyond available items, limit boundaries (0, 200, 500), sort order verification on multiple fields (ascending/descending), filtering + pagination combinations, and invalid sort fields. Added 9 test functions across notes, action-items, and tags. All 30 tests pass.

c. Graphite Diamond generated code review
This PR adds a comprehensive test suite for pagination and sorting functionality across all three resources (notes, action-items, tags). The tests are well-structured and cover important edge cases like skip beyond available items, boundary conditions (limit=0, limit=200, limit>200), and combinations of filtering with pagination. The approach of creating specific test data and then filtering for it by ID is solid for isolating test behavior. One minor consideration: some tests could benefit from cleanup/teardown to ensure test isolation, though this may already be handled by your test fixtures. Overall, this provides strong coverage for critical API functionality and should catch regressions effectively.

## Brief Reflection
a. The types of comments you typically made in your manual reviews (e.g., correctness, performance, security, naming, test gaps, API shape, UX, docs).

I focused on correctness (edge cases, 404 handling), test coverage (ensuring new code had tests), API design (RESTful patterns), and input validation (preventing bad data). Also checked for code consistency with existing patterns.

b. A comparison of **your** comments vs. **Graphite's** AI-generated comments for each PR.

My reviews focused on basic correctness and test coverage. Graphite caught deeper issues I missed - like the @mention pattern matching email addresses (Task 2), db.flush() vs db.commit() concerns (Task 1), and suggestions for test isolation improvements (Task 4). Graphite was more thorough in identifying edge cases and potential bugs.

c. When the AI reviews were better/worse than yours (cite specific examples)

Better: Graphite identified the email matching bug in extract.py (@mention pattern too broad) and the transaction handling question with db.flush(). It also gave specific line references and architectural feedback.

Worse: Graphite sometimes over-explains obvious patterns (like explaining what 204 status codes mean). My reviews were more concise for straightforward implementations.

d. Your comfort level trusting AI reviews going forward and any heuristics for when to rely on them.

I'd trust AI reviews for catching common bugs, edge cases, and security issues. They're good at pattern matching against best practices. But I'd still need human review for business logic, architecture decisions, and context-specific tradeoffs. Use AI for first-pass reviews and bug hunting, but don't skip human review for critical code. 



