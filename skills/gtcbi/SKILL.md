---
name: gtcbi
description: Use when finding B2B prospects or continuing a candidate list, researching or updating named companies, assessing supplier-buyer fit, verifying business contact paths, or exporting evidence-backed customer investigations. 适用于外贸找客户、开发客户、继续找一批候选、客户背调/背景调查、核实公司主体、联系人与采购路径核验、合作可行性判断、导出背调报告、把背调结果保存或同步到 Twenty CRM。
compatibility: Works with any Agent Skills host (Codex, Claude Code, Claude.ai, Hermes, Gemini CLI). Web search/source reading depend on host tools; optional validators need Python 3.10+.
metadata:
  version: "2.0.4"
  author: chengtxya142-prog
  homepage: https://github.com/chengtxya142-prog/gtcbi-cc
---

# Global Trade Customer Background Investigation V2.0.4

## Entry

For prospect discovery or new named targets, read [discovery and execution gate](references/discovery-and-gate.md) first.

1. Check relevant host capabilities. Then confirm who the operator is: show the operator profile card (`PROFILE-r1`: company, industry, products, markets, customer types, cooperation objective) unchecked, prefilled only from retrievable defaults, and wait for explicit confirmation. No mode, named target or time pressure skips this; with no default, ask and wait. Edits change this run's snapshot, not the defaults.
2. Recommend editable keywords or accept operator-only terms; obtain keyword confirmation before prospect discovery.
3. Show ten candidates initially by default; require an explicit quantity for each additional batch. Show unchecked candidates with company, country, website, preliminary match reason and inspected discovery source.
4. Wait for explicit selection plus final start confirmation before researching any candidate. A missing UI control is not permission: use candidate IDs and explicit textual confirmation.
5. For already named targets, use the same profile confirmation, configuration and execution gate without requiring a discovery batch. Export-only work bypasses new research.
6. After approval, create one run per selected customer and continue the existing scoped F1–F6 workflow.

## Research and delivery

Read [operating rules](references/rules.md) before research and [output contract](references/output-contract.md) for delivery. For F1 identity and domain checks, [official sources](references/official-sources.md) is an optional starting list.

1. Declare entity, country, scope, mode, required deliverables and source restrictions. Read existing records before researching.
2. Verify identity first, including any operator-supplied email domain against the official domain; follow the pause rule for conflicts. Research business, procurement and timing; then choose a route based on evidence and gaps.
3. Match depth to purpose. Preserve useful evidence. Budget exhaustion does not fulfill a required deliverable.
4. Compare buyer conditions with seller capabilities. Separate facts, hypotheses, unknowns and conflicts. Report which action each gap affects.
5. Independently report execution, deliverables, draft readiness, cooperation conditions and handoff. Default to no numerical score.
6. Refresh only affected facts when new evidence arrives; preserve historical dates and judgments. Apply the execution gate to newly scoped research, not a pure export.
7. Produce the requested output. If the current action is to contact the target and no draft was requested, ask once whether to draft it. The optional outreach module is draft-only; actual contact is a separate action, not part of research approval.

Do not transfer a source workflow's module number, fixed headcount, query quota or unapproved scoring policy into this generic model. Apply configured source exclusions before source selection. Read-only authorization and research approval do not authorize outreach or CRM writes.

## Optional CRM sync

To save results into a Twenty CRM workspace, read [Twenty CRM sync](references/crm-twenty.md) first. It is a separate, one-way action after research: check that Twenty tools are really connected, show the write plan, and write only after explicit confirmation of that plan. Without a connected CRM, say so and export instead.

For optional structured JSON and offline checking, see [discovery record](references/discovery-record.md). A pass is not authorization or proof of evidence quality.

## 中文入口

适用于跨行业 B2B 客户发现、客户背调、联系人路径核验、合作可行性判断和定向更新。发现或新指定客户先读[执行门](references/discovery-and-gate.md)；开始前必须先展示操作人画像卡（公司、行业、产品、目标市场、客户类型、合作目标）并取得明确确认，如“确认画像 PROFILE-r1”，任何模式都不能跳过；正式研究、交付、文案就绪、实际发送分别判断。禁止把未知当负面、把检索结束当取得目标、把岗位线索当已验证个人。需要把结果写入 Twenty CRM 时先读 [CRM 同步](references/crm-twenty.md)：单向写入，先展示写入计划并取得明确确认。
