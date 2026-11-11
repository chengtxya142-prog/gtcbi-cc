"""Validate offline discovery records without changing them or authorizing research."""

from datetime import date
from urllib.parse import urlsplit


def normalize_domain(url: str | None) -> str | None:
    """Return a domain as a duplicate clue, never an entity decision."""
    if not isinstance(url, str) or not url.strip():
        return None
    try:
        host = urlsplit(url).hostname
    except ValueError:
        return None
    if not host:
        return None
    host = host.lower().rstrip(".").removeprefix("www.")
    return host or None


def _issue(code, detail):
    return {"code": code, "detail": detail}


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _texts(value, *, nonempty=False):
    return (isinstance(value, list) and (not nonempty or bool(value))
            and all(_text(item) for item in value))


def _valid_quantity(value):
    return type(value) is int and value > 0


def _web_url(value):
    if not _text(value) or any(char.isspace() for char in value):
        return False
    try:
        parts = urlsplit(value)
        return parts.scheme in ("http", "https") and bool(normalize_domain(value))
    except ValueError:
        return False


def _iso_date(value):
    if not isinstance(value, str):
        return False
    try:
        return date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def _validate_snapshot(snapshot, *, require_confirmed):
    if not isinstance(snapshot, dict):
        return [_issue("SCHEMA", "snapshot must be an object")]

    issues = []
    revision = snapshot.get("revision")
    if not _text(revision):
        issues.append(_issue("SCHEMA", "snapshot.revision must be a nonblank string"))

    for field in ("company", "industry", "cooperation_objective"):
        value = snapshot.get(field)
        if not _text(value) and (require_confirmed or value is not None):
            issues.append(_issue("SCHEMA", f"snapshot.{field} must be a nonblank string"))
    for field in ("products", "markets", "customer_types"):
        value = snapshot.get(field)
        if (require_confirmed or value is not None) and not _texts(
            value, nonempty=require_confirmed
        ):
            issues.append(_issue("SCHEMA", f"snapshot.{field} requires valid terms"))

    keywords = snapshot.get("keywords")
    if isinstance(keywords, dict):
        for field in ("include", "exclude", "provenance"):
            if not _texts(keywords.get(field), nonempty=(
                require_confirmed and field in ("include", "provenance")
            )):
                issues.append(_issue("SCHEMA", f"snapshot.keywords.{field} requires valid terms"))
    elif require_confirmed or keywords is not None:
        issues.append(_issue("SCHEMA", "snapshot.keywords must be an object"))

    for field in ("profile_confirmation", "keyword_confirmation"):
        confirmation = snapshot.get(field)
        if not isinstance(confirmation, dict) or confirmation.get("confirmed") is not True:
            if require_confirmed:
                issues.append(_issue("CONFIG_UNCONFIRMED", f"snapshot.{field} requires confirmation"))
            elif confirmation is not None and (
                not isinstance(confirmation, dict) or confirmation.get("confirmed") is not False
            ):
                issues.append(_issue("SCHEMA", f"snapshot.{field} requires a Boolean confirmed value"))
            continue
        if not _text(confirmation.get("basis")):
            issues.append(_issue("CONFIG_UNCONFIRMED", f"snapshot.{field} requires a confirmation basis"))
        if not _text(confirmation.get("revision")) or confirmation["revision"] != revision:
            issues.append(_issue("CONFIG_REVISION", f"snapshot.{field} must confirm the snapshot revision"))
        timestamp = confirmation.get("confirmed_at")
        if timestamp is not None and not _text(timestamp):
            issues.append(_issue("SCHEMA", f"snapshot.{field}.confirmed_at must be a string or null"))

    return issues


def _validate_batches(batches, revision):
    issues = []
    batch_ids = set()
    membership = {}

    for index, batch in enumerate(batches):
        path = f"batches[{index}]"
        if not isinstance(batch, dict):
            issues.append(_issue("SCHEMA", f"{path} must be an object"))
            continue
        batch_id = batch.get("id")
        if not _text(batch_id) or batch_id in batch_ids:
            issues.append(_issue("SCHEMA", f"{path}.id must be a unique nonblank string"))
        else:
            batch_ids.add(batch_id)
        kind = "initial" if index == 0 else "additional"
        if batch.get("kind") != kind:
            issues.append(_issue("SCHEMA", f"{path}.kind must be {kind}"))
        requested = batch.get("requested_count")
        basis = batch.get("quantity_basis")
        if not _valid_quantity(requested) or not (
            basis == "operator" or (index == 0 and basis == "default" and requested == 10)
        ):
            issues.append(_issue("BATCH_QUANTITY", f"{path} requires a positive operator quantity or the initial default of 10"))

        actual = batch.get("actual_count")
        ids = batch.get("candidate_ids")
        if type(actual) is not int or actual < 0 or (
            isinstance(ids, list) and actual != len(ids)
        ) or (_valid_quantity(requested) and actual > requested):
            issues.append(_issue("BATCH_COUNT", f"{path}.actual_count must match the listed IDs and not exceed the requested count"))
        if type(actual) is int and 0 <= actual and _valid_quantity(requested) and actual < requested:
            if not _text(batch.get("shortfall_reason")):
                issues.append(_issue("SHORTFALL_REASON", f"{path} requires a shortfall reason"))

        batch_revision = batch.get("snapshot_revision")
        if not _text(batch_revision) or batch_revision != revision:
            issues.append(_issue("CONFIG_REVISION", f"{path} must reference the snapshot revision"))
        if not _texts(ids):
            issues.append(_issue("SCHEMA", f"{path}.candidate_ids must be a list of nonblank IDs"))
            continue
        for candidate_id in ids:
            if candidate_id in membership:
                issues.append(_issue("DUPLICATE_CANDIDATE", f"{path} lists candidate {candidate_id!r} again"))
            else:
                membership[candidate_id] = batch_revision

    return issues, membership


def _validate_candidates(candidates, revision, membership, *, discovered):
    issues = []
    candidate_ids = set()
    entity_keys = set()
    for index, candidate in enumerate(candidates):
        path = f"candidates[{index}]"
        if not isinstance(candidate, dict):
            issues.append(_issue("SCHEMA", f"{path} must be an object"))
            continue
        for field in ("id", "name", "match_reason", "entity_key"):
            if not _text(candidate.get(field)):
                issues.append(_issue("SCHEMA", f"{path}.{field} must be a nonblank string"))

        candidate_id = candidate.get("id")
        candidate_revision = candidate.get("snapshot_revision")
        if not _text(candidate_revision) or candidate_revision != revision:
            issues.append(_issue("CONFIG_REVISION", f"{path} must reference the snapshot revision"))
        if _text(candidate_id):
            if candidate_id in candidate_ids:
                issues.append(_issue("DUPLICATE_CANDIDATE", f"{path} repeats candidate ID {candidate_id!r}"))
            candidate_ids.add(candidate_id)
            if discovered and candidate_id not in membership:
                issues.append(_issue("SCHEMA", f"{path} is not listed in a discovery batch"))
            if candidate_id in membership and membership[candidate_id] != candidate_revision:
                issues.append(_issue("CONFIG_REVISION", f"{path} must match its batch revision"))

        entity_key = candidate.get("entity_key")
        if _text(entity_key):
            if entity_key in entity_keys:
                issues.append(_issue("DUPLICATE_ENTITY", f"{path} repeats entity key {entity_key!r}"))
            entity_keys.add(entity_key)

        country = candidate.get("country")
        if country is not None and not _text(country):
            issues.append(_issue("SCHEMA", f"{path}.country must be a string or null"))
        website = candidate.get("website")
        if website is not None and not _web_url(website):
            issues.append(_issue("SCHEMA", f"{path}.website must be a web URL or null"))
        if candidate.get("status") not in ("pending", "selected", "excluded"):
            issues.append(_issue("SCHEMA", f"{path}.status must be pending, selected, or excluded"))

        sources = candidate.get("sources")
        from_batch = _text(candidate_id) and candidate_id in membership
        if not isinstance(sources, list) or ((discovered or from_batch) and not sources):
            issues.append(_issue("SCHEMA", f"{path}.sources requires a list of read sources for discovery"))
        else:
            for source_index, source in enumerate(sources):
                if not isinstance(source, dict) or not (
                    _web_url(source.get("url")) and source.get("access_state") == "read"
                    and _iso_date(source.get("checked_on"))
                ):
                    issues.append(_issue("SCHEMA", f"{path}.sources[{source_index}] requires a read web source and a checked_on date"))

    for candidate_id in membership:
        if candidate_id not in candidate_ids:
            issues.append(_issue("SCHEMA", f"Batch references unknown candidate {candidate_id!r}"))
    return issues


def validate_discovery(record: dict) -> list[dict[str, str]]:
    """Return structural and discovery diagnostics; do not repair input."""
    if not isinstance(record, dict):
        return [_issue("SCHEMA", "discovery record must be an object")]

    issues = []
    for field, expected in (("model_version", "2.0.1"), ("discovery_schema", "discovery-gate-v1")):
        if record.get(field) != expected:
            issues.append(_issue("SCHEMA", f"{field} must be {expected}"))
    if "synthetic" in record and type(record["synthetic"]) is not bool:
        issues.append(_issue("SCHEMA", "synthetic must be a Boolean"))
    if not _text(record.get("discovery_id")):
        issues.append(_issue("SCHEMA", "discovery_id must be a nonblank string"))
    mode = record.get("entry_mode")
    if mode not in ("discovery", "direct_target"):
        issues.append(_issue("SCHEMA", "entry_mode must be discovery or direct_target"))
    snapshot = record.get("snapshot")
    if not isinstance(snapshot, dict):
        issues.append(_issue("SCHEMA", "snapshot must be an object"))
    for field in ("batches", "candidates", "selection", "approval_history", "runs"):
        if not isinstance(record.get(field), list):
            issues.append(_issue("SCHEMA", f"{field} must be a list"))
    approval = record.get("approval")
    if "approval" not in record or (approval is not None and not isinstance(approval, dict)):
        issues.append(_issue("SCHEMA", "approval must be an object or null"))
    if issues:
        return issues

    batches = record["batches"]
    candidates = record["candidates"]
    activity = bool(batches or candidates or record["selection"] or approval is not None or record["runs"])
    issues = _validate_snapshot(snapshot, require_confirmed=activity)
    revision = snapshot.get("revision")
    batch_issues, membership = _validate_batches(batches, revision)
    issues.extend(batch_issues)
    issues.extend(_validate_candidates(candidates, revision, membership, discovered=mode == "discovery"))
    return issues
