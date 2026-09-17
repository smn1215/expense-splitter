# AI Usage Report

## Tools Used
- ChatGPT / Claude: Drafted product specs, OpenAPI contracts, and test setup.
- GitHub Copilot / Cursor: Assisted in generating FastAPI database integration boilerplate code.

## Key Prompts & Iterations
- Prompt: "Generate a FastAPI backend handling expense creation with SQLite persistence."
- Refinement: Manually adjusted database initialization logic to trigger on startup without complex migrations.

## Verification
- Verified persistence via local SQLite creation (`expenses.db`).
- Ran automated test suite via `pytest`.
