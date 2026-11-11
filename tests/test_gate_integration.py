import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

from discovery_fixtures import approve, discovery_fixture

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from discovery_contract import validate_discovery
from validate_run import validate

AS_OF = "2026-11-10"


def identity_conflict():
    return {
        "reason": "The synthetic directory and register disagree about the entity.",
        "conflicts": [
            {"claim": "The site belongs to Example Trading Ltd", "source": "Synthetic directory"},
            {"claim": "The site belongs to Example Services Ltd", "source": "Synthetic register"},
        ],
        "needed_input": "The intended legal entity's registration number",
        "resume_condition": "Recheck the registration and website against the intended entity",
    }


def codes(issues):
    return {issue["code"] for issue in issues}


class GateIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.run = json.loads(
            (ROOT / "examples" / "synthetic-run.json").read_text(encoding="utf-8")
        )

    def test_historical_validation_stays_compatible(self):
        self.assertEqual(validate(self.run, AS_OF), [])

    def test_new_execution_requires_gate(self):
        self.assertIn("GATE_REQUIRED", codes(validate(self.run, AS_OF, require_gate=True)))

    def test_synthetic_gated_example_passes_strict_validation(self):
        run = json.loads(
            (ROOT / "examples" / "synthetic-gated-run.json").read_text(encoding="utf-8")
        )
        self.assertIs(run["synthetic"], True)
        self.assertEqual(validate(run, AS_OF, require_gate=True), [])

    def test_present_gate_is_checked_even_without_strict_mode(self):
        data = approve(discovery_fixture())
        self.run["gate"] = {
            "schema": "discovery-gate-v1", "discovery_id": data["discovery_id"],
            "candidate_id": "CAND-001", "snapshot": data["snapshot"], "approval": data["approval"],
        }
        self.run["target"]["candidate_id"] = "CAND-002"
        self.assertEqual(codes(validate(self.run, AS_OF)), {"GATE_TARGET"})

    def test_strict_cli_reports_missing_gate_for_historical_record(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_run.py"),
             str(ROOT / "examples" / "synthetic-run.json"), "--as-of", AS_OF, "--require-gate"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("GATE_REQUIRED", codes(json.loads(result.stdout)["issues"]))

    def mark_identity_conflict(self):
        self.run["target"]["identity_status"] = "conflict"
        self.run["states"]["execution"] = "blocked"
        self.run["current_action"] = {
            "kind": "clarify_identity", "ready": False,
            "text": "Wait for operator clarification",
        }

    def test_identity_conflict_requires_explanation(self):
        self.mark_identity_conflict()
        self.assertIn("IDENTITY_REASON_REQUIRED", codes(validate(self.run, AS_OF)))

    def test_identity_conflict_requires_all_explanation_fields(self):
        self.mark_identity_conflict()
        for field, value in (("reason", " "), ("needed_input", None), ("resume_condition", True)):
            with self.subTest(field=field):
                self.run["identity_conflict"] = identity_conflict()
                self.run["identity_conflict"][field] = value
                self.assertEqual(codes(validate(self.run, AS_OF)), {"IDENTITY_REASON_REQUIRED"})

    def test_identity_conflict_requires_at_least_two_distinct_well_formed_claims(self):
        self.mark_identity_conflict()
        first, second = identity_conflict()["conflicts"]
        for conflicts in (
            None, [], [first], [first, {**first, "source": "Different source"}],
            [first, {**second, "claim": "  "}], [first, {**second, "source": "  "}],
            [first, second, None],
        ):
            with self.subTest(conflicts=conflicts):
                self.run["identity_conflict"] = {**identity_conflict(), "conflicts": conflicts}
                self.assertEqual(codes(validate(self.run, AS_OF)), {"IDENTITY_EVIDENCE_REQUIRED"})

    def test_identity_conflict_cannot_stay_active(self):
        self.mark_identity_conflict()
        self.run["identity_conflict"] = identity_conflict()
        for execution in (None, "running", "completed"):
            with self.subTest(execution=execution):
                self.run["states"]["execution"] = execution
                self.assertEqual(codes(validate(self.run, AS_OF)), {"IDENTITY_NOT_PAUSED"})

    def test_explained_identity_pause_needs_no_unknown_dates(self):
        self.mark_identity_conflict()
        self.run["identity_conflict"] = identity_conflict()
        for execution in ("blocked", "stopped"):
            with self.subTest(execution=execution):
                self.run["states"]["execution"] = execution
                before = copy.deepcopy(self.run)
                self.assertEqual(validate(self.run, AS_OF), [])
                self.assertEqual(self.run, before)

    def test_identity_pause_still_blocks_external_action_and_completion(self):
        self.mark_identity_conflict()
        self.run["identity_conflict"] = identity_conflict()
        self.run["states"]["research_complete"] = True
        self.run["deliverables"][1].update(status="not_applicable", reason="Identity unresolved")
        self.run["current_action"].update(kind="contact", ready=True)
        self.assertEqual(codes(validate(self.run, AS_OF)), {"IDENTITY_BLOCK", "UNRESOLVED_CONFLICT"})


class DiscoveryIdentityPauseTests(unittest.TestCase):
    def setUp(self):
        self.record = approve(discovery_fixture())
        self.run = {
            "run_id": "SYN-RUN-001", "candidate_id": "CAND-001",
            "snapshot_revision": "P1", "execution": "blocked",
            "pause": {"reason_code": "identity_conflict", **identity_conflict()},
        }
        self.record["runs"] = [self.run]

    def test_candidate_identity_pause_requires_explanation(self):
        for field in ("reason", "needed_input", "resume_condition"):
            with self.subTest(field=field):
                self.run["pause"] = {"reason_code": "identity_conflict", **identity_conflict()}
                del self.run["pause"][field]
                self.assertIn("IDENTITY_REASON_REQUIRED", codes(validate_discovery(self.record)))

    def test_candidate_identity_pause_requires_conflicting_claims(self):
        self.run["pause"]["conflicts"] = []
        self.assertEqual(codes(validate_discovery(self.record)), {"IDENTITY_EVIDENCE_REQUIRED"})

    def test_candidate_identity_pause_cannot_stay_active(self):
        self.run["execution"] = "running"
        self.assertEqual(codes(validate_discovery(self.record)), {"IDENTITY_NOT_PAUSED"})

    def test_blocked_candidate_does_not_change_or_block_another_run(self):
        second = copy.deepcopy(self.record["candidates"][0])
        second.update(id="CAND-002", entity_key="SYN-BUYER-2-GB", name="Second Synthetic Buyer")
        self.record["candidates"].append(second)
        self.record["batches"][0].update(candidate_ids=["CAND-001", "CAND-002"], actual_count=2)
        approve(self.record, ["CAND-001", "CAND-002"])
        self.record["runs"].append({
            "run_id": "SYN-RUN-002", "candidate_id": "CAND-002",
            "snapshot_revision": "P1", "execution": "running", "pause": None,
        })
        before = copy.deepcopy(self.record)
        self.assertEqual(validate_discovery(self.record), [])
        self.assertEqual(self.record, before)
