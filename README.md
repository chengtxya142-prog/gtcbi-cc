# GTCBI · V2.0.5

**Global Trade Customer Background Investigation**  
**全球外贸客户背景调查模型**

An AI-assisted, cross-industry workflow for B2B prospect discovery and customer research. GTCBI helps sales and business development teams move from a market or product idea to a shortlist of prospects, then investigate only the customers explicitly approved by the operator.

The project is delivered as a reusable **Skill**, supported by operating rules, output specifications, synthetic examples and optional offline validators. It is not a standalone application or an autonomous lead-generation service.

## What GTCBI helps you do

- **Define the opportunity:** confirm the seller company, industry, products, target markets and cooperation goals for each run.
- **Discover relevant prospects:** use editable recommendations, custom keywords or a combination of both.
- **Keep the operator in control:** select candidates and explicitly approve research before the full F1–F6 workflow starts.
- **Build evidence-backed customer insights:** distinguish verified facts, assumptions, unknowns and conflicts; identify business contact paths and decision-changing gaps.
- **Turn research into next steps:** present cooperation opportunities, risks, outstanding questions and recommended actions. Outreach remains draft-only.

## Install

`skills/gtcbi` is a self-contained [Agent Skills](https://agentskills.io/specification) folder: `SKILL.md`, `references/`, the optional validators in `scripts/` and the synthetic `examples/`. Copy that whole folder (not just `SKILL.md`) to your agent's skill directory:

| Agent | Personal install | Per-project install |
| --- | --- | --- |
| Codex (CLI / app) | `~/.codex/skills/gtcbi` | `<repo>/.agents/skills/gtcbi` |
| Claude Code | `~/.claude/skills/gtcbi` | `<repo>/.claude/skills/gtcbi` |
| Claude.ai / Claude app | Zip the `gtcbi` folder and upload it under Settings → Capabilities → Skills | — |
| Hermes Agent | `~/.hermes/skills/gtcbi` | — |
| Gemini CLI | `~/.gemini/skills/gtcbi` | `<repo>/.gemini/skills/gtcbi` |

```sh
# macOS / Linux (example: Codex). Swap the target for another agent.
git clone https://github.com/chengtxya142-prog/gtcbi-cc.git
cp -R gtcbi-cc/skills/gtcbi ~/.codex/skills/
```

```powershell
# Windows PowerShell (example: Claude Code)
git clone https://github.com/chengtxya142-prog/gtcbi-cc.git
Copy-Item -Recurse gtcbi-cc\skills\gtcbi "$HOME\.claude\skills\"
```

Restart the agent or open a new session. Skill folder locations can change between agent releases; check your agent's skill documentation if GTCBI is not picked up.

## Get started

1. Ask in English or Chinese (e.g. "帮我找德国的包装分销商" or "背调这家公司"), or call the skill by name (`$gtcbi` in Codex, `/gtcbi` in Claude Code). Assistants without skill support can be given [`skills/gtcbi/SKILL.md`](skills/gtcbi/SKILL.md) and its referenced files as context.
2. Describe your company, products, target market and goal—or provide a company you already want to research.
3. Confirm the run-specific configuration and keyword pack. Review the candidate list, then explicitly select and approve the customers to investigate.

The host assistant must provide the authorized search, source-reading, interaction and file-generation capabilities required for the task. Hosts without code execution can follow the workflow but cannot run the optional validators (Python 3.10+, run from the skill folder: `python scripts/validate_discovery.py examples/synthetic-discovery.json`).

## Optional: save results to Twenty CRM

GTCBI can save finished research into a [Twenty](https://twenty.com) workspace (cloud or self-hosted). It is one-way (GTCBI → Twenty), optional, and never happens without your confirmation.

1. In Twenty, open **Settings → AI → MCP Server** and add the connection snippet to your agent (OAuth is recommended; do not paste API keys into chat).
2. Optionally add the GTCBI fields listed in the [sync rules](skills/gtcbi/references/crm-twenty.md) to Companies (decision, research date, run ID, candidate ID, status, key gap).
3. After a research run, say "把背调结果存到 Twenty". The agent shows a write plan; reply "确认写入 Twenty" to proceed.

Companies are matched before being created, existing CRM values are not overwritten, email drafts are saved as not-sent notes, and the agent reports what was created, updated, skipped or failed after reading the records back. On 2026-11-11 an agent wrote companies, notes, tasks, a contact and a draft note to a live Twenty Cloud workspace through its MCP server.

---

## 中文介绍

GTCBI 是面向外贸销售与商务拓展的**跨行业 B2B 客户发现与背景调查工作流**。

它将“明确开发方向、寻找目标客户、人工确认、深入背调、形成行动建议”整理为可复用的 Skill，帮助操作人有依据地判断：**客户是否匹配、合作机会在哪里、还缺哪些信息，以及下一步该做什么。**

### 核心功能

| 功能 | 说明 |
| --- | --- |
| 灵活配置开发方向 | 可沿用已有默认画像，也可临时切换公司、行业、产品或市场；本次修改不覆盖默认值。 |
| 开放式关键词 | 支持推荐词、自定义词及混合使用；关键词包确认后才开始搜索。 |
| 分批发现客户 | 首批默认目标为 10 家，后续每批由操作人填写数量；候选不足时如实说明，不凑数。 |
| 清晰展示候选 | 默认展示公司名、国家、官网、初步匹配理由及发现来源；支持去重和手动添加。 |
| 人工确认执行门 | 候选默认未选中，只有“选择客户＋明确确认开始”才启动正式背调；导出或继续查找不代表批准。 |
| 完整客户背调 | 沿用 F1–F6 流程，结合证据、联系人核验、合作条件和信息缺口，形成业务判断与行动建议。 |
| 客户任务相互独立 | 主体存在冲突时，仅暂停该客户，并注明缘由、冲突证据、待补信息和恢复条件。 |
| 可追溯的研究记录 | 保留运行快照、批准记录和历史证据，支持对受影响的信息进行定向更新。 |

### 安装

把整个 `skills/gtcbi` 文件夹复制到所用 Agent 的技能目录：Codex `~/.codex/skills/`，Claude Code `~/.claude/skills/`，Hermes `~/.hermes/skills/`，Gemini CLI `~/.gemini/skills/`；Claude.ai 把该文件夹打包为 zip 后在“设置 → 功能 → 技能”上传。重启或新开会话后，用中文提问即可触发。

### 两种使用方式

**按行业寻找客户**

> 帮我寻找法国市场的包装材料分销商。先与我确认产品范围和关键词，再展示首批候选客户。

**直接调查指定公司**

> 我已经有目标公司，请先确认本次配置，再由我确认开始背调，不需要重新搜索一批客户。

指定客户可以直接进入候选与确认流程，无需为了流程形式先找满 10 家。宿主不支持真实多选控件时，可通过稳定的客户编号和明确文字完成选择及批准。

### 输出与使用边界

研究结果重点呈现客户匹配情况、合作机会与风险、证据来源、关键缺口和下一步建议，并保留四表输出规范。实际文件生成取决于宿主工具；本仓库不内置导出引擎。

- **有依据再下结论：** 未知不等于负面，检索结束不等于目标信息已经取得。
- **研究与外联分开：** 邮件模块仅生成可选草稿，不自动发送、提交表单或写入 CRM。
- **校验不代替判断：** 离线检查器用于检查记录结构和部分一致性，不能证明真实授权、来源真实性或研究结论正确。
- **私有数据独立保存：** 仓库中的示例均为合成数据；真实客户资料、默认画像和凭证不应提交到公共仓库。

## Documentation / 项目文档

| 入口 | 内容 |
| --- | --- |
| [Skill](skills/gtcbi/SKILL.md) | 使用入口与任务路由 |
| [Discovery & approval](skills/gtcbi/references/discovery-and-gate.md) | 客户发现、选择和启动确认规则 |
| [Operating rules](skills/gtcbi/references/rules.md) | 完整背调执行规则 |
| [Output contract](skills/gtcbi/references/output-contract.md) | 交付内容与四表输出规范 |
| [Twenty CRM sync](skills/gtcbi/references/crm-twenty.md) | 可选：把背调结果单向写入 Twenty CRM 的规则 |
| [Official sources](skills/gtcbi/references/official-sources.md) | 可选：各国企业登记、欧盟 VIES、LEI、域名注册查询等官方核验来源清单 |
| [Structured records](skills/gtcbi/references/discovery-record.md) | 可选结构化记录与离线校验说明 |
| [Examples](skills/gtcbi/examples/) · [Tests](tests/) · [Evals](evals/discovery-gate.json) | 合成示例、回归测试与行为场景 |
| [Changelog](CHANGELOG.md) | 版本更新记录 |

## Acknowledgments / 致谢

Thanks to the [Twenty team and contributors](https://github.com/twentyhq/twenty/graphs/contributors) for building and maintaining [Twenty](https://github.com/twentyhq/twenty), the open-source CRM supported by GTCBI's optional integration.

感谢 [Twenty 项目团队及贡献者](https://github.com/twentyhq/twenty/graphs/contributors) 开发和维护开源 CRM 项目 [Twenty](https://github.com/twentyhq/twenty)，为 GTCBI 的可选 CRM 集成提供支持。
