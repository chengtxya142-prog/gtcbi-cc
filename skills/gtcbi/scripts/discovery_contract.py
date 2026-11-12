"""Validate offline discovery records without changing them or authorizing research."""

from datetime import date, datetime
import re
from urllib.parse import urlsplit


_GATE_SCHEMA = "discovery-gate-v1"
_EXECUTION_STATES = ("not_started", "running", "completed", "partial", "blocked", "stopped")


def normalize_domain(url: str | None) -> str | None:
    """Return a domain as a duplicate clue, never an entity decision."""
    if not isinstance(url, str) or not url.strip():
        return None
    try:
        parts = urlsplit(url)
        _ = parts.port  # urlsplit validates explicit ports only when accessed.
        host = parts.hostname
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


def _iso_datetime(value):
    if not isinstance(value, str) or not re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}[T ][0-9]{2}:[0-9]{2}"
        r"(?::[0-9]{2}(?:\.[0-9]+)?)?(?:Z|[+-](?:[01][0-9]|2[0-3]):[0-5][0-9])?",
        value,
    ):
        return False
    try:
        datetime.fromisoformat(value[:-1] + "+00:00" if value.endswith("Z") else value)
    except ValueError:
        return False
    return True


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
        if timestamp is not None and not _iso_datetime(timestamp):
            issues.append(_issue("SCHEMA", f"snapshot.{field}.confirmed_at must be an ISO 8601 datetime or null"))

    return issues


def _validate_batches(batches, revisions):
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
        if not _text(batch_revision) or batch_revision not in revisions:
            issues.append(_issue("CONFIG_REVISION", f"{path} must reference a retained snapshot revision"))
        if not _texts(ids):
            issues.append(_issue("SCHEMA", f"{path}.candidate_ids must be a list of nonblank IDs"))
            continue
        for candidate_id in ids:
            if candidate_id in membership:
                issues.append(_issue("DUPLICATE_CANDIDATE", f"{path} lists candidate {candidate_id!r} again"))
            else:
                membership[candidate_id] = batch_revision

    return issues, membership


def _validate_candidates(candidates, revisions, membership, *, discovery_mode):
    issues = []
    statuses = {}
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
        from_batch = _text(candidate_id) and candidate_id in membership
        origin = candidate.get("origin", "discovered" if discovery_mode or from_batch else "manual")
        if origin not in ("manual", "discovered"):
            issues.append(_issue("SCHEMA", f"{path}.origin must be manual or discovered"))
        elif origin == "manual" and from_batch:
            issues.append(_issue("SCHEMA", f"{path} is manual and must not belong to a discovery batch"))
        elif origin == "discovered" and not from_batch:
            issues.append(_issue("SCHEMA", f"{path} is not listed in a discovery batch"))

        candidate_revision = candidate.get("snapshot_revision")
        if not _text(candidate_revision) or candidate_revision not in revisions:
            issues.append(_issue("CONFIG_REVISION", f"{path} must reference a retained snapshot revision"))
        if _text(candidate_id):
            if candidate_id in statuses:
                issues.append(_issue("DUPLICATE_CANDIDATE", f"{path} repeats candidate ID {candidate_id!r}"))
            else:
                statuses[candidate_id] = candidate.get("status")
            if from_batch and membership[candidate_id] != candidate_revision:
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
        if not isinstance(sources, list) or (origin == "discovered" and not sources):
            issues.append(_issue("SCHEMA", f"{path}.sources requires a list of read sources for discovery"))
        else:
            for source_index, source in enumerate(sources):
                if not isinstance(source, dict) or not (
                    _web_url(source.get("url")) and source.get("access_state") == "read"
                    and _iso_date(source.get("checked_on"))
                ):
                    issues.append(_issue("SCHEMA", f"{path}.sources[{source_index}] requires a read web source and a checked_on date"))

    for candidate_id in membership:
        if candidate_id not in statuses:
            issues.append(_issue("SCHEMA", f"Batch references unknown candidate {candidate_id!r}"))
    return issues, statuses


def _validate_snapshot_history(history, revision):
    issues = []
    revisions = {revision} if _text(revision) else set()
    for index, snapshot in enumerate(history):
        path = f"snapshot_history[{index}]"
        for issue in _validate_snapshot(snapshot, require_confirmed=True):
            issues.append(_issue(issue["code"], f"{path}: {issue['detail']}"))
        old_revision = snapshot.get("revision") if isinstance(snapshot, dict) else None
        if _text(old_revision):
            if old_revision in revisions:
                issues.append(_issue("GATE_REVISION", f"{path}.revision must not repeat a snapshot revision"))
            revisions.add(old_revision)
    return issues, revisions


def _validate_approval(approval, path, revisions):
    if not isinstance(approval, dict):
        return [_issue("GATE_UNCONFIRMED", f"{path} requires final confirmation")], None

    issues = []
    if approval.get("confirmed") is not True or not _text(approval.get("basis")):
        issues.append(_issue("GATE_UNCONFIRMED", f"{path} requires final confirmation and its basis"))
    if not _text(approval.get("id")):
        issues.append(_issue("SCHEMA", f"{path}.id must be a nonblank string"))
    timestamp = approval.get("confirmed_at")
    if timestamp is not None and not _iso_datetime(timestamp):
        issues.append(_issue("SCHEMA", f"{path}.confirmed_at must be an ISO 8601 datetime or null"))
    revision = approval.get("snapshot_revision")
    if not _text(revision) or revision not in revisions:
        issues.append(_issue("GATE_REVISION", f"{path} must reference the applicable snapshot revision"))

    ids = approval.get("candidate_ids")
    if not _texts(ids, nonempty=True):
        issues.append(_issue("GATE_SELECTION", f"{path}.candidate_ids must be a nonempty list of nonblank IDs"))
        return issues, None
    return issues, set(ids)


def _validate_approvals(record, statuses, revision, revisions):
    issues = []
    selected = record["selection"]
    if not _texts(selected) or any(
        item not in statuses or statuses[item] == "excluded" for item in selected
    ):
        issues.append(_issue("GATE_SELECTION", "selection must list only known, non-excluded candidate IDs"))
        selected = None
    else:
        selected = set(selected)

    entries = [
        (f"approval_history[{index}]", approval)
        for index, approval in enumerate(record["approval_history"])
    ]
    if record["approval"] is not None:
        entries.insert(0, ("approval", record["approval"]))

    approvals = {}
    for path, approval in entries:
        current = path == "approval"
        approval_issues, ids = _validate_approval(
            approval, path, (revision,) if current else revisions
        )
        issues.extend(approval_issues)
        if ids is not None:
            if current and (not selected or ids != selected):
                issues.append(_issue("GATE_SELECTION", "approval must match the nonempty current selection"))
            elif not current and not ids.issubset(statuses):
                issues.append(_issue("GATE_SELECTION", f"{path} includes an unknown candidate ID"))
        approval_id = approval.get("id") if isinstance(approval, dict) else None
        if _text(approval_id):
            if approval_id in approvals:
                issues.append(_issue("SCHEMA", f"{path}.id must not repeat an approval ID"))
            else:
                approvals[approval_id] = (approval.get("snapshot_revision"), ids)
    return issues, approvals


def validate_execution_state(execution, *, path):
    """Check the shared execution-state vocabulary for a declared run."""
    if execution not in _EXECUTION_STATES:
        return [_issue("SCHEMA", f"{path} must be a recognized execution state")]
    return []


def validate_identity_pause(execution, conflict, *, execution_path, conflict_path):
    """Check the declared execution state, explanation, and conflicting claims."""
    issues = []
    if execution not in ("blocked", "stopped"):
        issues.append(_issue("IDENTITY_NOT_PAUSED", f"{execution_path} must be blocked or stopped"))

    conflict = conflict if isinstance(conflict, dict) else {}
    fields = ("reason", "needed_input", "resume_condition")
    missing = [field for field in fields if not _text(conflict.get(field))]
    if missing:
        issues.append(_issue("IDENTITY_REASON_REQUIRED", f"{conflict_path} requires: {', '.join(missing)}"))

    claims = conflict.get("conflicts")
    if (not isinstance(claims, list)
            or not all(isinstance(item, dict) and _text(item.get("claim"))
                       and _text(item.get("source")) for item in claims)
            or len({" ".join(item["claim"].casefold().split()) for item in claims}) < 2):
        issues.append(_issue("IDENTITY_EVIDENCE_REQUIRED",
                             f"{conflict_path}.conflicts requires at least two distinct claims with sources"))
    return issues


def _validate_runs(record, statuses, revision, revisions, approvals):
    issues = []
    run_ids = set()
    targets = set()
    current_id = (record["approval"] or {}).get("id")
    for index, run in enumerate(record["runs"]):
        path = f"runs[{index}]"
        if not isinstance(run, dict):
            issues.append(_issue("SCHEMA", f"{path} must be an object"))
            continue
        run_id = run.get("run_id")
        if not _text(run_id) or run_id == record["discovery_id"]:
            issues.append(_issue("SCHEMA", f"{path}.run_id must be nonblank and distinct from discovery_id"))
        elif run_id in run_ids:
            issues.append(_issue("DUPLICATE_RUN", f"{path} repeats run ID {run_id!r}"))
        else:
            run_ids.add(run_id)
        execution = run.get("execution")
        issues.extend(validate_execution_state(execution, path=f"{path}.execution"))
        pause = run.get("pause")
        if pause is not None and not isinstance(pause, dict):
            issues.append(_issue("SCHEMA", f"{path}.pause must be an object or null"))
        elif isinstance(pause, dict) and pause.get("reason_code") == "identity_conflict":
            issues.extend(validate_identity_pause(
                execution, pause, execution_path=f"{path}.execution", conflict_path=f"{path}.pause",
            ))
        elif isinstance(pause, dict):
            for field in ("reason_code", "reason", "needed_input", "resume_condition"):
                if not _text(pause.get(field)):
                    issues.append(_issue("SCHEMA", f"{path}.pause.{field} must be a nonblank string"))
            if not isinstance(pause.get("conflicts"), list):
                issues.append(_issue("SCHEMA", f"{path}.pause.conflicts must be a list"))

        candidate_id = run.get("candidate_id")
        known_candidate = _text(candidate_id) and candidate_id in statuses
        if not known_candidate:
            issues.append(_issue("GATE_TARGET", f"{path} must bind one known candidate ID"))
        run_revision = run.get("snapshot_revision")
        if not _text(run_revision) or run_revision not in revisions:
            issues.append(_issue("GATE_REVISION", f"{path} must reference a retained snapshot revision"))
        elif known_candidate:
            target = (candidate_id, run_revision)
            if target in targets:
                issues.append(_issue("DUPLICATE_RUN", f"{path} repeats candidate {candidate_id!r} at revision {run_revision!r}"))
            targets.add(target)

        # Without an explicit ID a run can only use the current approval.
        approval_id = run.get("approval_id", current_id if run_revision == revision else None)
        if not _text(approval_id) or approval_id not in approvals:
            issues.append(_issue("GATE_UNCONFIRMED", f"{path} requires a matching final approval"))
            continue
        approved_revision, approved_ids = approvals[approval_id]
        if run_revision != approved_revision:
            issues.append(_issue("GATE_REVISION", f"{path} must use its approved snapshot revision"))
        if known_candidate and (approved_ids is None or candidate_id not in approved_ids):
            issues.append(_issue("GATE_SELECTION", f"{path} candidate was not selected in its approval"))
    return issues


def validate_gate(run: dict) -> list[dict[str, str]]:
    """Check a research run's embedded approval and snapshot, not its authenticity."""
    gate = run.get("gate") if isinstance(run, dict) else None
    if not isinstance(gate, dict) or gate.get("schema") != _GATE_SCHEMA:
        return [_issue("GATE_REQUIRED", f"run requires an embedded {_GATE_SCHEMA} gate")]

    issues = []
    discovery_id = gate.get("discovery_id")
    if not _text(discovery_id):
        issues.append(_issue("GATE_REQUIRED", "gate.discovery_id must be a nonblank string"))
    elif run.get("run_id") == discovery_id:
        issues.append(_issue("SCHEMA", "run_id must be distinct from gate.discovery_id"))
    candidate_id = gate.get("candidate_id")
    target = run.get("target")
    if not _text(candidate_id) or not isinstance(target, dict) or target.get("candidate_id") != candidate_id:
        issues.append(_issue("GATE_TARGET", "run.target.candidate_id must match gate.candidate_id"))

    snapshot = gate.get("snapshot")
    issues.extend(_validate_snapshot(snapshot, require_confirmed=True))
    revision = snapshot.get("revision") if isinstance(snapshot, dict) else None
    approval_issues, approved_ids = _validate_approval(gate.get("approval"), "gate.approval", (revision,))
    issues.extend(approval_issues)
    if _text(candidate_id) and approved_ids is not None and candidate_id not in approved_ids:
        issues.append(_issue("GATE_SELECTION", "gate.candidate_id must be included in its approval"))
    return issues


def validate_discovery(record: dict) -> list[dict[str, str]]:
    """Return structural and discovery diagnostics; do not repair input."""
    if not isinstance(record, dict):
        return [_issue("SCHEMA", "discovery record must be an object")]

    issues = []
    for field, expected in (("model_version", "2.0.5"), ("discovery_schema", _GATE_SCHEMA)):
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
    history = record.get("snapshot_history", [])
    if not isinstance(history, list):
        issues.append(_issue("SCHEMA", "snapshot_history must be a list"))
    approval = record.get("approval")
    if "approval" not in record or (approval is not None and not isinstance(approval, dict)):
        issues.append(_issue("SCHEMA", "approval must be an object or null"))
    if issues:
        return issues

    batches = record["batches"]
    candidates = record["candidates"]
    direct_target = mode == "direct_target"
    revision = snapshot.get("revision")
    # Historical activity does not confirm a replacement draft or require it to be confirmed.
    activity = bool((direct_target and not candidates) or record["selection"] or approval is not None or any(
        isinstance(item, dict) and item.get("snapshot_revision") == revision
        for group in (batches, candidates, record["runs"], record["approval_history"])
        for item in group
    ))
    issues = _validate_snapshot(snapshot, require_confirmed=activity)
    if direct_target and not candidates:
        issues.append(_issue("SCHEMA", "direct_target requires at least one candidate"))
    history_issues, revisions = _validate_snapshot_history(history, revision)
    issues.extend(history_issues)
    batch_issues, membership = _validate_batches(batches, revisions)
    issues.extend(batch_issues)
    candidate_issues, statuses = _validate_candidates(
        candidates, revisions, membership, discovery_mode=mode == "discovery"
    )
    issues.extend(candidate_issues)
    approval_issues, approvals = _validate_approvals(record, statuses, revision, revisions)
    issues.extend(approval_issues)
    issues.extend(_validate_runs(record, statuses, revision, revisions, approvals))
    return issues
