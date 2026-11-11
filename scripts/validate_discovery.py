"""Validate declared discovery records; no search, authorization or sending."""

import argparse
import json
from pathlib import Path

from discovery_contract import validate_discovery


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    args = parser.parse_args()

    try:
        data = json.loads(args.record.read_text(encoding="utf-8-sig"))
        issues = validate_discovery(data)
    except (OSError, ValueError, TypeError) as exc:
        issues = [{"code": "INPUT_ERROR", "detail": str(exc)}]

    print(json.dumps(
        {"model_version": "2.0.1", "issues": issues},
        ensure_ascii=False, indent=2,
    ))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
