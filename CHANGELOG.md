# Changelog

## 2.0.2

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
