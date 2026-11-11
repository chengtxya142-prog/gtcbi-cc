---
name: gtcbi
description: Use when finding B2B prospects or continuing a candidate list, researching or updating named companies (客户背调), assessing supplier-buyer fit, verifying business contact paths, or exporting evidence-backed customer investigations.
---

# Global Trade Customer Background Investigation V2.0.1

## Entry

For prospect discovery or new named targets, read [discovery and execution gate](references/discovery-and-gate.md) first.

1. Check relevant host capabilities. Prefill only retrievable default seller context; confirm or edit a run-specific snapshot without changing defaults.
2. Recommend editable keywords or accept operator-only terms; obtain keyword confirmation before prospect discovery.
3. Show ten candidates initially by default; require an explicit quantity for each additional batch. Show unchecked candidates with company, country, website, preliminary match reason and inspected discovery source.
4. Wait for explicit selection plus final start confirmation before researching any candidate. A missing UI control is not permission: use candidate IDs and explicit textual confirmation.
5. For already named targets, use the same configuration and execution gate without requiring a discovery batch. Export-only work bypasses new research.
6. After approval, create one run per selected customer and continue the existing scoped F1–F6 workflow.

## Research and delivery

Read [operating rules](references/rules.md) before research and [output contract](references/output-contract.md) for delivery.

1. Declare entity, country, scope, mode, required deliverables and source restrictions. Read existing records before researching.
2. Verify identity first; follow the pause rule for conflicts. Research business, procurement and timing; then choose a route based on evidence and gaps.
3. Match depth to purpose. Preserve useful evidence. Budget exhaustion does not fulfill a required deliverable.
4. Compare buyer conditions with seller capabilities. Separate facts, hypotheses, unknowns and conflicts. Report which action each gap affects.
5. Independently report execution, deliverables, draft readiness, cooperation conditions and handoff. Default to no numerical score.
6. Refresh only affected facts when new evidence arrives; preserve historical dates and judgments. Apply the execution gate to newly scoped research, not a pure export.
7. Produce the requested output. The optional outreach module is draft-only; actual contact is a separate action, not part of research approval.

Do not transfer a source workflow's module number, fixed headcount, query quota or unapproved scoring policy into this generic model. Apply configured source exclusions before source selection. Read-only authorization does not authorize outreach or CRM writes.

For optional structured JSON and offline checking, see [discovery record](references/discovery-record.md). A pass is not authorization or proof of evidence quality.

## 中文入口

适用于跨行业 B2B 客户发现、客户背调、联系人路径核验、合作可行性判断和定向更新。发现或新指定客户先读[执行门](references/discovery-and-gate.md)；正式研究、交付、文案就绪、实际发送分别判断。禁止把未知当负面、把检索结束当取得目标、把岗位线索当已验证个人。
