import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "skills" / "gtcbi"
sys.path.insert(0, str(ROOT / 'scripts'))
from validate_run import validate


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.run = json.loads((ROOT / 'examples' / 'synthetic-run.json').read_text(encoding='utf-8'))

    def codes(self):
        return {item['code'] for item in validate(self.run, '2026-11-09')}

    def test_valid_conditional_research(self):
        self.assertEqual(self.codes(), set())

    def test_missing_target(self):
        del self.run['target']
        self.assertIn('SCHEMA', self.codes())

    def test_identity_conflict_blocks_contact(self):
        self.run['target']['identity_status'] = 'conflict'
        self.assertIn('IDENTITY_BLOCK', self.codes())

    def test_unnamed_role_is_not_r3(self):
        self.run['contacts'][0]['reachability'] = 3
        self.assertIn('R3_UNVERIFIED', self.codes())

    def test_verified_person_can_refer_without_authority(self):
        c = self.run['contacts'][0]
        c.update(name='Synthetic Person', current_role_verified=True, relevant_role=True, reachability=3)
        self.assertEqual(self.codes(), set())

    def test_profile_url_not_verified(self):
        self.run['deliverables'].append({'id':'profile', 'status':'obtained', 'kind':'personal_profile', 'contact_id':'C1'})
        self.assertIn('PROFILE_UNVERIFIED', self.codes())

    def test_budget_exhausted_not_complete(self):
        self.run['states']['research_complete'] = True
        self.assertIn('DELIVERY_MISSING', self.codes())

    def test_two_gaps_are_not_single(self):
        self.run['route'] = 'verify_one_gap'
        for gap in self.run['gaps']:
            gap['impact'] = 'routing'
        self.assertIn('ROUTING_GAPS', self.codes())

    def test_transaction_gap_allows_contact(self):
        self.assertEqual(self.codes(), set())

    def test_transaction_gap_blocks_quote(self):
        self.run['current_action']['kind'] = 'quote'
        self.assertIn('ACTION_BLOCKED', self.codes())

    def test_wrong_entity_evidence(self):
        self.run['evidence'][0]['entity_id'] = 'OTHER'
        self.assertIn('EVIDENCE_ENTITY', self.codes())

    def test_missing_evidence_id(self):
        self.run['conclusions'][0]['evidence_ids'] = ['E999']
        self.assertIn('EVIDENCE_MISSING', self.codes())

    def test_required_conclusion_without_support(self):
        self.run['conclusions'][0]['evidence_ids'] = []
        self.assertIn('EVIDENCE_MISSING', self.codes())

    def test_restricted_evidence_not_verified(self):
        self.run['evidence'][0]['status'] = 'restricted'
        self.assertIn('EVIDENCE_UNVERIFIED', self.codes())

    def test_blocked_source(self):
        self.run['profile']['blocked_sources'] = ['synthetic-material']
        self.assertIn('SOURCE_BLOCKED', self.codes())

    def test_stale_evidence_flagged(self):
        self.run['evidence'][0]['expires_on'] = '2026-10-01'
        self.assertIn('EVIDENCE_STALE', self.codes())

    def test_future_evidence_rejected(self):
        self.run['evidence'][0]['checked_on'] = '2027-01-01'
        self.assertIn('EVIDENCE_DATE', self.codes())

    def test_scores_off_by_default(self):
        self.run['score'] = {'total':90}
        self.assertIn('SCORING_DISABLED', self.codes())

    def test_draft_does_not_mean_sent(self):
        self.run['states']['sent'] = True
        self.assertIn('SEND_EVIDENCE_MISSING', self.codes())

    def test_named_draft_requires_verified_person(self):
        self.run['draft']['kind'] = 'named'
        self.assertIn('NAMED_DRAFT_UNVERIFIED', self.codes())

    def test_draft_claim_must_exist(self):
        self.run['draft']['claim_ids'] = ['Q999']
        self.assertIn('DRAFT_CLAIM_MISSING', self.codes())

    def test_duplicate_evidence(self):
        self.run['evidence'].append(copy.deepcopy(self.run['evidence'][0]))
        self.assertIn('DUPLICATE_ID', self.codes())

    def test_missing_scope_is_not_complete(self):
        self.run['scope']['executed'] = False
        self.run['states']['research_complete'] = True
        self.assertIn('SCOPE_NOT_EXECUTED', self.codes())

    def test_na_requires_reason(self):
        self.run['deliverables'][0]['status'] = 'not_applicable'
        self.run['deliverables'][0]['reason'] = ''
        self.assertIn('NA_REASON_MISSING', self.codes())

    def test_version_mismatch(self):
        self.run['model_version'] = '2.0'
        self.assertIn('VERSION', self.codes())


if __name__ == '__main__':
    unittest.main()
