# Optional discovery and research gate records — V2.0.3

The host can record actual dialogue actions in an authorized conversation or file; the operator need not fill in JSON. Follow [discovery and execution gate](discovery-and-gate.md) to obtain confirmations first. An offline record, including a plausible `basis`, cannot grant permission to search, research or contact anyone.

## Discovery JSON

| Field | Content |
| --- | --- |
| `discovery_schema`, `model_version` | `"discovery-gate-v1"`, `"2.0.3"`. Set `synthetic: true` for fictional records; keep real records private. |
| `discovery_id`, `entry_mode` | Nonblank task ID distinct from individual run IDs; `discovery` or `direct_target`. Direct-target records require a candidate, not a search batch. |
| `snapshot` | Current configuration object; see below. |
| `snapshot_history` | Optional list of complete, confirmed earlier snapshots with unique revisions distinct from the current one. Retain any snapshot referenced by earlier batches, candidates, approvals or runs. |
| `batches`, `candidates` | Lists of discovery batches and pool entries; see below. |
| `selection` | List of known non-excluded candidate IDs currently selected; not final approval. |
| `approval` | `null` until final confirmation, or the current approval object. |
| `approval_history` | List of prior approval objects, not grants for the current selection. |
| `runs` | List of per-customer run summaries, not full reports; see below. |

**Snapshot.** Use a nonblank `revision`. In a confirmed snapshot, `company`, `industry` and `cooperation_objective` are nonblank strings; `products`, `markets` and `customer_types` are nonempty lists of nonblank terms. `keywords` is an object with term lists `include` (nonempty), `exclude` (may be empty) and `provenance` (nonempty, e.g. `["operator"]` or `["recommended", "operator"]`). The `profile_confirmation` and `keyword_confirmation` objects use Boolean `confirmed` and, when confirmed, matching `revision`, nonblank actual `basis` and an available `confirmed_at` or `null`. A new snapshot with no current activity can be a draft; historical activity neither confirms nor overwrites it.

**Batch.** Use `id`, `kind` (`initial` then `additional`), positive integer `requested_count`, `quantity_basis` (`default` only for the first batch at 10, otherwise `operator`), `actual_count`, `candidate_ids`, `snapshot_revision`, and `shortfall_reason` (nonblank if fewer than requested). The actual count equals the number of listed IDs and cannot exceed the request. Keep actual search scope and date in the host's record.

**Candidate.** Use `id`, `name`, `country` (nullable), `website` (web URL or `null`), `match_reason`, `sources`, `entity_key`, `status` (`pending`, `selected`, `excluded`), `snapshot_revision`, and optional `origin` (`manual` or `discovered`). If omitted, origin defaults to `discovered` in discovery mode or for a batched candidate; otherwise an unbatched direct target defaults to `manual`. Discovered candidates require batch membership and at least one actually inspected source. Manually supplied targets may coexist in the same pool as `origin: "manual"`; do not list them in a discovery batch or count them toward its quantity. An unbatched manual target can have `sources: []` if no source was read, but still requires the normal configuration and approval before research. Each recorded source uses direct web `url`, `access_state: "read"` and actual `checked_on` (YYYY-MM-DD). Do not invent a source for missing data. Keep `entity_key` unique for each entity in the pool; a domain alone is not an entity identifier.

**Approval and run.** An approval has unique `id`, `candidate_ids`, `snapshot_revision`, `basis`, Boolean `confirmed: true`, and `confirmed_at` if available (otherwise `null`). Current approval must exactly match the nonempty current selection and snapshot revision. Confirmation timestamps are real ISO 8601 calendar datetimes with a time component, optionally with an offset or `Z` (e.g. `2026-11-10T13:30:00Z`), not date-only strings; syntax does not authenticate them.

Each summary has unique `run_id`, one `candidate_id`, `snapshot_revision`, `execution` (`not_started`, `running`, `completed`, `partial`, `blocked`, `stopped`), `pause` (object or `null`), and optional `approval_id`. The candidate and revision must match that run's approval; do not duplicate a candidate at the same revision. Omitted `approval_id` can bind only the current approval. An existing historical run must name its retained approval via `approval_id` and use the retained snapshot when its revision is no longer current; it need not stay in current selection. A newly approved run may use an existing candidate without rewriting the candidate's or batch's original discovery revision.

## Full research JSON and identity pause

New full research records add `gate` with `schema: "discovery-gate-v1"`, `discovery_id`, `candidate_id`, the approved `snapshot` and its `approval`. Match `target.candidate_id` to `gate.candidate_id`, and set `states.execution` to the run's actual state. Do not replace the approved snapshot with the latest one.

In a discovery summary, a non-null `pause` contains `reason_code`, `reason`, `conflicts` (list), `needed_input` and `resume_condition`. For an F1 identity conflict, use `reason_code: "identity_conflict"` and set `execution` to `blocked` (or `stopped` if stopped). In a full run use `target.identity_status: "conflict"`, `states.execution: "blocked"` (or `"stopped"`), and the explanation in `identity_conflict`. In both formats include at least two distinct claims with `claim` and `source`, plus entity scope and date where known; record affected conclusions/steps, needed input and the resume condition. Do not claim completion or recommend dependent external action while identity is unresolved.

## Offline checks and diagnostics

Run from this skill's folder (the directory containing `SKILL.md`), so the commands work wherever the skill is installed:

```bash
python scripts/validate_discovery.py examples/synthetic-discovery.json
python scripts/validate_run.py examples/synthetic-gated-run.json --require-gate
```

Each CLI prints JSON with `model_version` and an `issues` list of `code` and `detail`; exit 0 means no detected issues, exit 1 means issues. The discovery CLI uses `INPUT_ERROR` for unreadable or invalid JSON. The research checker also accepts historical records without `gate` when `--require-gate` is omitted, but checks any embedded gate. A missing historical gate does not establish past or present approval.

| Diagnostics | What to inspect |
| --- | --- |
| `SCHEMA`, `CONFIG_UNCONFIRMED`, `CONFIG_REVISION` | Field shapes and source format, both actual confirmations and configuration revision references. |
| `BATCH_QUANTITY`, `BATCH_COUNT`, `SHORTFALL_REASON`, `DUPLICATE_CANDIDATE`, `DUPLICATE_ENTITY` | Count source, batch membership, reported shortfall and repeated candidate/entity IDs. |
| `GATE_REQUIRED`, `GATE_UNCONFIRMED`, `GATE_SELECTION`, `GATE_REVISION`, `GATE_TARGET`, `DUPLICATE_RUN` | Missing or unsupported gate, confirmation, selected set, approval/snapshot revision, target binding or duplicate run. |
| `IDENTITY_NOT_PAUSED`, `IDENTITY_REASON_REQUIRED`, `IDENTITY_EVIDENCE_REQUIRED` | Execution not blocked/stopped, missing pause explanation, or fewer than two distinct sourced claims. Existing research checks also flag `IDENTITY_BLOCK` and `UNRESOLVED_CONFLICT`. |

The checkers read self-reported data. They do not authenticate an operator or timestamp, establish that a source was read, compare a standalone gate with an independent approval ledger, prove evidence quality, execute a run or authorize external actions. Review actual evidence and deliverables using the [output contract](output-contract.md).
