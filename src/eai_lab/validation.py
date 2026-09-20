"""JSON contract validation for EAI Lab payloads."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

_REPO_ROOT = Path(__file__).resolve().parents[2]
_CONTRACT_DIR = _REPO_ROOT / "contracts"
_ALLOWED = {"learning_case", "learning_event", "evidence_record"}


def load_schema(name: str) -> dict[str, Any]:
    if name not in _ALLOWED:
        raise KeyError(name)
    path = _CONTRACT_DIR / f"{name}.schema.json"
    return json.loads(path.read_text(encoding="utf-8"))


def validate_payload(name: str, payload: dict[str, Any]) -> None:
    schema = load_schema(name)
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(payload)
