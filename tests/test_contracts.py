import pytest
from jsonschema import ValidationError

from eai_lab.validation import validate_payload


def test_minimal_learning_case_is_valid():
    validate_payload(
        "learning_case",
        {
            "case_id": "case_1",
            "mode": "real",
            "learning_goal": "Explain a causal relation independently.",
            "target_core_operations": ["explain_causal_relation"],
        },
    )


def test_learning_case_requires_target_operation():
    with pytest.raises(ValidationError):
        validate_payload(
            "learning_case",
            {"case_id": "case_1", "mode": "real", "learning_goal": "Explain."},
        )


def test_learning_event_uses_canonical_actor_values():
    payload = {
        "event_id": "evt_1",
        "case_id": "case_1",
        "timestamp": "2026-09-20T15:00:00+02:00",
        "actor": "learner",
        "phase": "P4",
        "action_type": "learner_attempt",
        "content_or_reference": "Because...",
        "target_operation_if_relevant": "explain_causal_relation",
        "synthetic": False,
    }
    validate_payload("learning_event", payload)
    payload["actor"] = "oracle"
    with pytest.raises(ValidationError):
        validate_payload("learning_event", payload)


def test_evidence_record_can_explicitly_remain_unknown():
    validate_payload(
        "evidence_record",
        {
            "evidence_id": "ev_1",
            "case_id": "case_1",
            "claim_type": "retention",
            "source_event_ids": ["evt_1"],
            "assessment_status": "unknown",
            "evidence_fit": "UNKNOWN",
            "conclusion": "No delayed independent evidence is available yet.",
            "core_version": "0.5.4",
        },
    )
