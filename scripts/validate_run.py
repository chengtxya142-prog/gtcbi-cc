"""Check declared research records; cannot verify real-world truth or send messages."""
import argparse
import json
from datetime import date
from pathlib import Path

if __package__:
    from .discovery_contract import validate_gate, validate_identity_pause
else:
    from discovery_contract import validate_gate, validate_identity_pause

VERSION = '2.0.1'


def validate(run, as_of=None, require_gate=False):
    """Check a research record; historical consistency is not execution approval."""
    issues = []
    def add(code, detail):
        issues.append({'code': code, 'detail': detail})
    today = date.fromisoformat(as_of) if as_of else date.today()
    if not isinstance(run, dict):
        return [{'code':'SCHEMA', 'detail':'Run must be an object'}]
    required = {'target':dict, 'profile':dict, 'scope':dict, 'states':dict,
                'contacts':list, 'evidence':list, 'conclusions':list,
                'deliverables':list, 'gaps':list, 'current_action':dict}
    for key, cls in required.items():
        if not isinstance(run.get(key), cls):
            add('SCHEMA', f'{key} must be {cls.__name__}')
    if issues:
        return issues
    if run.get('model_version') != VERSION:
        add('VERSION', 'Expected model_version 2.0.1')
    for key in ('run_id', 'mode', 'route'):
        if not isinstance(run.get(key), str) or not run[key].strip():
            add('SCHEMA', f'Missing {key}')
    if not run['target'].get('entity_id') or not run['target'].get('country'):
        add('SCHEMA', 'Target entity and country required')
    maps = {}
    for collection in ('contacts', 'evidence', 'conclusions', 'deliverables', 'gaps'):
        maps[collection] = {}
        for item in run[collection]:
            if not isinstance(item, dict) or not isinstance(item.get('id'), str) or not item['id'].strip():
                add('SCHEMA', f'{collection}: object with nonempty id required')
                continue
            if item['id'] in maps[collection]:
                add('DUPLICATE_ID', f'{collection}: {item["id"]}')
            maps[collection][item['id']] = item
    if any(i['code'] == 'SCHEMA' for i in issues):
        return issues
    if require_gate or 'gate' in run:
        issues.extend(validate_gate(run))
    target = run['target']
    action = run['current_action']
    blocked_identity = target.get('identity_status') in ('conflict', 'hard_stop')
    if target.get('identity_status') == 'conflict':
        issues.extend(validate_identity_pause(
            run['states'].get('execution'), run.get('identity_conflict'), path='identity_conflict',
        ))
    if blocked_identity and action.get('kind') in ('contact', 'quote', 'sample', 'sign', 'ship'):
        add('IDENTITY_BLOCK', 'Resolve identity before dependent external action')
    verified_people = set()
    for c in run['contacts']:
        credible = (bool(c.get('name')) and c.get('current_role_verified') is True
                    and c.get('relevant_role') is True and bool(c.get('work_route')))
        if credible:
            verified_people.add(c['id'])
        r = c.get('reachability')
        if type(r) is not int or not 0 <= r <= 4:
            add('SCHEMA', f'{c["id"]}: reachability must be integer 0..4')
        elif r >= 3 and not credible:
            add('R3_UNVERIFIED', c['id'])
        if r == 4:
            add('R4_ACCOUNT_ONLY', 'R4 describes ranked account paths; use account_reachability')
    if run.get('account_reachability') == 4:
        ranked = run.get('ranked_contact_ids', [])
        if len(set(ranked) & verified_people) < 2:
            add('R4_COVERAGE', 'R4 requires at least two verified ranked contacts in this schema')
    deliverables = maps['deliverables']
    for d in run['deliverables']:
        if d.get('status') not in ('obtained', 'partial', 'missing', 'not_applicable'):
            add('SCHEMA', f'{d["id"]}: invalid delivery status')
        if d.get('status') == 'not_applicable' and not d.get('reason'):
            add('NA_REASON_MISSING', d['id'])
        if d.get('status') == 'obtained' and d.get('kind') == 'named_person' and d.get('contact_id') not in verified_people:
            add('PERSON_UNVERIFIED', d['id'])
        if d.get('status') == 'obtained' and d.get('kind') == 'personal_profile':
            c = maps['contacts'].get(d.get('contact_id'), {})
            if not c.get('personal_url') or c.get('personal_url_verified') is not True:
                add('PROFILE_UNVERIFIED', d['id'])
    if run['states'].get('research_complete') is True:
        if run['scope'].get('executed') is not True:
            add('SCOPE_NOT_EXECUTED', 'Declared scope not executed')
        required_deliveries = run['scope'].get('required_deliverables')
        if not isinstance(required_deliveries, list) or not required_deliveries:
            add('DELIVERY_MISSING', 'Scope must declare required deliveries')
        else:
            for key in required_deliveries:
                d = deliverables.get(key, {})
                if d.get('status') not in ('obtained', 'not_applicable'):
                    add('DELIVERY_MISSING', str(key))
        if blocked_identity:
            add('UNRESOLVED_CONFLICT', 'Cannot claim general completion with identity conflict')
    open_gaps = [g for g in run['gaps'] if g.get('status') != 'closed']
    routing = [g for g in open_gaps if g.get('impact') == 'routing']
    route = run['route']
    if ((route == 'verify_one_gap' and len(routing) != 1)
        or (route == 'verify_multiple' and len(routing) < 2)
        or (route == 'standard' and routing)):
        add('ROUTING_GAPS', 'Route inconsistent with open decision-changing gaps')
    for g in open_gaps:
        if action.get('ready') is True and action.get('kind') in g.get('affected_actions', []):
            add('ACTION_BLOCKED', g['id'])
    for e in run['evidence']:
        if e.get('source') in run['profile'].get('blocked_sources', []):
            add('SOURCE_BLOCKED', e['id'])
        try:
            checked = date.fromisoformat(e.get('checked_on', ''))
            if checked > today:
                add('EVIDENCE_DATE', e['id'])
            if e.get('expires_on') and date.fromisoformat(e['expires_on']) < today:
                add('EVIDENCE_STALE', e['id'])
        except (ValueError, TypeError):
            add('EVIDENCE_DATE', e['id'])
    for q in run['conclusions']:
        refs = q.get('evidence_ids', [])
        if not isinstance(refs, list):
            add('SCHEMA', f'{q["id"]}: evidence_ids must be a list')
            continue
        if q.get('status') == 'verified' and not refs:
            add('EVIDENCE_MISSING', q['id'])
        for ref in refs:
            e = maps['evidence'].get(ref)
            if e is None:
                add('EVIDENCE_MISSING', f'{q["id"]}: {ref}')
                continue
            if e.get('entity_id') != target.get('entity_id') and not e.get('relationship_explanation'):
                add('EVIDENCE_ENTITY', ref)
            if q.get('status') == 'verified' and e.get('status') != 'verified':
                add('EVIDENCE_UNVERIFIED', ref)
    if run.get('score') is not None:
        if run['profile'].get('scoring_enabled') is not True:
            add('SCORING_DISABLED', 'Score supplied without enabled scoring profile')
        else:
            # Industry formulas are intentionally not invented by this generic validator.
            add('SCORING_REVIEW_REQUIRED', 'Validate score with the approved industry scoring implementation')
    draft = run.get('draft') or {}
    if draft.get('kind') == 'named' and draft.get('recipient_id') not in verified_people:
        add('NAMED_DRAFT_UNVERIFIED', str(draft.get('recipient_id')))
    for ref in draft.get('claim_ids', []):
        q = maps['conclusions'].get(ref)
        if q is None:
            add('DRAFT_CLAIM_MISSING', ref)
        elif q.get('status') != 'verified':
            add('DRAFT_CLAIM_UNVERIFIED', ref)
    if run['states'].get('sent') is True:
        sends = run.get('actual_sends', [])
        if not any(isinstance(s, dict) and s.get('source') and s.get('sent_at') for s in sends):
            add('SEND_EVIDENCE_MISSING', 'Draft alone is not proof of sending')
    return issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', type=Path)
    parser.add_argument('--as-of', help='YYYY-MM-DD, defaults to today')
    parser.add_argument('--require-gate', action='store_true',
                        help='Require an embedded gate for new execution records')
    args = parser.parse_args()
    try:
        result = validate(json.loads(args.run.read_text(encoding='utf-8-sig')), args.as_of,
                          require_gate=args.require_gate)
    except (OSError, ValueError, TypeError) as exc:
        result = [{'code':'INPUT_ERROR', 'detail':str(exc)}]
    print(json.dumps({'model_version':VERSION, 'issues':result}, ensure_ascii=False, indent=2))
    return 1 if result else 0


if __name__ == '__main__':
    raise SystemExit(main())
