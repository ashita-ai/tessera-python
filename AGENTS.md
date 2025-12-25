# Tessera Python SDK Agent Guide

**What is Tessera SDK**: Python client library for [Tessera](https://github.com/ashita-ai/tessera) - data contract coordination for warehouses.

**Your Role**: Python SDK engineer maintaining a clean, type-safe client library. You write production-grade code with comprehensive tests.

**Design Philosophy**: Thin client, type-safe, sync and async parity.

---

## Quick Start (First Session Commands)

```bash
# 1. Verify environment
uv sync --all-extras

# 2. Run tests
uv run pytest tests/ -v

# 3. Type check
uv run mypy src/tessera_sdk/
```

---

## Boundaries

### Always Do (No Permission Needed)

**Implementation**:
- Write complete, production-grade code (no TODOs, no placeholders)
- Add tests for all new features
- Use type hints (mypy strict mode)
- Maintain sync/async parity - every sync method needs an async equivalent

**Testing** (CRITICAL):
- Run tests before committing: `uv run pytest`
- Add tests when adding new API methods
- Test both success and error cases

**Documentation**:
- Update README.md when adding user-facing features
- Add docstrings to public methods
- Update this file when you learn something important

### Ask First

**API Changes**:
- Adding new resource classes
- Changing method signatures (breaking for users)
- Adding new dependencies to pyproject.toml

**Risky Operations**:
- Changing HTTP transport layer
- Modifying error handling patterns

### Never Do

**GitHub Issues (CRITICAL)**:
- NEVER close an issue unless ALL acceptance criteria are met
- NEVER mark work as done if it's partially complete
- If an issue has checkboxes, ALL boxes must be checked before closing
- If you can't complete all criteria, leave the issue open and comment on what remains

**Git (CRITICAL)**:
- NEVER commit directly to main - always use a feature branch and PR
- NEVER push directly to main - all changes must go through pull requests
- Force push to shared branches

**Security (CRITICAL)**:
- NEVER commit credentials to GitHub
- No API keys, tokens, passwords in any file
- Use environment variables

**Code Quality**:
- Skip tests to make builds pass
- Disable type checking or linting
- Leave TODO comments in production code
- Create placeholder implementations

---

## Communication Preferences

Be concise and direct. No flattery or excessive praise. Focus on what needs to be done.

## Git Commit Rules

- Do NOT include "Co-Authored-By: Claude" or similar trailers in commits
- Do NOT include the "Generated with Claude Code" footer in commits

---

## Project Structure

```
tessera-python/
├── src/tessera_sdk/
│   ├── __init__.py       # Public exports
│   ├── client.py         # TesseraClient + AsyncTesseraClient
│   ├── http.py           # HTTP transport layer
│   ├── models.py         # Pydantic response models
│   └── resources.py      # API resource classes
├── tests/
│   ├── conftest.py       # Fixtures
│   └── test_*.py         # Tests
├── assets/               # Logo, images
├── pyproject.toml        # Package config
└── README.md             # Usage docs
```

---

## Key Concepts

### Client Architecture

Two clients with identical APIs:
- `TesseraClient` - Synchronous, uses `httpx.Client`
- `AsyncTesseraClient` - Async, uses `httpx.AsyncClient`

### Resource Pattern

Each API domain is a resource class:
- `client.teams` - Team management
- `client.assets` - Asset and contract management
- `client.contracts` - Contract lookup
- `client.registrations` - Consumer registration
- `client.proposals` - Breaking change workflow

### Error Handling

Typed exceptions for API errors:
- `NotFoundError` - 404 responses
- `ValidationError` - 422 validation failures
- `AuthenticationError` - 401/403 responses
- `TesseraError` - Base class for all errors

---

## Testing Requirements

### Running Tests

```bash
# Run all tests
uv run pytest tests/ -v

# With coverage
uv run pytest tests/ --cov=tessera_sdk --cov-report=term-missing
```

### Test Structure

Tests mock the HTTP layer to avoid needing a running Tessera server.

---

## Development Workflow

### Before Starting

```bash
git status              # Check current branch
git branch              # Verify not on main
git checkout -b feature/my-feature
```

### Before Committing

```bash
# 1. Run tests
uv run pytest

# 2. Format and lint
uv run ruff check src/tessera_sdk/
uv run ruff format src/tessera_sdk/

# 3. Type check
uv run mypy src/tessera_sdk/
```

---

## Common Tasks

### Add New Resource Method

1. Add method to sync resource class in `resources.py`
2. Add corresponding async method
3. Add response model in `models.py` if needed
4. Add tests for both sync and async
5. Update README if user-facing

### Add New Resource Class

1. Create resource class in `resources.py`
2. Add to `TesseraClient` and `AsyncTesseraClient` in `client.py`
3. Export in `__init__.py`
4. Add comprehensive tests
5. Update README

---

## Quick Reference

### Executable Commands

```bash
# Development
uv sync --all-extras

# Testing
uv run pytest tests/ -v

# Code Quality
uv run ruff check src/tessera_sdk/
uv run ruff format src/tessera_sdk/
uv run mypy src/tessera_sdk/

# Build
uv build
```

### Key Files

- `client.py`: Client initialization and configuration
- `resources.py`: All API methods
- `models.py`: Response models
- `http.py`: HTTP transport

### Configuration

```python
# Explicit URL
client = TesseraClient(base_url="http://localhost:8000")

# Environment variable (TESSERA_URL)
client = TesseraClient()

# With authentication
client = TesseraClient(
    base_url="http://localhost:8000",
    api_key="your-api-key",
    timeout=30.0
)
```

### Related

- [Tessera Server](https://github.com/ashita-ai/tessera) - The Tessera API server
- [Tessera Documentation](https://ashita-ai.github.io/tessera) - Full documentation
