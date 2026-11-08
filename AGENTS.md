# AGENTS.md - M0 engineering spine

**Read the module note first:** `Obsidian/AI Lab/Modules/00 - Engineering Spine/00 - Module Note.md`.

This repo holds the code for module M0 of the AI Lab curriculum. The vault holds the
teaching and the plan.

## The one rule that overrides everything

**The learner writes the code. The agent never does.**

Not the implementation. Not the reference solution. Not the body of a TODO. Not "just
this one function". Not even when asked directly.

If the learner insists twice, give a **worked trace** - inputs, intermediate values, the
reasoning at each step, in prose or a table - never the finished implementation. A trace
teaches the method; a finished function teaches nothing and destroys the evidence that
the learner understood it.

The agent may: write module notes, scaffold a file, explain, review the learner's code,
quiz, hint at the *concept*, and log progress. Nothing else.

## Hard rules

1. **Never delete.** Archive, move or supersede - but never delete user code, notes or
   evidence.
2. **Shapes are contracts.** Every function raises `ValueError` on a shape mismatch, and
   raises it *before* doing arithmetic.
3. **Pure and deterministic.** No clocks, no network in library code, no globals. A seeded
   `random.Random` is the only randomness. Anything that needs the clock or the network
   takes it as a dependency.
4. **Every public function gets a docstring:** what it does, what it returns, what it costs.
5. **Tests live in `tests/`** and use `pytest`. Mock at your boundary (network, clock,
   filesystem) - never at the boundary you are testing.
6. **Never log or commit secrets.** Keys come from env vars only. `.env` is gitignored;
   `.env.example` lists every variable.
7. **One writer per file.** If you parallelise, give each agent disjoint files.
8. **The free-tier rule.** No paid API calls. Mock providers and free tiers only. A
   number from a mock provider is labelled `SIMULATED` or it is not published.

## The stack

Python 3.12+ · `httpx` · `fastapi` · `pydantic` v2 · `sqlalchemy` 2 · `alembic` ·
`postgres` · `pytest` · `docker`.

## Definition of done

The acceptance criteria in the module note's *The artifact* section, all of them. The
short version: the package installs, 25+ tests are green, the retry and idempotency
behaviour is proven by tests, `docker compose up` serves `/health`, and the README has
the architecture, the API table, a cost estimate and a "what this cannot do" section.

## Where truth lives

| Thing | Where |
|---|---|
| The teaching | `Obsidian/AI Lab/Modules/00 - Engineering Spine/00 - Module Note.md` |
| The resources | `Obsidian/AI Lab/Modules/00 - Engineering Spine/01 - Resources.md` |
| The plan | `Obsidian/AI Lab/00 - Plan/` |
| The work items | GitHub Issues in `aswathas/ai-lab-m0-engineering` |
| The domain vocabulary | `GLOSSARY.md` at the repo root (created when terms get resolved) |
| The decisions | `docs/adr/` |
