# Prospect discovery and execution gate — V2.0.3

Discovery yields leads, selection marks intent, and final confirmation authorizes formal research for a specific set of targets and one configuration revision. None authorizes outreach.

## Route the request and check capabilities

- For new prospect discovery, check the host's authorized search, source reading, interaction and file capabilities, then confirm the configuration below. Checking capability is not prospect research. Do not assume a provider, a working multiselect, or a save/export facility.
- For named targets, use the same operator profile confirmation, configuration and approval gate, but add the supplied targets manually; do not force a discovery batch. A company name alone is not final approval. Show its candidate ID and mark unsupplied or unverified facts as such; do not invent a discovery source. Give it the next unused sequential candidate ID, and ask for any known country or website because F1 identity checks need them; missing values do not block registration or the gate.
- To continue an already approved run or refresh affected facts within its existing target, configuration and scope, reuse that run's approved snapshot and evidence. New targets, material configuration changes and new research scope require current approval; historical records alone do not establish that approval.
- For candidate-list or existing-report export only, use the existing records; do not discover prospects, request new approval or restart research. Preserve original dates, scope and statuses. If a required capability is unavailable, report exactly what could not be done. Distinguish a record in the conversation from an actually saved file or export. In a candidate-list export, label a tentative selection as selected but not approved, so the file is never read as research authorization.

## Confirm the operator profile first

Before recommending keywords, searching for prospects, asking for a start confirmation or researching anything about a target, show the operator's own background as one profile card and obtain explicit confirmation of it. This applies to discovery and to named targets, in every mode: a quick identity-only or targeted check still needs it, because the decision, gaps and next action are judged from the seller's side. Never offer a way to start without it, and do not start because the operator is in a hurry or says to decide for them.

Display the card unchecked, the same way candidates are displayed, with a stable ID that carries the snapshot revision:

```text
- [ ] PROFILE-r1 | Supplying company name
  - Industry:
  - Products/services:
  - Target markets:
  - Customer types:
  - Cooperation objective:
  - Constraints (MOQ, price, lead time, certification, language; optional):
  - Source of these values:
```

- The first six fields are required. Fill only what is retrievable from a known default or supplied by the operator, and name that source. Mark every other field `未提供` and ask for it; never guess a field from the target's industry, an email signature or earlier conversations about other companies. Unknown constraints stay `未知`; they do not block confirmation.
- With no retrievable default, say so, show the empty card and wait for the operator's answers. Registering a named target as a candidate may happen meanwhile; nothing else may.
- Confirmation is explicit text for exactly that card, e.g. “确认画像 PROFILE-r1”. Viewing the card, naming a target, selecting candidates or silence is not confirmation. One message may confirm the profile, select candidates and confirm the start if each part is unambiguous. Record the actual basis in `profile_confirmation`.
- Within the same session an already confirmed, unchanged profile is reused: restate its ID and one-line summary instead of asking again. Any edit produces a new revision (`PROFILE-r2`) that needs its own confirmation.
- A confirmed card is this run's snapshot, not a saved default. Save or change a persistent default only on a distinct explicit request and only in the host's private storage, never in the public repository; without such storage, ask again in the next session.
- Not required for: exporting existing records, continuing an already approved run within its scope, or a CRM sync of finished results.
- **Profile confirmed after research already exists** (for example a run made under an older version of these rules, or before the operator gave their background): keep earlier evidence, dates and statuses. Re-evaluate under the newly confirmed card using that existing evidence only, without new searching, and label the result as a re-evaluation under `PROFILE-rN`. Earlier follow/defer decisions, preliminary match reasons, gap priorities and next actions do not carry over; re-judge each of them from the seller's side, and say plainly when the decision is unchanged and why. An identity conflict stays in force regardless of the profile. Any new searching or new modules under the new card need an explicit start confirmation for that target; a request such as “深入查” counts if it names the target. Record each re-evaluation as a new entry; never rewrite the earlier one.

## Confirm the run-specific configuration

1. Use the confirmed profile card as the seller part of the snapshot. Show the supplying company's name, industry and products/services, target markets, customer types and cooperation objective, plus relevant constraints. Prefill only retrievable defaults with a known source. Collect missing decision-critical inputs; do not invent seller facts. Allow a temporary switch of company, industry, products or other fields. Confirm the run-specific snapshot separately; only a distinct explicit request may change persistent defaults.
2. Offer editable keyword recommendations, or use only operator-supplied terms when requested. Product, synonym, channel, use case, role, competitor, local-language and exclusion terms are options, not required categories. The operator may add, edit, remove or replace any term. Do not restore deleted terms or reject free terms for not matching a preset vocabulary.
3. Show the final include/exclude pack and obtain explicit confirmation **before searching for prospects**. Record its actual recommendation/operator provenance and confirmation basis. A vague “continue” on an unconfirmed pack means ask for confirmation, not search. Reuse confirmed settings without asking again when unchanged.
4. On a material change (such as seller company, product, market or keyword meaning), make a new immutable revision; confirm its profile and keywords and obtain new final approval before using it for formal research. Keep earlier snapshots, discovery provenance, approvals and runs intact. Old approvals do not transfer to a new revision or changed selection. Preliminary match reasons from the old revision do not carry over either: tell the operator that existing candidates were screened under the old configuration, and recheck their fit under the new one (or let the operator reselect) before asking for final approval.

## Discover and display

- The initial batch targets **10 companies by default**; use a positive integer override explicitly provided by the operator. Each additional batch requires a positive integer supplied for that batch. If missing, zero, negative or non-integer, ask for a valid count and do not begin that batch, even if the operator says to decide for them.
- Inspect an official website or another reliable, authorized source for each discovered lead and check its basic identity and preliminary fit. Search-result snippets alone are leads, not inspected sources. Do not assign commercial grades, buying intent or budgets or start formal F1–F6 during discovery.
- Deduplicate against all previously shown, selected and excluded entities. Use normalized company name, country, known aliases and legal/entity scope; normalize website domain (e.g. protocol, `www` and query variations do not make different entities). A shared group domain is a clue, not proof that different legal entities are the same. Keep stable, sequential candidate IDs across batches and reordering.
- Treat the count as a result target, not a search quota or permission for unlimited search. Record requested and actual counts, actual search scope and dates, and the stopping or shortfall reason. Return only substantiated candidates if sources, access or budget are insufficient; never pad the batch.

Display each new candidate unchecked with a stable ID and these five business fields. Use an actually inspected direct link; mark uncertain country or website as unverified, not guessed. For a manual target with no inspected source, say it was operator-supplied and not independently checked.

```text
- [ ] CAND-001 | Company name
  - Country:
  - Website:
  - Preliminary match reason:
  - Discovery source:
```

## Select and approve

The operator can select one or more candidates, confirm research, request a further batch with a count, stop discovery and retain the pool, add named targets to the same pool, or export it. Manual additions are not discovery batch results. Leave candidates pending by default; an unchecked candidate is not excluded.

- Use blank real multiselect controls only if the host supports them and returns selection events; require a final start action. Otherwise show static unchecked entries and use stable IDs plus explicit text, e.g. “选择 CAND-001、CAND-003，确认开始背调”. Do not pretend static Markdown is clickable or guess at control events. A selection and final start confirmation may be in the same message if the intended IDs are unambiguous.
- Start formal research **only** when the current operator profile card and keyword pack are confirmed, the operator has explicitly selected at least one valid non-excluded candidate, and the operator explicitly confirms starting for exactly that set. Selection alone waits; do not begin even F1 or a preliminary formal check from supplied evidence. Viewing, adding, exporting, more search, editing keywords and silence are not approval.
- Capture the exact selected IDs, revision, actual confirmation basis and real timestamp if available. Do not invent times or operator quotes. If the set changes, get a fresh final confirmation; new candidates cannot inherit an earlier approval. Replaying the same confirmation never duplicates a run. [Optional JSON and checks](discovery-record.md) record real interactions; they do not create them.

## Hand off and track independently

Create one distinct run per approved customer; fix the approved snapshot, scope and required deliverables. Recheck relevant tool/source access, read applicable records and follow the [existing F1–F6 sequence](rules.md#sequence-and-routing). Reuse applicable inspected discovery sources only after assessing entity, timing and support. A preliminary match reason is not a research conclusion.

Keep entry progress (profile pending, keywords pending, discovering, awaiting selection/start, approved) separate from each client's execution and from deliverables, draft readiness, cooperation conditions, actual handoff and export status. Follow the [formal output contract](output-contract.md). An optional outreach request produces a draft only; do not send, invite/connect, submit a form or write to a CRM as part of the workflow. Saving results to a CRM is a separate action with its own confirmation; see [Twenty CRM sync](crm-twenty.md). Drafting does not change sent, reply or meeting states.

## Pause, stop and recover

- If F1 reveals a material identity conflict, label that client “主体冲突” (`identity_conflict`) and block **all** formal investigation of that client, even evidence collection that seems independent. Keep existing evidence. Record the specific mismatch; both claims and sources, with entity scopes and dates where known; affected conclusions/steps; input needed; and the condition for resuming. A conflict is not a low-credibility verdict. On clarification, recheck identity first; resume only when the condition is met and approval is still applicable. Continue other approved clients independently.
- When the operator stops discovery, retain the pool and do not begin another batch. When the operator stops remaining research, stop affected queued work and any affected active work at the next safe opportunity; preserve completed results and acquired evidence, and report exactly what stopped. A single-client failure affects that run, not the others.
- If a source is inaccessible, record the source, cause if known and what remains unverified. Use other applicable authorized sources where allowed; do not bypass access controls or ask for passwords, verification codes or session credentials. If tools fail, report the actual state and any next input needed. Keep private default profiles and real customer data out of the public repository.
