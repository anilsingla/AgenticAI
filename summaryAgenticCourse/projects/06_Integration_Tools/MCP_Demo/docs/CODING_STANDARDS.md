# Coding Standards

## General
- Keep modules focused and small.
- Prefer explicit names for functions, classes, and variables.
- Add short comments only where logic is non-obvious.
- Avoid hardcoded secrets; use environment variables via .env.

## Python
- Follow PEP 8 and use type hints for new code.
- Keep side effects under if __name__ == '__main__' blocks.
- Validate external inputs and fail with clear error messages.

## Logging and Reports
- Write runtime logs to the logs folder.
- Write run summaries and generated reports to the reports folder.
- Keep outputs deterministic when possible for demos/tests.
