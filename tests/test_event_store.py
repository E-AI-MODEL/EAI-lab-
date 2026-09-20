import pytest

from eai_lab.event_store import DuplicateEventError, EventStore, EvidenceNamespaceError


def event(*, synthetic: bool, event_id: str = "evt_1"):
    return {
        "event_id": event_id,
        "case_id": "case_1",
        "timestamp": "2026-09-20T15:00:00+02:00",
        "actor": "learner",
        "phase": "P4",
        "action_type": "learner_attempt",
        "content_or_reference": "Learner response",
        "target_operation_if_relevant": "explain_causal_relation",
        "synthetic": synthetic,
    }


def test_real_store_rejects_synthetic_event():
    store = EventStore("real")
    with pytest.raises(EvidenceNamespaceError):
        store.append(event(synthetic=True))


def test_simulation_store_rejects_real_event():
    store = EventStore("simulation")
    with pytest.raises(EvidenceNamespaceError):
        store.append(event(synthetic=False))


def test_store_is_append_only_and_rejects_duplicate_ids():
    store = EventStore("real")
    store.append(event(synthetic=False))
    with pytest.raises(DuplicateEventError):
        store.append(event(synthetic=False))
    assert len(store) == 1


def test_returned_events_cannot_mutate_stored_events():
    store = EventStore("real")
    store.append(event(synthetic=False))
    returned = store.all()[0]
    returned["actor"] = "ai"
    assert store.all()[0]["actor"] == "learner"
