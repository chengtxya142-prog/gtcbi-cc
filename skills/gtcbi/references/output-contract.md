# Output contract / �����Լ �� V2.0.1

Lead with follow / conditional follow / defer / stop, the main opportunity and risk, conditions for changing the decision, and the current action. State evidence limitations close to affected conclusions. Do not require a numerical score.

## Four-sheet workbook layout

| Sheet | Required content |
| --- | --- |
| �ͻ�������Ϣ | Target/company identity, source, actual check dates, seller configuration, model/profile/Run IDs, scope/mode and required deliverables |
| �ͻ�������� | Decision; F1�CF6; Why now; routing; buyer/seller comparison; contacts and independent verification fields; evidence register; gaps with action impact; separate completion states; current/subsequent actions |
| �ʼ����� | Optional company-referral or verified named-person draft; factual claim IDs; one CTA; draft/sent/reply evidence separately; configurable follow-up timing |
| ����ӳ�� | Stable field keys, input-to-conclusion mappings, source/claim links and diagnostics; no diagnostic output feeds facts or business decisions |

Preserve original valid details on edits. No customer records are included with this package. This contract is not an XLSX file or export implementation. Use the host's supported document/spreadsheet tools when a user requests exports, then validate values, statuses and references across formats.

## Mandatory content review

- Does every decisive claim have appropriate evidence for the correct entity, country and period? Evaluate support and counter-evidence, not just reference existence.
- Is the stated certainty supported? Source assertions and hypotheses remain labeled.
- Do required deliverables remain visibly missing when not obtained?
- Is the current action allowed by unresolved conditions, with its preconditions named?
- Are named-person claims and email promises within the verified facts and seller capabilities?
- Are actual sends/replies supported separately from drafts?
- Do versions and dates reflect actual research or only a template change?

Evidence count, action count, nonempty cells and successful formulas do not prove any of these. The offline validator catches a subset of contradictions; a pass is not a research-completion certificate.

## Structured interchange

The repository example is the JSON interchange reference. `evidence` and `conclusions` use stable IDs; `scope.required_deliverables` lists delivery IDs; `gaps.affected_actions` uses contact/quote/sample/sign/ship or declared internal actions. `current_action.ready` describes readiness, not execution. Profile-approved N/A requires an explanation.

Dates use ISO YYYY-MM-DD. Synthetic records must set `synthetic: true` and identify fictional entities. The JSON schema used by the lightweight checker is intentionally conservative; richer host records may require an adapter and semantic review.

## ����

�ı��ṹ�� V2.0 �������һ�£����Ӷ�������״̬��Why now����ȱ�ڶ���Ӱ���ʱЧ����������ֻ��֤��������Ҳ���ܷ������ɡ���ɡ�״̬��δ�����ʼ�ʱ��ȷδ���ã��������ʼ�ֻ��ݸ塣������Ϣ������ʵ�߽磬��ֹ��Ư��ģ���ڸ�δ��ɽ�����
