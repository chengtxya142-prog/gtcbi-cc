import copy
import sys
import unittest
from pathlib import Path

from discovery_fixtures import approve, discovery_fixture

ROOT = Path(__file__).resolve().parents[1] / "skills" / "gtcbi"
sys.path.insert(0, str(ROOT / "scripts"))
from discovery_contract import normalize_domain, validate_discovery, validate_gate


def codes(record):
    return {issue["code"] for issue in validate_discovery(record)}


def additional_batch():
    return {
        "id": "B2", "kind": "additional", "requested_count": 3,
        "quantity_basis": "operator", "actual_count": 0,
        "candidate_ids": [], "snapshot_revision": "P1",
        "shortfall_reason": "No new synthetic sources",
    }


def manual_candidate():
    return {
        "id": "CAND-002", "name": "Manually Supplied Buyer (fictional)",
        "country": None, "website": None, "match_reason": "Operator supplied; unverified",
        "sources": [], "entity_key": "SYN-MANUAL-BUYER", "status": "pending",
        "snapshot_revision": "P1", "origin": "manual",
    }


class DiscoveryTests(unittest.TestCase):
    def test_valid_pending_record_and_no_mutation(self):
        data = discovery_fixture()
        before = copy.deepcopy(data)
        self.assertEqual(validate_discovery(data), [])
        self.assertEqual(data, before)

    def test_malformed_shapes_are_diagnosed(self):
        for value in (None, [], "record", 3):
            with self.subTest(value=value):
                self.assertIn("SCHEMA", codes(value))
        for field, value in (
            ("snapshot", None), ("entry_mode", []), ("batches", [None]),
            ("candidates", [[]]), ("selection", {}),
        ):
            with self.subTest(field=field):
                data = discovery_fixture()
                data[field] = value
                self.assertIn("SCHEMA", codes(data))
        data = discovery_fixture()
        del data["snapshot"]
        self.assertIn("SCHEMA", codes(data))

    def test_activity_requires_real_confirmations_on_current_revision(self):
        for field in ("profile_confirmation", "keyword_confirmation"):
            for value in (None, {}, {"confirmed": "true", "revision": "P1", "basis": "OK"}):
                with self.subTest(field=field, value=value):
                    data = discovery_fixture()
                    data["snapshot"][field] = value
                    self.assertIn("CONFIG_UNCONFIRMED", codes(data))
            data = discovery_fixture()
            data["snapshot"][field]["revision"] = "P2"
            self.assertIn("CONFIG_REVISION", codes(data))

    def test_empty_draft_does_not_require_confirmations(self):
        data = discovery_fixture()
        data["batches"] = []
        data["candidates"] = []
        del data["snapshot"]["profile_confirmation"]
        del data["snapshot"]["keyword_confirmation"]
        self.assertEqual(validate_discovery(data), [])

    def test_empty_direct_target_requires_candidate_and_confirmations(self):
        data = discovery_fixture()
        data.update(entry_mode="direct_target", batches=[], candidates=[])
        self.assertIn("SCHEMA", codes(data))
        del data["snapshot"]["profile_confirmation"]
        del data["snapshot"]["keyword_confirmation"]
        self.assertIn("CONFIG_UNCONFIRMED", codes(data))

    def test_confirmation_time_requires_an_iso_datetime_or_null(self):
        data = discovery_fixture()
        confirmation = data["snapshot"]["keyword_confirmation"]
        for timestamp in (
            "not a time", "2026-11-10", "2026-02-30T13:30:00Z",
            "2026-11-10T13:30:00+12:60", "2026-11-10T13:30:00+00:99",
            "2026-11-10T13:30:00+24:00",
        ):
            with self.subTest(timestamp=timestamp):
                confirmation["confirmed_at"] = timestamp
                self.assertIn("SCHEMA", codes(data))
        for timestamp in (None, "2026-11-10T13:30:00Z", "2026-11-10T13:30:00+08:00"):
            with self.subTest(timestamp=timestamp):
                confirmation["confirmed_at"] = timestamp
                self.assertEqual(validate_discovery(data), [])

    def test_config_and_keyword_payload_are_checked(self):
        data = discovery_fixture()
        data["snapshot"]["markets"] = [""]
        self.assertIn("SCHEMA", codes(data))
        data = discovery_fixture()
        data["snapshot"]["keywords"]["include"] = []
        self.assertIn("SCHEMA", codes(data))

    def test_invalid_requested_count(self):
        for count in (0, -1, 1.5, True, "10", None):
            with self.subTest(count=count):
                data = discovery_fixture()
                data["batches"][0]["requested_count"] = count
                self.assertIn("BATCH_QUANTITY", codes(data))

    def test_initial_batch_can_override_default_only_explicitly(self):
        data = discovery_fixture()
        batch = data["batches"][0]
        batch["requested_count"] = 3
        self.assertIn("BATCH_QUANTITY", codes(data))
        batch["quantity_basis"] = "operator"
        self.assertEqual(validate_discovery(data), [])

    def test_later_batch_requires_operator_quantity(self):
        data = discovery_fixture()
        batch = additional_batch()
        batch["quantity_basis"] = "default"
        data["batches"].append(batch)
        self.assertIn("BATCH_QUANTITY", codes(data))

    def test_actual_count_matches_membership_and_does_not_exceed_request(self):
        for count in (True, -1, 0, 11):
            with self.subTest(count=count):
                data = discovery_fixture()
                data["batches"][0]["actual_count"] = count
                self.assertIn("BATCH_COUNT", codes(data))
        data = discovery_fixture()
        data["batches"][0].update(requested_count=1, quantity_basis="operator",
                                   candidate_ids=["CAND-001", "CAND-002"], actual_count=2)
        self.assertIn("BATCH_COUNT", codes(data))

    def test_shortfall_needs_meaningful_reason(self):
        data = discovery_fixture()
        data["batches"][0]["shortfall_reason"] = " "
        self.assertIn("SHORTFALL_REASON", codes(data))

    def test_batch_references_known_candidates_at_its_revision(self):
        data = discovery_fixture()
        data["batches"][0]["candidate_ids"] = ["UNKNOWN"]
        self.assertIn("SCHEMA", codes(data))
        data = discovery_fixture()
        data["batches"][0]["snapshot_revision"] = "P2"
        self.assertIn("CONFIG_REVISION", codes(data))
        data = discovery_fixture()
        data["candidates"][0]["snapshot_revision"] = "P2"
        self.assertIn("CONFIG_REVISION", codes(data))

    def test_duplicate_candidate_id_cannot_be_redisplayed(self):
        data = discovery_fixture()
        data["candidates"].append(copy.deepcopy(data["candidates"][0]))
        self.assertIn("DUPLICATE_CANDIDATE", codes(data))
        data = discovery_fixture()
        second = additional_batch()
        second.update(actual_count=1, candidate_ids=["CAND-001"])
        data["batches"].append(second)
        self.assertIn("DUPLICATE_CANDIDATE", codes(data))

    def test_duplicate_entity_cannot_get_a_second_id(self):
        data = self.shared_domain_record()
        data["candidates"][1]["entity_key"] = "SYN-BUYER-GB"
        self.assertIn("DUPLICATE_ENTITY", codes(data))

    def test_shared_domain_is_not_an_entity_verdict(self):
        self.assertEqual(validate_discovery(self.shared_domain_record()), [])

    @staticmethod
    def shared_domain_record():
        data = discovery_fixture()
        other = copy.deepcopy(data["candidates"][0])
        other.update(id="CAND-002", entity_key="SYN-BUYER-IE", country="IE",
                     name="Example Buyer Ireland (fictional)",
                     match_reason="Separate synthetic Irish subsidiary")
        data["candidates"].append(other)
        batch = additional_batch()
        batch.update(actual_count=1, candidate_ids=["CAND-002"])
        data["batches"].append(batch)
        return data

    def test_only_actually_read_sources_count_for_discovered_candidate(self):
        for sources in ([], [None], [{"url": "https://buyer.example.invalid",
                                      "checked_on": "2026-11-10",
                                      "access_state": "search_result"}]):
            with self.subTest(sources=sources):
                data = discovery_fixture()
                data["candidates"][0]["sources"] = sources
                self.assertIn("SCHEMA", codes(data))

    def test_direct_target_without_batch_or_known_website(self):
        data = discovery_fixture()
        data.update(entry_mode="direct_target", batches=[])
        data["candidates"][0].update(website=None, country=None, sources=[])
        self.assertEqual(validate_discovery(data), [])
        del data["snapshot"]["profile_confirmation"]
        self.assertIn("CONFIG_UNCONFIRMED", codes(data))

    def test_manual_addition_shares_pool_without_changing_batch_membership(self):
        data = discovery_fixture()
        data["candidates"].append(manual_candidate())
        self.assertEqual(validate_discovery(data), [])
        del data["snapshot"]["profile_confirmation"]
        self.assertIn("CONFIG_UNCONFIRMED", codes(data))

    def test_candidate_origin_rejects_explicit_invalid_values(self):
        for origin in (None, "", "external", [], True):
            with self.subTest(origin=origin):
                data = discovery_fixture()
                data["candidates"][0]["origin"] = origin
                self.assertIn("SCHEMA", codes(data))

    def test_manual_candidate_cannot_count_toward_a_discovery_batch(self):
        data = discovery_fixture()
        data["candidates"][0]["origin"] = "manual"
        self.assertIn("SCHEMA", codes(data))

    def test_discovery_default_still_requires_batch_membership(self):
        data = discovery_fixture()
        data["batches"] = []
        self.assertIn("SCHEMA", codes(data))

    def test_explicit_discovered_origin_requires_a_batch_and_read_sources(self):
        data = discovery_fixture()
        data["candidates"][0]["origin"] = "discovered"
        self.assertEqual(validate_discovery(data), [])
        missing_batch = copy.deepcopy(data)
        missing_batch.update(entry_mode="direct_target", batches=[])
        self.assertIn("SCHEMA", codes(missing_batch))
        data["candidates"][0]["sources"] = []
        self.assertIn("SCHEMA", codes(data))

    def test_adding_manual_candidate_does_not_inherit_approval(self):
        data = approve(discovery_fixture())
        data["candidates"].append(manual_candidate())
        self.assertEqual(validate_discovery(data), [])
        data["runs"] = [run_summary("CAND-002")]
        self.assertEqual(codes(data), {"GATE_SELECTION"})

    def test_normalize_domain(self):
        self.assertEqual(normalize_domain("https://www.EXAMPLE.invalid./shop?a=1"),
                         "example.invalid")
        for value in (None, "example.invalid", "https://[", {}, [1], 3, b"https://a"):
            with self.subTest(value=value):
                self.assertIsNone(normalize_domain(value))

    def test_normalize_domain_rejects_invalid_ports(self):
        for port in ("no-such-port", "65536"):
            with self.subTest(port=port):
                self.assertIsNone(normalize_domain(f"https://buyer.example.invalid:{port}/about"))
        self.assertEqual(normalize_domain("https://buyer.example.invalid:443/about"),
                         "buyer.example.invalid")


def run_summary(candidate_id="CAND-001", run_id="SYN-RUN-001", revision="P1", **extra):
    return {
        "run_id": run_id, "candidate_id": candidate_id,
        "snapshot_revision": revision, "execution": "running", "pause": None,
        **extra,
    }


def pause_fixture():
    return {
        "reason_code": "access_blocked",
        "reason": "The synthetic source is unavailable",
        "conflicts": [],
        "needed_input": "An accessible primary source",
        "resume_condition": "An accessible primary source is supplied",
    }


def embedded_run():
    data = approve(discovery_fixture())
    return {
        "target": {"candidate_id": "CAND-001", "entity_id": "SYN-BUYER-GB"},
        "gate": {
            "schema": "discovery-gate-v1", "discovery_id": data["discovery_id"],
            "candidate_id": "CAND-001", "snapshot": data["snapshot"],
            "approval": data["approval"],
        },
    }


class ApprovalTests(unittest.TestCase):
    def test_checked_without_final_confirmation_is_valid_only_without_runs(self):
        data = discovery_fixture()
        data["selection"] = ["CAND-001"]
        data["candidates"][0]["status"] = "selected"
        self.assertEqual(validate_discovery(data), [])
        data["runs"] = [run_summary()]
        self.assertIn("GATE_UNCONFIRMED", codes(data))

    def test_current_approval_authorizes_individual_runs_without_mutation(self):
        data = approve(DiscoveryTests.shared_domain_record(), ["CAND-001", "CAND-002"])
        data["approval"]["candidate_ids"].reverse()
        data["runs"] = [run_summary(), run_summary("CAND-002", "SYN-RUN-002")]
        before = copy.deepcopy(data)
        self.assertEqual(validate_discovery(data), [])
        self.assertEqual(data, before)

    def test_fresh_approval_authorizes_manual_run_in_mixed_pool(self):
        data = approve(discovery_fixture())
        data["approval_history"] = [data["approval"]]
        data["runs"] = [run_summary(approval_id="SYN-APPROVAL-001", execution="completed")]
        data["candidates"][0]["status"] = "pending"
        data["candidates"].append(manual_candidate())
        approve(data, ["CAND-002"])
        data["approval"]["id"] = "SYN-APPROVAL-002"
        data["runs"].append(run_summary("CAND-002", "SYN-RUN-002"))

        before = copy.deepcopy(data)
        self.assertEqual(validate_discovery(data), [])
        self.assertEqual(data, before)

    def test_approval_without_selection_is_invalid(self):
        self.assertIn("GATE_SELECTION", codes(approve(discovery_fixture(), ids=[])))

    def test_selection_rejects_unknown_or_excluded_candidates(self):
        for selection, status in ((["UNKNOWN"], "pending"), (["CAND-001"], "excluded")):
            with self.subTest(selection=selection, status=status):
                data = discovery_fixture()
                data["selection"] = selection
                data["candidates"][0]["status"] = status
                self.assertIn("GATE_SELECTION", codes(data))

    def test_approval_must_match_current_selection(self):
        data = approve(DiscoveryTests.shared_domain_record(), ["CAND-001", "CAND-002"])
        data["approval"]["candidate_ids"] = ["CAND-001"]
        self.assertIn("GATE_SELECTION", codes(data))

    def test_approval_requires_boolean_confirmation_and_basis(self):
        for field, value in (("confirmed", 1), ("confirmed", False), ("basis", " ")):
            with self.subTest(field=field, value=value):
                data = approve(discovery_fixture())
                data["approval"][field] = value
                self.assertIn("GATE_UNCONFIRMED", codes(data))

    def test_approval_requires_identifier_and_valid_timestamp_if_present(self):
        for field, value in (("id", ""), ("confirmed_at", "2026-11-10")):
            with self.subTest(field=field):
                data = approve(discovery_fixture())
                data["approval"][field] = value
                self.assertIn("SCHEMA", codes(data))

    def test_stale_approval_cannot_bind_current_configuration(self):
        data = approve(discovery_fixture())
        data["approval"]["snapshot_revision"] = "P2"
        self.assertIn("GATE_REVISION", codes(data))

    def test_current_run_cannot_claim_another_revision(self):
        data = approve(discovery_fixture())
        data["runs"] = [run_summary(revision="P2")]
        self.assertIn("GATE_REVISION", codes(data))

    def test_new_candidate_does_not_inherit_approval(self):
        data = approve(DiscoveryTests.shared_domain_record())
        data["runs"] = [run_summary("CAND-002")]
        self.assertIn("GATE_SELECTION", codes(data))

    def test_duplicate_confirmation_cannot_create_two_runs(self):
        data = approve(discovery_fixture())
        data["runs"] = [run_summary(), run_summary(run_id="SYN-RUN-002")]
        self.assertIn("DUPLICATE_RUN", codes(data))

    def test_run_id_cannot_be_shared_across_candidates(self):
        data = approve(DiscoveryTests.shared_domain_record(), ["CAND-001", "CAND-002"])
        data["runs"] = [run_summary(), run_summary("CAND-002")]
        self.assertIn("DUPLICATE_RUN", codes(data))

    def test_run_summary_validates_target_id_execution_and_pause_shape(self):
        for field, value, code in (
            ("candidate_id", ["CAND-001"], "GATE_TARGET"),
            ("candidate_id", "UNKNOWN", "GATE_TARGET"),
            ("run_id", "", "SCHEMA"),
            ("execution", "unknown", "SCHEMA"),
            ("pause", [], "SCHEMA"),
        ):
            with self.subTest(field=field, value=value):
                data = approve(discovery_fixture())
                data["runs"] = [run_summary()]
                data["runs"][0][field] = value
                self.assertIn(code, codes(data))

    def test_empty_pause_cannot_describe_a_blocked_run(self):
        data = approve(discovery_fixture())
        data["runs"] = [run_summary(execution="blocked", pause={})]
        self.assertIn("SCHEMA", codes(data))

    def test_pause_rejects_malformed_required_fields(self):
        for field, value in (
            ("reason_code", True), ("reason", ""), ("conflicts", {}),
            ("needed_input", None), ("resume_condition", " "),
        ):
            with self.subTest(field=field):
                pause = pause_fixture()
                pause[field] = value
                data = approve(discovery_fixture())
                data["runs"] = [run_summary(execution="blocked", pause=pause)]
                self.assertIn("SCHEMA", codes(data))

    def test_nonidentity_pause_can_have_no_conflicting_claims(self):
        data = approve(discovery_fixture())
        data["runs"] = [run_summary(execution="blocked", pause=pause_fixture())]
        self.assertEqual(validate_discovery(data), [])

    def test_malformed_approval_and_selection_ids_are_diagnosed(self):
        for value in ({}, [{"id": "CAND-001"}], [" "], [None]):
            with self.subTest(value=value):
                data = approve(discovery_fixture())
                data["approval"]["candidate_ids"] = value
                self.assertIn("GATE_SELECTION", codes(data))
        data = discovery_fixture()
        data["selection"] = [["CAND-001"]]
        self.assertIn("GATE_SELECTION", codes(data))

    @staticmethod
    def historical_record():
        data = approve(DiscoveryTests.shared_domain_record())
        data["approval_history"] = [data["approval"]]
        data["snapshot_history"] = [copy.deepcopy(data["snapshot"])]
        data["runs"] = [run_summary(approval_id="SYN-APPROVAL-001")]
        data["snapshot"]["revision"] = "P2"
        for field in ("profile_confirmation", "keyword_confirmation"):
            data["snapshot"][field]["revision"] = "P2"
        data["batches"][1]["snapshot_revision"] = "P2"
        data["candidates"][1]["snapshot_revision"] = "P2"
        data["candidates"][0]["status"] = "pending"
        approve(data, ["CAND-002"])
        data["approval"].update(id="SYN-APPROVAL-002", snapshot_revision="P2")
        data["runs"].append(run_summary("CAND-002", "SYN-RUN-002", "P2"))
        return data

    def test_historical_run_binds_original_snapshot_without_remaining_selected(self):
        self.assertEqual(validate_discovery(self.historical_record()), [])

    def test_historical_run_stays_valid_while_replacement_configuration_is_draft(self):
        for mode in ("discovery", "direct_target"):
            with self.subTest(mode=mode):
                data = self.historical_record()
                data.update(entry_mode=mode, batches=data["batches"][:1],
                            candidates=data["candidates"][:1], selection=[], approval=None,
                            runs=data["runs"][:1], snapshot={"revision": "P2"})
                self.assertEqual(validate_discovery(data), [])

    def test_fresh_approval_can_select_old_candidate_without_changing_provenance(self):
        data = self.historical_record()
        data["selection"] = ["CAND-001"]
        data["approval"]["candidate_ids"] = ["CAND-001"]
        data["runs"][1]["candidate_id"] = "CAND-001"
        self.assertEqual(validate_discovery(data), [])

    def test_retained_approval_must_reference_a_valid_retained_snapshot(self):
        data = self.historical_record()
        del data["snapshot_history"]
        self.assertIn("GATE_REVISION", codes(data))
        data = self.historical_record()
        del data["snapshot_history"][0]["keyword_confirmation"]
        self.assertIn("CONFIG_UNCONFIRMED", codes(data))

    def test_retained_run_requires_an_explicit_known_approval_id(self):
        data = self.historical_record()
        del data["runs"][0]["approval_id"]
        self.assertIn("GATE_UNCONFIRMED", codes(data))
        data = self.historical_record()
        data["runs"][0]["approval_id"] = "MISSING"
        self.assertIn("GATE_UNCONFIRMED", codes(data))

    def test_retained_approval_cannot_authorize_a_different_candidate(self):
        data = self.historical_record()
        data["runs"][0]["candidate_id"] = "CAND-002"
        self.assertIn("GATE_SELECTION", codes(data))

    def test_retained_approval_cannot_authorize_a_different_retained_revision(self):
        data = self.historical_record()
        data["runs"][0]["snapshot_revision"] = "P2"
        self.assertIn("GATE_REVISION", codes(data))

    def test_retained_approval_cannot_be_used_for_current_run_by_omitting_id(self):
        data = approve(discovery_fixture())
        data["approval_history"] = [data["approval"]]
        data["approval"] = None
        data["runs"] = [run_summary()]
        self.assertIn("GATE_UNCONFIRMED", codes(data))
        data["runs"][0]["approval_id"] = "SYN-APPROVAL-001"
        self.assertEqual(validate_discovery(data), [])

    def test_history_cannot_create_ambiguous_approval_or_snapshot_ids(self):
        data = self.historical_record()
        data["approval"]["id"] = "SYN-APPROVAL-001"
        self.assertIn("SCHEMA", codes(data))
        data = self.historical_record()
        data["snapshot_history"].append(copy.deepcopy(data["snapshot"]))
        self.assertIn("GATE_REVISION", codes(data))

    def test_malformed_history_and_run_entries_are_diagnosed(self):
        for field, value in (
            ("snapshot_history", {}),
            ("runs", [None]),
        ):
            with self.subTest(field=field):
                data = discovery_fixture()
                data[field] = value
                self.assertIn("SCHEMA", codes(data))


class EmbeddedGateTests(unittest.TestCase):
    def gate_codes(self, run):
        return {issue["code"] for issue in validate_gate(run)}

    def test_gate_requires_versioned_envelope(self):
        for run in ({}, {"gate": []}, {"gate": {"schema": "unsupported"}}):
            with self.subTest(run=run):
                self.assertIn("GATE_REQUIRED", self.gate_codes(run))

    def test_run_id_cannot_be_its_discovery_id(self):
        run = embedded_run()
        run["run_id"] = run["gate"]["discovery_id"]
        self.assertIn("SCHEMA", self.gate_codes(run))

    def test_valid_gate_binds_exactly_one_member_of_a_larger_approval(self):
        run = embedded_run()
        run["gate"]["approval"]["candidate_ids"].append("CAND-002")
        before = copy.deepcopy(run)
        self.assertEqual(validate_gate(run), [])
        self.assertEqual(run, before)

    def test_run_target_must_match_gate_even_when_both_are_approved(self):
        run = embedded_run()
        run["gate"]["approval"]["candidate_ids"].append("CAND-002")
        run["target"]["candidate_id"] = "CAND-002"
        self.assertIn("GATE_TARGET", self.gate_codes(run))

    def test_gate_candidate_must_be_in_approved_set(self):
        run = embedded_run()
        run["gate"]["approval"]["candidate_ids"] = ["CAND-002"]
        self.assertIn("GATE_SELECTION", self.gate_codes(run))

    def test_gate_requires_final_approval_for_the_embedded_revision(self):
        run = embedded_run()
        run["gate"]["approval"]["snapshot_revision"] = "P2"
        self.assertIn("GATE_REVISION", self.gate_codes(run))
        run["gate"]["approval"] = None
        self.assertIn("GATE_UNCONFIRMED", self.gate_codes(run))

    def test_gate_requires_both_configuration_confirmations(self):
        for field in ("profile_confirmation", "keyword_confirmation"):
            with self.subTest(field=field):
                run = embedded_run()
                del run["gate"]["snapshot"][field]
                self.assertIn("CONFIG_UNCONFIRMED", self.gate_codes(run))


if __name__ == "__main__":
    unittest.main()
