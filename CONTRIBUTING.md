# Contributing

Thank you for your interest in contributing to VoiceSRT!

## Prerequisites

- Python 3.11+
- ffmpeg (`apt-get install ffmpeg` or `brew install ffmpeg`)
- Git

## Setup

```bash
git clone https://github.com/JFK/voicesrt.git
cd voicesrt
pip install -e ".[dev]"

# Generate encryption key
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Create .env
echo "ENCRYPTION_KEY=<paste key>" > .env

# Start dev server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Or with Docker:

```bash
cp .env.example .env
# Edit .env and set ENCRYPTION_KEY
docker compose up --build
```

## Development Workflow

### 1. Create a Branch

Branch from `main` using the convention:

```
feat/<description>     # New features
fix/<description>      # Bug fixes
refactor/<description> # Code improvements
docs/<description>     # Documentation
test/<description>     # Test additions
```

### 2. Make Changes

Follow the coding conventions:

- **Type hints** required on all functions
- **Async/await** for DB, API calls, file I/O, and subprocess
- **snake_case** for functions/variables, **PascalCase** for classes
- Code and comments in **English**
- Line length: **120 characters**

### 3. Lint and Format

```bash
ruff check src/ tests/       # Lint
ruff check --fix src/ tests/ # Auto-fix lint issues
ruff format src/ tests/      # Format
```

Ruff rules enabled: `E` (pycodestyle), `F` (pyflakes), `I` (isort), `N` (pep8-naming), `W` (warnings).

### 4. Run Tests

```bash
pytest                       # Run all tests
pytest -v --maxfail=5        # Verbose, stop after 5 failures
pytest --cov=src             # With coverage report
pytest tests/test_srt.py     # Single file
```

Tests use `pytest-asyncio` with `asyncio_mode = "auto"` — no need to mark async tests manually. Test timeout is 30 seconds.

### 5. Commit

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`
Scopes: `api`, `service`, `ui`, `db`, `infra`, `srt-editor`

Examples:

```
feat(srt-editor): add speaker assignment
fix(api): handle missing glossary gracefully
test: add model selection tests
docs: update architecture for v0.3.0
```

### 6. Create a Pull Request

- Target branch: `main`
- Keep PRs focused — one feature or fix per PR
- Include a description of what changed and why
- CI must pass (lint + format + tests)

## CI Pipeline

Every push and PR runs on GitHub Actions:

1. `ruff check src/ tests/` — lint
2. `ruff format --check src/ tests/` — format check
3. `pytest --cov=src` — tests with coverage
4. Coverage uploaded to Codecov (on `main` only)

## Writing Tests

### Test Structure

```
tests/
├── conftest.py              # Shared fixtures (encryption key, sample data)
├── test_srt.py              # Unit: SRT parse/generate
├── test_utils.py            # Unit: JSON repair, helpers
├── test_cost.py             # Unit: cost calculation
├── test_pipeline.py         # Integration: transcription pipeline
├── test_refine.py           # Integration: LLM refinement
├── test_settings_api.py     # API: settings endpoints
├── test_costs_api.py        # API: cost dashboard
├── test_api_validation.py   # API: input validation
└── ...
```

### Patterns

**Async tests** — just use `async def`:

```python
async def test_something():
    result = await some_async_function()
    assert result == expected
```

**FastAPI client**:

```python
from httpx import ASGITransport, AsyncClient
from src.main import app

async def test_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/jobs")
        assert response.status_code == 200
```

**Mocking external APIs** — always mock, never call real APIs in tests:

```python
from unittest.mock import AsyncMock, patch

async def test_with_mock():
    with patch("openai.AsyncOpenAI") as mock_cls:
        mock_client = AsyncMock()
        mock_cls.return_value = mock_client
        # ... test logic
```

## Database Migrations

When changing models in `src/models/`:

```bash
# Generate a migration
alembic revision --autogenerate -m "add column_name to table"

# Apply (also runs automatically on app startup)
alembic upgrade head

# Check current version
alembic current
```

Migrations run automatically in CI and on Docker container startup.

## Frontend Guidelines

- **No build step** — Tailwind CSS, HTMX, and Alpine.js are loaded from CDNs
- **No npm/yarn** — do not add JS dependencies or bundlers
- **Jinja2 templates** in `src/templates/`
- **HTMX** for server-driven updates (polling, partial page swaps)
- **Alpine.js** for client-side state (forms, editor, modals)
- **i18n** — add translations to both `src/i18n/en.json` and `src/i18n/ja.json`

## Project Architecture

See [docs/architecture.md](docs/architecture.md) for system design and data model details.

## Getting Help

- Open an issue for bugs or feature requests
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common errors
- Read the [User Guide](docs/user-guide.md) for feature documentation
