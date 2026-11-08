"""Create the M0 task issues, sequentially blocked. Run once; idempotent by title."""

import json
import subprocess
import sys

REPO = "aswathas/ai-lab-m0-engineering"

ISSUES = [
    {
        "title": "M0.1 - Set up the package: pyproject, venv, imports",
        "body": """## What
A package that installs. `pip install -e ".[dev]"` from a clean virtualenv, and `import ticketrouter` works.

## Why first
Everything else in M0 lives in this package. Do it before writing a line of logic.

## Done when
- [ ] `pyproject.toml` with the project metadata, dependencies and the `dev` extra (pytest, ruff)
- [ ] `src/ticketrouter/__init__.py` exists and exports `__version__`
- [ ] A clean virtualenv install succeeds: `pip install -e ".[dev]"`
- [ ] `python -c "import ticketrouter; print(ticketrouter.__version__)"` prints a version
- [ ] `.gitignore` covers `__pycache__`, `.venv`, `.env`, `*.egg-info`, `.pytest_cache`

## Notes
- Source layout (`src/`), not a flat package. It is the only layout that stops a stale `import ticketrouter` from resolving to the wrong directory.
- Add `__version__` as a plain string constant. No `importlib.metadata` gymnastics yet.
""",
    },
    {
        "title": "M0.2 - Write the config module: env vars, validated at import",
        "body": """## What
`config.py` reads configuration from the environment and **fails loudly at import time** if it is missing or malformed.

## Done when
- [ ] A `ConfigError(ValueError)` exception in `errors.py`
- [ ] `Config` dataclass with typed fields: `api_key`, `base_url`, `timeout_s`, `max_attempts`, `db_url`
- [ ] `load_config()` reads `os.environ`, raises `ConfigError` naming the missing variable
- [ ] Numeric fields are validated: `timeout_s > 0`, `1 <= max_attempts <= 10`
- [ ] `.env.example` lists every variable with a comment
- [ ] At least 5 tests: missing key, bad timeout, too many attempts, happy path, defaults
- [ ] `Config` is frozen (`@dataclass(frozen=True)`)

## Notes
- Validate at the boundary, once. Every other module reads a `Config`, never `os.environ`.
- The error message must name the variable and what was expected. "Missing API key" is useless at 2am; "API_KEY is required; set it in .env" is not.
""",
    },
    {
        "title": "M0.3 - Write the typed HTTP client: timeout, retry, backoff with jitter",
        "body": """## What
An `httpx.AsyncClient` wrapper that times out, retries only retryable statuses, backs off exponentially with jitter, and never retries a 4xx.

## Done when
- [ ] `Client` with `base_url`, `api_key`, `timeout_s`, `max_attempts`
- [ ] `RETRYABLE = {409, 429, 500, 502, 503, 504}` as a module constant
- [ ] A non-retryable status raises immediately, without sleeping
- [ ] Backoff is `base * 2 ** attempt` plus jitter in `[0, 0.25)` s
- [ ] `httpx.TransportError` (network died) is retried; a 4xx is not
- [ ] The clock and the sleep are injected, so tests do not actually wait
- [ ] At least 6 tests: 200 returns, 400 does not retry, 500 retries N times, transport error retries, jitter bounds, timeout is set
- [ ] Every public method has a docstring

## Notes
- Inject the sleep function. A test that sleeps 3.5 seconds is a test nobody runs.
- Jitter exists so 100 clients retrying at once do not arrive together. Use `random.Random(seed)` - seeded, per the determinism rule.
""",
    },
    {
        "title": "M0.4 - Add idempotency keys to the write path",
        "body": """## What
Every non-idempotent request carries an `Idempotency-Key` header, stable across retries of the same logical action.

## Done when
- [ ] `Client.post(path, payload, idempotency_key=...)` sets the header
- [ ] The key is derived from the logical action, not random per attempt (so a retry reuses it) - e.g. `f"order-{order_id}-v1"`
- [ ] A test proves two calls with the same key produce ONE server-side effect
- [ ] The docstring says why this exists and what breaks without it

## Notes
- This is the difference between a retry and a duplicate charge. If you skip it, say so in the README's "what this cannot do" section.
""",
    },
    {
        "title": "M0.5 - Design the Postgres schema and the SQLAlchemy models",
        "body": """## What
A `tickets` table with a primary key, a unique external id, `TIMESTAMPTZ` timestamps, and an index; and the SQLAlchemy model that matches it exactly.

## Done when
- [ ] `models.py` with a `Ticket` model
- [ ] `external_id` is `UNIQUE` - this is the idempotency guarantee at rest
- [ ] `created_at` is `TIMESTAMPTZ`, not `TIMESTAMP`
- [ ] An index on `label`, partial (`WHERE label IS NOT NULL`)
- [ ] `db.py` has the engine, `SessionLocal`, and a `get_db()` dependency with `try/finally` cleanup
- [ ] An Alembic migration exists and `alembic upgrade head` runs clean
- [ ] At least 3 tests: unique constraint rejects a duplicate, index is used for a label query, timestamps carry a timezone

## Notes
- Constraints are cheaper than validation. A `UNIQUE` holds no matter which code path wrote the row; a check in a handler protects only that handler.
- Use `TIMESTAMPTZ`. Timezones are not a detail you add later.
""",
    },
    {
        "title": "M0.6 - Write the service layer: logic with no HTTP and no SQLAlchemy",
        "body": """## What
The business logic, written so it can be tested without a server and without a database.

## Done when
- [ ] `service.py` functions take plain Python objects and return plain Python objects
- [ ] No `fastapi` import, no session object, no HTTP response type in this module
- [ ] At least 4 unit tests that call the service functions directly
- [ ] Every invalid input raises a typed error, not a bare `ValueError`

## Notes
- This is the seam. If the service layer needs a database session, the boundary is in the wrong place and the tests will be slow.
""",
    },
    {
        "title": "M0.7 - Write the Pydantic schemas",
        "body": """## What
Request and response models. One declaration, three guarantees: validation, serialisation and OpenAPI docs.

## Done when
- [ ] `PredictRequest` with `text: str = Field(min_length=1, max_length=8000)`
- [ ] `PredictResponse` with `label: str`, `confidence: float = Field(ge=0, le=1)`, `abstain: bool`
- [ ] `HealthResponse` for the health endpoint
- [ ] Tests: empty text rejected, over-length text rejected, confidence out of range rejected, valid payload accepted

## Notes
- `Field` constraints are validation. The 422 you get for free is the point.
""",
    },
    {
        "title": "M0.8 - Build the FastAPI app: routes, DI, health check",
        "body": """## What
The HTTP layer: a health endpoint, a predict endpoint, dependency injection, and exception handlers that turn typed errors into clean responses.

## Done when
- [ ] `GET /health` returns 200 with `{"status": "ok"}`
- [ ] `POST /predict` uses `response_model=PredictResponse`
- [ ] The DB session comes in through `Depends(get_db)`, not opened in the handler body
- [ ] `ConfigError` and the domain errors are handled by exception handlers
- [ ] `app` is importable as `ticketrouter.main:app`
- [ ] Tests use `fastapi.testclient.TestClient` against the real app

## Notes
- The `try/finally` in `get_db` is the same context-manager pattern as the M0 lesson. A `return` halfway through the handler must not skip the cleanup.
""",
    },
    {
        "title": "M0.9 - Write the pytest suite: fixtures, parametrisation, a real local server",
        "body": """## What
The test suite. At least 25 tests, fixtures at the right scope, one parametrised test, and a local HTTP server instead of a mock of the client.

## Done when
- [ ] `tests/conftest.py` with fixtures: `config`, `db`, `client` (TestClient), `fake_server`
- [ ] At least one `@pytest.mark.parametrize` covering 3+ cases
- [ ] The fake server is a real local HTTP server, not `mocker.patch` of `httpx`
- [ ] At least 25 tests total, all green
- [ ] Tests are independent - running one alone passes
- [ ] No test sleeps more than 0.1 s (the clock and sleep are injected)
- [ ] `pytest -v` runs clean from the repo root

## Notes
- A mock asserts you called the method you expected. A real server asserts the request arrived and the response parsed. Test the wire.
""",
    },
    {
        "title": "M0.10 - Write the Dockerfile, docker-compose and .dockerignore",
        "body": """## What
The image and the local stack.

## Done when
- [ ] `Dockerfile` on a pinned base (`python:3.12-slim`, not `latest`)
- [ ] `pip install .` (the package), not `-r requirements.txt`
- [ ] `pip install --no-cache-dir`
- [ ] `CMD` is an exec array, not a shell string
- [ ] `.dockerignore` excludes `.git`, `.venv`, `.env`, `__pycache__`
- [ ] `docker-compose.yml` runs the app plus Postgres, with a healthcheck
- [ ] `docker build` succeeds and `docker compose up` serves `/health` -> 200
- [ ] The image size is recorded in the build log

## Notes
- `CMD uvicorn app:app` makes PID 1 a shell that swallows SIGTERM, so the container takes 30 s to die on deploy. That is the exec-array reason, stated once.
- Check the image size. Over 1 GB usually means `.dockerignore` is missing.
""",
    },
    {
        "title": "M0.11 - Write the README: architecture, API table, cost estimate, limits",
        "body": """## What
The README is the hiring artifact. A stranger must be able to clone, run and understand it in 5 minutes.

## Done when
- [ ] What it does, in one sentence, at the top
- [ ] An architecture section (an ASCII diagram or a Mermaid diagram is fine)
- [ ] The API table: method, path, request, response, status codes
- [ ] How to run it: venv, install, test, docker compose up
- [ ] The test command and the current test count
- [ ] A cost estimate for one call and for 10k calls/day
- [ ] An explicit **"what this cannot do"** section
- [ ] A screenshot of YOUR code, not a template

## Notes
- "What this cannot do" is the section that reads as senior. Nobody else writes it.
""",
    },
    {
        "title": "M0.12 - The G0 gate: ship a service with tests, from a blank repo",
        "body": """## What
**GATE.** 90 minutes. M0 is done only when this passes.

## The task
From a blank repo, in 90 minutes:
1. A FastAPI endpoint with a Pydantic request model and a response model
2. A `pytest` test that posts to it and asserts on the response
3. One `Depends`-injected resource with proper cleanup
4. A `.gitignore` that would keep a secret out of the repo

Materials open: the FastAPI docs, the pytest docs.

## Then answer out loud
- What is the difference between a `list` and a generator, and when must you care?
- Why does pytest complain about a missing fixture, and what are two causes?
- Your retry just doubled a customer's charge. What one thing was missing?

## Pass
The code works and the three answers are right. **Fail = do not start M1.**
""",
    },
]


def gh(args: list[str]) -> str:
    result = subprocess.run(
        ["gh", *args], capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


def main() -> None:
    existing = json.loads(
        gh(["issue", "list", "--repo", REPO, "--state", "all",
            "--limit", "100", "--json", "number,title"])
    )
    by_title = {issue["title"]: issue["number"] for issue in existing}

    numbers: list[int] = []
    for spec in ISSUES:
        if spec["title"] in by_title:
            numbers.append(by_title[spec["title"]])
            continue
        args = ["issue", "create", "--repo", REPO, "--title", spec["title"],
                "--body", spec["body"]]
        if numbers:
            args += ["--blocked-by", str(numbers[-1])]
        url = gh(args)
        number = int(url.rsplit("/", 1)[1])
        numbers.append(number)
        print(f"#{number} {spec['title']}")

    print("total:", len(numbers))


if __name__ == "__main__":
    sys.exit(main())
