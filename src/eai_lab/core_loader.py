"""Read-only access to the bundled EAI Core 0.5.4."""

from __future__ import annotations

import json
from functools import lru_cache
from importlib.resources import files
from typing import Any

CORE_VERSION = "0.5.4"
_CORE_RESOURCE = "core/eai_core_v0.5.4.json"


class CoreIntegrityError(RuntimeError):
    """Raised when the bundled core is missing or not the pinned version."""


@lru_cache(maxsize=1)
def _core_text() -> str:
    return files("eai_lab").joinpath(_CORE_RESOURCE).read_text(encoding="utf-8")


def load_core() -> dict[str, Any]:
    """Return a fresh copy of the pinned canonical core."""
    core = json.loads(_core_text())
    if core.get("version") != CORE_VERSION:
        raise CoreIntegrityError(
            f"Expected EAI Core {CORE_VERSION}, found {core.get('version')!r}"
        )
    required = {
        "unknown_policy", "dimensions", "evidence_contract", "rules",
        "claim_boundaries", "observation_contract", "execution_contract",
        "lossless_knowledge_layer"
    }
    missing = sorted(required - core.keys())
    if missing:
        raise CoreIntegrityError(f"Core is missing required sections: {missing}")
    return core


def get_rule(rule_id: str) -> dict[str, Any]:
    for rule in load_core()["rules"]:
        if rule.get("id") == rule_id:
            return rule
    raise KeyError(rule_id)


def get_dimension(dimension_id: str) -> dict[str, Any]:
    for dimension in load_core()["dimensions"]:
        if dimension.get("id") == dimension_id:
            return dimension
    raise KeyError(dimension_id)


def observation_contract() -> dict[str, Any]:
    return load_core()["observation_contract"]
