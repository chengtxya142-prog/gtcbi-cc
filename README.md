# GTCBI V2.0.1

Global Trade Customer Background Investigation: a cross-industry research skill with evidence-based decisions, configurable research depth, and optional outreach drafts.

This is a new standalone implementation of the agreed V2.0.1 rules. It is not a recovered copy of the previous V2.0 repository. No customer records, private Notion pages, credentials, or prior Git history are included.

## Use

Open `skills/gtcbi/SKILL.md` with your agent, or copy the entire `skills/gtcbi` directory into the skill directory supported by your agent. For Claude/Gemini or another assistant, supply this entrypoint and the referenced files as project context. No platform-specific installer is claimed.

Provide seller industry, product, market, customer type, cooperation model, and target company. Reuse an already confirmed profile. Research requires your agent's available browsing/connector capabilities; this repository is not an autonomous crawler.

## Validate a structured run

Requires Python 3.10+; no third-party dependencies.

```sh
python scripts/validate_run.py examples/synthetic-run.json --as-of 2026-11-09
python -m unittest discover -s tests -v
```

The validator detects declared contradictions and missing references. It cannot establish source truth, legal compliance, authority, semantic entailment, or real sending. Industry scoring needs a separately approved implementation. Synthetic examples are not live research.

## Package contents

- `skills/gtcbi`: skill, operating rules and four-sheet output contract.
- `examples/synthetic-run.json`: fictional conditional case with an unfulfilled named-person deliverable.
- `scripts/validate_run.py`: offline consistency checker; never sends messages or writes CRM.
- `tests`: executable regression scenarios.
- `CHANGELOG.md`: version scope and limitations.

## 中文

全球外贸客户背景调查模型 **V2.0.1**。本项目按已确认规则新建，不冒充原 V2.0 源码的恢复版本。

核心优化：模块职责映射、研究与交付分开验收、联系人四维核验、多缺口分流、可选行业评分、证据时效及定向更新、内容验收。

模型不写死员工人数、行业权重、来源平台或固定查询次数。默认不评分；邮件模块可选，只生成草稿。四表结构保留为输出契约；本版未捆绑原 V2.0 Excel 文件或原 PDF/CSV/Markdown/Excel 导出程序，也不宣称已完成其兼容性验证。

校验器通过只证明结构及部分一致性规则通过，研究结论仍须人工或代理逐条核对证据。真实客户数据应存放在独立私有位置，不提交到此仓库。
