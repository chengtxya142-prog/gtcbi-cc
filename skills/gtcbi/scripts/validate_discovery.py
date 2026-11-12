"""Validate declared discovery records; no search, authorization or sending."""

import argparse
import json
from pathlib import Path

from discovery_contract import validate_discovery


def _reject_non_json_constant(token):
    raise ValueError(f"{token} is not a valid JSON number")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    args = parser.parse_args()

    try:
        data = json.loads(
            args.record.read_text(encoding="utf-8-sig"),
            parse_constant=_reject_non_json_constant,
        )
    except (OSError, ValueError, RecursionError) as exc:
        issues = [{"code": "INPUT_ERROR", "detail": str(exc)}]
    else:
        issues = validate_discovery(data)

    print(json.dumps(
        {"model_version": "2.0.4", "issues": issues},
        ensure_ascii=False, indent=2,
    ))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
