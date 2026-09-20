# EAI Lab

**EAI Lab** is an experimental runtime for building, simulating and inspecting AI-supported learning configurations without confusing task performance with learning.

The repository starts from one rule: evidence about what a learner can do must stay separate from what an AI, teacher, peer or simulator contributed.

## Status

This is the foundation release. It contains the semantic core, data contracts and first runtime safeguards. It does **not** yet contain a tutor agent, production database, classroom UI or validated learner simulator.

Semantic authority in this repository: **EAI Core 0.5.4**. The core is treated as read-only runtime logic. Missing or conflicting evidence remains `UNKNOWN`; it is never silently converted to a low score.

## What is already here

- `src/eai_lab/core/` contains the pinned EAI Core 0.5.4 and its conformance suite.
- `contracts/` contains the first three stable interchange contracts: learning case, learning event and evidence record.
- `src/eai_lab/core_loader.py` exposes the core without duplicating its semantics.
- `src/eai_lab/event_store.py` provides an append-only in-memory event store and prevents real/synthetic evidence mixing.
- `src/eai_lab/validation.py` validates payloads against the JSON contracts.
- `tests/` checks core integrity, contract behavior and evidence namespace separation.

## Architecture

```text
Learning case
    |
    v
Observable event  ---> append-only EventStore
    |
    v
Evidence record
    |
    v
EAI runtime / gates
    |
    +--> intervention proposal
    +--> UNKNOWN / blocked claim
    +--> bounded conclusion

Simulation uses the same event shape but a different namespace.
Simulation output is never evidence about a real learner.
```

## First contracts

`learning_case` defines the goal and target cognitive operations. `learning_event` records who actually did what. `evidence_record` connects a bounded conclusion to event IDs and evidence fit.

These contracts deliberately contain no universal `mastery` percentage.

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e '.[dev]'
pytest
```

## Next milestone

The next milestone is a deterministic EAI gate engine that consumes events and candidate interventions. Generative models may propose an intervention; the EAI runtime decides whether the proposal is allowed, needs modification or must be blocked.

See `docs/architecture.md` and `docs/roadmap.md`.
