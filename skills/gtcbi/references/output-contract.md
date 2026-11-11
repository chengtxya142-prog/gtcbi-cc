# Output contract / 输出契约 — V2.0.2

Lead with follow / conditional follow / defer / stop, the main opportunity and risk, conditions for changing the decision, and the current action. State evidence limitations close to affected conclusions. Do not require a numerical score.

The [five-field candidate format](discovery-and-gate.md#discover-and-display) is for the pre-research pool; it is not a formal finding or an extra required worksheet. Candidate selection and approval, research execution and required deliverables, draft readiness, cooperation conditions, actual handoff, and each requested export's status stay separate. A pure export retains the original research scope, dates and statuses.

## Four-sheet workbook layout

| Sheet | Required content |
| --- | --- |
| 客户基本信息 | Target/company identity, source, actual check dates, seller configuration, model/profile/Run IDs, scope/mode and required deliverables |
| 客户背调结果 | Decision; F1–F6; Why now; routing; buyer/seller comparison; contacts and independent verification fields; evidence register; gaps with action impact; separate completion states; current/subsequent actions |
| 邮件跟进 | Optional company-referral or verified named-person draft; factual claim IDs; one CTA; draft/sent/reply evidence separately; configurable follow-up timing |
| 数据映射 | Stable field keys, input-to-conclusion mappings, source/claim links and diagnostics; no diagnostic output feeds facts or business decisions |

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

The bundled `examples/` files are the JSON interchange reference; see [discovery record](discovery-record.md) for optional discovery and gate fields. `evidence` and `conclusions` use stable IDs; `scope.required_deliverables` lists delivery IDs; `gaps.affected_actions` uses contact/quote/sample/sign/ship or declared internal actions. `current_action.ready` describes readiness, not execution. Profile-approved N/A requires an explanation.

Research dates use ISO YYYY-MM-DD. Synthetic records must set `synthetic: true` and identify fictional entities. The JSON schema used by the lightweight checker is intentionally conservative; richer host records may require an adapter and semantic review.

## 中文

四表结构与 V2.0 结果方向一致；增加独立交付状态、Why now、多缺口动作影响和时效。勾稽不能只数证据行数，也不能反向生成“完成”状态。未启用邮件时明确未启用；已生成邮件只标草稿。受限信息保留事实边界，禁止用漂亮模板掩盖未完成交付。
