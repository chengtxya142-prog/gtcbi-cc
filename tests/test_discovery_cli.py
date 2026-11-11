import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SYNTHETIC_RECORD = ROOT / "examples/synthetic-discovery.json"


class DiscoveryCliTests(unittest.TestCase):
    def run_validator(self, path, expected_exit_code):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_discovery.py"), str(path)],
            capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(result.returncode, expected_exit_code, result.stderr)
        self.assertEqual(result.stderr, "")
        payload = json.loads(result.stdout)
        self.assertEqual(payload["model_version"], "2.0.1")
        return payload["issues"]

    def test_synthetic_pending_example(self):
        self.assertEqual(self.run_validator(SYNTHETIC_RECORD, 0), [])

    def test_accepts_utf8_bom(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "with-bom.json"
            path.write_text(SYNTHETIC_RECORD.read_text(encoding="utf-8"), encoding="utf-8-sig")
            self.assertEqual(self.run_validator(path, 0), [])

    def test_missing_file_has_json_error(self):
        with tempfile.TemporaryDirectory() as temp:
            issues = self.run_validator(Path(temp) / "missing.json", 1)
        self.assertEqual(issues[0]["code"], "INPUT_ERROR")

    def test_non_record_inputs_get_schema_errors(self):
        for body in ("[]", "{}"):
            with self.subTest(body=body), tempfile.TemporaryDirectory() as temp:
                path = Path(temp) / "not-a-record.json"
                path.write_text(body, encoding="utf-8")
                issues = self.run_validator(path, 1)
                self.assertEqual(issues[0]["code"], "SCHEMA")

    def test_malformed_json_has_json_error(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "malformed.json"
            path.write_text('{"model_version":', encoding="utf-8")
            issues = self.run_validator(path, 1)
        self.assertEqual(issues[0]["code"], "INPUT_ERROR")

    def test_deeply_nested_malformed_json_has_json_error(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "nested.json"
            path.write_text("[" * 12_000, encoding="utf-8")
            issues = self.run_validator(path, 1)
        self.assertEqual(issues[0]["code"], "INPUT_ERROR")

    def test_rejects_non_json_number_tokens_even_in_unvalidated_fields(self):
        record = SYNTHETIC_RECORD.read_text(encoding="utf-8").rstrip()
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "non-json-number.json"
            for token in ("NaN", "Infinity", "-Infinity"):
                with self.subTest(token=token):
                    path.write_text(record[:-1] + f', "extra": {token}}}', encoding="utf-8")
                    issues = self.run_validator(path, 1)
                    self.assertEqual(issues[0]["code"], "INPUT_ERROR")
