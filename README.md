# ai-lab-m0-engineering

**M0 - The engineering spine.** The floor under everything else.

A typed Python package that does one real thing and does it properly: an HTTP client
with timeouts, retries with exponential backoff and jitter, and idempotency keys; a
FastAPI service over a Postgres schema; a Dockerfile; and a pytest suite that tests
against a real local server rather than a mock of the client.

| | |
|---|---|
| **Module note** | `Obsidian/AI Lab/Modules/00 - Engineering Spine/00 - Module Note.md` |
| **Resources** | `Obsidian/AI Lab/Modules/00 - Engineering Spine/01 - Resources.md` |
| **Vault** | `github.com/aswathas/ai-lab-vault` (private) |
| **Issues** | `github.com/aswathas/ai-lab-m0-engineering/issues` - one per task, sequential |

---

## Why this repo exists

Every AI feature a client pays for is a software system that happens to contain a model.
The model is 5% of the code and 5% of the failures. This module is the other 95%.

## What gets built

```
src/ticketrouter/
    config.py     env vars, validated at import
    client.py     typed httpx client: timeout, retry, backoff+jitter, idempotency key
    schemas.py    Pydantic request/response models
    db.py         engine, session, get_db dependency
    models.py     SQLAlchemy models + the UNIQUE constraint
    service.py    business logic, no HTTP, no DB details
    main.py       FastAPI app: routes, DI, health check
    errors.py     ConfigError and the exception handlers
```

## Rules

**You write every line of code in this repo.** The agent writes notes, explains, reviews,
quizzes and hints. It never writes an implementation - not the reference solution, not
the body of a TODO, not "just this one function". If you insist twice, it gives you a
worked trace (inputs, intermediate values, reasoning at each step) instead.

**The learner writes the code. The agent never does.** See `AGENTS.md`.

## Running it

```bash
python -m venv .venv && source .venv/Scripts/activate    # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest -v
docker compose up --build
```

## Status

Under construction. The acceptance criteria live in the module note's *The artifact*
section. The gate (G0) is a 90-minute build from a blank repo.
