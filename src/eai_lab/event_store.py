"""Append-only event storage for the first EAI Lab vertical slice."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any, Literal

from .core_loader import observation_contract

Namespace = Literal["real", "simulation"]


class EvidenceNamespaceError(ValueError):
    """Raised when synthetic evidence crosses into the real namespace or vice versa."""


class DuplicateEventError(ValueError):
    """Raised when an event ID is appended more than once."""


class EventShapeError(ValueError):
    """Raised when a minimum canonical event field is absent or malformed."""


class EventStore:
    """Append-only in-memory event store with hard real/simulation separation."""

    def __init__(self, namespace: Namespace) -> None:
        if namespace not in ("real", "simulation"):
            raise ValueError("namespace must be 'real' or 'simulation'")
        self.namespace = namespace
        self._events: list[dict[str, Any]] = []
        self._ids: set[str] = set()

    def append(self, event: dict[str, Any]) -> dict[str, Any]:
        self._validate_minimum_shape(event)
        synthetic = bool(event.get("synthetic"))
        expected_synthetic = self.namespace == "simulation"
        if synthetic != expected_synthetic:
            raise EvidenceNamespaceError(
                f"Event synthetic={synthetic} cannot enter {self.namespace!r} namespace"
            )
        event_id = event["event_id"]
        if event_id in self._ids:
            raise DuplicateEventError(event_id)
        stored = deepcopy(event)
        self._events.append(stored)
        self._ids.add(event_id)
        return deepcopy(stored)

    def all(self) -> tuple[dict[str, Any], ...]:
        return tuple(deepcopy(self._events))

    def for_case(self, case_id: str) -> tuple[dict[str, Any], ...]:
        return tuple(
            deepcopy(event) for event in self._events if event.get("case_id") == case_id
        )

    def __len__(self) -> int:
        return len(self._events)

    @staticmethod
    def _validate_minimum_shape(event: dict[str, Any]) -> None:
        contract = observation_contract()
        required = set(contract["minimum_event_fields"]) | {"case_id", "synthetic"}
        missing = sorted(field for field in required if field not in event)
        if missing:
            raise EventShapeError(f"Missing event fields: {missing}")
        if event["actor"] not in contract["actor_values"]:
            raise EventShapeError(f"Unsupported actor: {event['actor']!r}")
        try:
            datetime.fromisoformat(str(event["timestamp"]).replace("Z", "+00:00"))
        except ValueError as exc:
            raise EventShapeError("timestamp must be ISO-8601") from exc
