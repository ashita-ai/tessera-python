# Contributing to Tessera Python SDK

Thanks for your interest in contributing!

## Quick Setup

```bash
# Clone and install dependencies
git clone https://github.com/ashita-ai/tessera-python.git
cd tessera-python
uv sync --all-extras

# Install pre-commit hooks (auto-formats code on commit)
uv run pre-commit install

# Verify everything works
uv run pytest tests/ -v
```

## Before You Commit

Pre-commit hooks will automatically run when you commit, but you can also run them manually:

```bash
# Run all checks
uv run pre-commit run --all-files

# Or run individually
uv run ruff check src/tessera_sdk/
uv run ruff format src/tessera_sdk/
uv run mypy src/tessera_sdk/
```

## Development Workflow

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make your changes
3. Add tests for new functionality
4. Commit (pre-commit hooks will format your code)
5. Push and open a PR

## Key Guidelines

- **Sync/Async parity**: Every sync method needs an async equivalent
- **Type hints**: All public methods must have type hints
- **Tests**: Add tests for new API methods (see `tests/` for examples)
- **Docs**: Update README.md for user-facing changes

## Running Tests

```bash
# All tests
uv run pytest tests/ -v

# With coverage
uv run pytest tests/ --cov=tessera_sdk --cov-report=term-missing
```

## Questions?

Open an issue or check out [CLAUDE.md](./CLAUDE.md) for detailed development guidelines.
