import copy
import sys
import unittest
from pathlib import Path

from discovery_fixtures import discovery_fixture

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from discovery_contract import normalize_domain, validate_discovery


def codes(record):
    return {issue["code"] for issue in validate_discovery(record)}


def additional_batch():
    return {
        "id": "B2", "kind": "additional", "requested_count": 3,
        "quantity_basis": "operator", "actual_count": 0,
        "candidate_ids": [], "snapshot_revision": "P1",
        "shortfall_reason": "No new synthetic sources",
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
        for timestamp in ("not a time", "2026-11-10", "2026-02-30T13:30:00Z"):
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


if __name__ == "__main__":
    unittest.main()
