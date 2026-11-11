# Changelog

## 未发布

- **新增（执行门）：** 开始前必须先确认操作人画像。以与候选相同的未勾选卡片形式展示 `PROFILE-r1`（公司、行业、产品、目标市场、客户类型、合作目标为必填，限制条件可选），取得明确确认（如“确认画像 PROFILE-r1”）后才能推荐关键词、发现客户或开始背调。指定客户和“只核验身份”等窄模式同样适用，不得提供跳过选项；无默认画像时如实说明并等待操作人填写。同一会话内未变更的已确认画像直接沿用。新增行为场景 B17、B18（未回放）。
- **起因：** 2026-11-11 两次真实指定客户背调在未确认操作人行业与背景的情况下开始，导致跟进结论缺少卖方依据。
- **新增（核验）：** 操作人提供的联系人视为待核实的说法。F1 须比对其邮箱域名与目标官方域名；不一致时查注册日期与注册商、邮件托管、网站内容及官方反欺诈声明，符合风险特征即按主体冲突暂停。不联系该地址测试，不直接认定欺诈，只建议经独立找到的官方渠道核实。
- **新增（执行门）：** 画像晚于已有调研确认时，只用已有证据在新画像下重评并标为重评；旧的跟进结论、匹配理由、缺口优先级和下一步动作须重新判断，不沿用；主体冲突不受画像影响；新检索须另行确认开始；重评作为新记录，不改写旧结果。
- **新增（交付）：** 当前动作是联系类（转介、角色确认、首封）且未要求草稿时，询问一次是否需要草稿并说明走哪条路径；不自动生成，操作人略过后不重复询问；存在主体冲突时不提供草稿。
- **更新（Twenty 同步）：** 按 MCP 实测更新 `crm-twenty.md`：工具名语法；该服务器无目录模式；已配置但未登录（`needs_auth`）的处理，授权不跨会话；备注和任务正文为 `bodyV2`，关联须单独写入 note/task target，一条任务可关联多个对象；裸域名可写入；状态枚举 `TODO`；商机首阶段 `NEW`；`find_many_*` 默认 10 条、最多 100 条；`create_many_*` 每次最多 20 条；写入只返回 ID，须回读；关联写入失败时如实报告未关联记录；列出本流程不使用的工具。
- **澄清（Twenty 联系人）：** 公司官方页面或其他可靠、有日期的来源能证明现任职位的具名人员可建为联系人，即使没有直接邮箱或电话；无名角色、单一第三方提及或核验失败的操作人提供联系人只留在备注。操作人明确要求时只填已知字段并在备注说明缺口；不按格式猜测邮箱电话。
- **验证：** 2026-11-11 由 Agent 通过 Twenty MCP 完成合成数据写入测试，以及两家真实公司（主体冲突暂停、有条件跟进）的公司、备注、任务、联系人和草稿备注写入，均回读核对。新增行为场景 B19–B21、C07（未回放）。
- **新增（可选）：** Twenty CRM 单向同步规则 `skills/gtcbi/references/crm-twenty.md`。背调完成后可把公司、已核实联系人、背调报告备注、后续任务及“草稿，未发送”的邮件备注写入 Twenty；写入前必须确认宿主已连接 Twenty 工具、展示写入计划并取得明确确认；先查重、不覆盖已有不同内容。新增行为场景 `evals/crm-twenty.json`（C01–C06）。
- **验证：** 2026-11-11 在真实 Twenty Cloud 工作区通过界面手动建立一组合成记录（公司、联系人、背调备注、任务），确认标准字段与映射一致，并据此补充字段说明（国家位于 Address 内、备注和任务通过 Relations 关联）。
- **限制：** C01–C07 未作为评估回放。不读取 CRM 来选择候选或批准背调，不删除或合并 CRM 记录，不创建自定义字段。

## 2.0.2

- **多 Agent 适配：** `scripts/`、`examples/` 移入 `skills/gtcbi/`，技能文件夹可独立安装，校验命令在任意安装位置可用；description 增加中文触发词；frontmatter 增加 `compatibility` 与 `metadata.version`；README 新增 Codex、Claude Code、Claude.ai、Hermes、Gemini CLI 安装说明。

- **新增：** 按行业发现客户、直接指定客户两种入口，支持在发现池中加入手动客户。首批默认目标 10 家，后续数量逐批填写。默认未选中，须明确选择并确认开工；新增客户不继承旧批准。加入合成示例、发现记录校验及研究记录的严格执行门检查。
- **优化：** 本次画像可临时跨公司、行业或产品修改，不覆盖默认画像；关键词可完全自定义。实质变更使用新修订并重新确认。F1 主体冲突暂停该客户全部正式背调，记录证据、待确认事项及恢复条件，不阻断其他获准客户。
- **保留：** 现有完整 F1–F6、证据与联系人核验、多缺口分流、独立交付状态、定向更新和四表输出契约。邮件仅生成可选草稿。旧示例仍可做历史结构检查，结果不等于新流程授权。
- **补充规则：** 手动客户取下一个连续编号，并请操作人补充国家或官网（缺失不阻断登记）；实质变更后旧候选的初步匹配理由不沿用，须按新配置复核或重新选择；候选名单导出中的暂定选择标为"已选择，未批准"。
- **行为评估：** B01–B16 共 16 个合成对话场景均已回放（13 个由不读取评估答案的独立代理盲测），全部符合 expected，未出现 forbidden 行为。
- **限制：** 版本已于合并后更新为 2.0.2。离线校验不认证操作人或证实来源；实际搜索、选择控件及文件交付依赖宿主能力。未新增独立界面、导出引擎或自动外联，也未验证真实集成。

## 2.0.1

- New standalone Git baseline; prior V2.0 code/history was unavailable.
- Preserve generic F1–F6 semantics; map source workflow rules by responsibility.
- Separate executed scope, obtained deliverables, draft readiness and actual communication.
- Verify contact identity/current role, relevance, route and authority independently.
- Distinguish routing gaps from transaction conditions; support multiple unresolved gaps.
- Keep scoring disabled without an approved industry profile.
- Add evidence freshness, targeted refresh, and deterministic contradiction checks.
- Include synthetic example, four-sheet output contract, and 25 executable regression tests.

Limitations: no live crawler, source truth verifier, CRM migration, bundled XLSX/PDF exporter or automatic outreach. Export integration and cross-industry live validation remain future integration work, not completed features.

中文：V2.0.1 是按确认规则建立的新仓库基线；历史 V2.0 实物模板与导出功能未恢复。新增规则和一致性验证不等同真实客户调查完成。
