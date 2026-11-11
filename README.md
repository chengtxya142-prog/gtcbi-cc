# GTCBI V2.0.1

Global Trade Customer Background Investigation: a cross-industry research skill with evidence-based decisions, configurable research depth, and optional outreach drafts.

This is a new standalone implementation of the agreed V2.0.1 rules. It is not a recovered copy of the previous V2.0 repository. No customer records, private Notion pages, credentials, or prior Git history are included.

## Use

Open [the skill entrypoint](skills/gtcbi/SKILL.md) with your agent, or copy the entire `skills/gtcbi` directory into the skill directory supported by your agent. For Claude/Gemini or another assistant, supply this entrypoint and the referenced files as project context. No platform-specific installer is claimed.

1. **Discover prospects by industry:** Confirm the seller company, industry, products, target markets, customer types and cooperation objective. Use known defaults or temporarily switch to another company, industry or product for this run; only a separate explicit request changes the defaults. Review and confirm the final include/exclude keyword pack before searching. Recommendations are optional: you can edit or replace all terms and use only your own keywords.
2. **Research a named target:** Add the supplied company as a manual candidate. It uses the same profile, keyword and start confirmations, without requiring a discovery batch. You can also add manual targets to the same pool as discovered candidates; manual additions do not count as search results or inherit approval.

The first discovery batch targets **10 companies** unless you supply a different positive integer. For each later batch, enter a positive integer for that batch. If fewer eligible prospects can be supported by inspected sources, the result reports the actual count and reason rather than filling the list with unsupported leads.

Candidates start unchecked. **Select one or more, then explicitly confirm starting research for exactly that set.** Where real multiselect is unavailable, use the displayed IDs, e.g. `选择 CAND-001、CAND-003，确认开始背调`. Selecting alone, adding a candidate, requesting more results or exporting a list does not start F1. Material configuration changes require new confirmations and fresh approval; existing runs keep their original approved snapshots.

Each approved client gets an independent run through the existing F1–F6 workflow. If F1 finds a material identity conflict, pause all formal work for that client, report the reason and conflicting evidence, and state what is needed to resume. Other approved runs can continue. The existing evidence, contact and deliverable checks, targeted refresh and four-sheet [output contract](skills/gtcbi/references/output-contract.md) remain in place. A candidate list is not a formal worksheet; exporting an existing report does not restart research. Optional outreach is draft-only.

See the [discovery and approval rules](skills/gtcbi/references/discovery-and-gate.md) for details. Searching, reading sources, collecting actual confirmation and exporting files depend on the host's authorized capabilities. This repository does not provide a live crawler, interactive UI, or export engine.

## Validate structured records

Requires Python 3.10+; no third-party dependencies.

```sh
python scripts/validate_discovery.py examples/synthetic-discovery.json
python scripts/validate_run.py examples/synthetic-gated-run.json --require-gate --as-of 2026-11-10
python -m unittest discover -s tests -v
```

The `--as-of` dates are fixed for the synthetic examples. The historical example still supports the original structure check:

```sh
python scripts/validate_run.py examples/synthetic-run.json --as-of 2026-11-09
```

Passing the historical check is not approval under the new workflow; the historical example fails `--require-gate`. The validators check declared structure and some contradictions, not actual operator authorization, source truth, legal compliance, authority, semantic entailment, or real sending. Industry scoring needs a separately approved implementation. Synthetic examples are not live research.

## Package contents

- `skills/gtcbi`: skill, operating rules and four-sheet output contract.
- `examples/synthetic-discovery.json` and `examples/synthetic-gated-run.json`: fictional pending discovery and approved-run records.
- `examples/synthetic-run.json`: fictional conditional case with an unfulfilled named-person deliverable.
- `scripts/validate_discovery.py` and `scripts/validate_run.py`: offline consistency checkers; neither starts research, sends messages nor writes to a CRM.
- `tests`: executable regression scenarios.
- `CHANGELOG.md`: version scope and limitations.

## 中文

全球外贸客户背景调查模型 **V2.0.1**。本项目按已确认规则新建，不冒充原 V2.0 源码的恢复版本。

- **新增：** 支持按行业发现客户和直接指定客户，也可把手动客户加到同一候选池。确认本次画像和关键词后再搜索；关键词可完全自定义。首批默认目标 10 家，后续每批由操作人填写正整数；结果不足时如实说明。候选默认未选中，选中并明确确认开工后才对指定客户启动背调。
- **优化：** 默认画像可临时换公司、行业或产品，不覆盖原默认值；实质变更建立新修订并重新确认。F1 主体冲突时暂停该客户全部正式背调，说明冲突证据、待确认事项及恢复条件；其他获准客户独立推进。
- **保留：** 原完整 F1–F6、模块职责映射、四表输出契约、证据时效与定向更新、联系人四维核验、多缺口分流、研究与交付分开验收、内容验收。模型不写死员工人数、行业权重、来源平台或查询次数；评分默认关闭，邮件模块可选且只生成草稿。
- **限制：** 搜索、读取来源、真实交互控件和文件交付依赖宿主能力；没有控件时用编号和明确文字确认。离线校验不能认证同意、证实来源或代替研究验收。未捆绑原 V2.0 Excel 模板或 PDF/CSV/Markdown/Excel 导出程序，未验证原导出兼容性。真实客户资料和私有画像不提交到此仓库。
