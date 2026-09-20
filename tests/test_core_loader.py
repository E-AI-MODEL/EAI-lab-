from eai_lab.core_loader import CORE_VERSION, get_rule, load_core


def test_core_version_and_required_sections():
    core = load_core()
    assert core["version"] == CORE_VERSION == "0.5.4"
    assert core["unknown_policy"]["may_be_coerced_to_lowest_state"] is False
    assert len(core["dimensions"]) >= 18
    assert "lossless_knowledge_layer" in core


def test_core_is_returned_as_fresh_copy():
    first = load_core()
    first["version"] = "mutated"
    second = load_core()
    assert second["version"] == "0.5.4"


def test_key_claim_and_didactic_rules_are_present():
    assert get_rule("CLM-01")["then"] == "block_claim"
    assert get_rule("CLM-03")["id"] == "CLM-03"
    assert get_rule("CLM-04")["id"] == "CLM-04"
    assert get_rule("DID-01")["id"] == "DID-01"
    assert get_rule("DID-03")["id"] == "DID-03"
    assert get_rule("DID-04")["id"] == "DID-04"
