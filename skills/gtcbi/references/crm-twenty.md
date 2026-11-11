# Optional CRM sync: Twenty — V2.0.2

Saving GTCBI results into a [Twenty](https://twenty.com) workspace is an optional, separate action. It is never part of discovery, selection or research approval, and it is one-way: GTCBI results go into Twenty. Twenty records do not select candidates, approve research or change GTCBI conclusions.

## When this applies

Use this file only when the operator asks to save, sync or push results to Twenty (or "the CRM" where Twenty is the connected CRM), or accepts an offer to do so. After a research run finishes or is paused you may offer the sync once in one line if Twenty tools are available; do not repeat the offer and do not write on silence.

## Check capability first

1. Confirm the host actually exposes Twenty tools (the workspace's MCP server at `https://{workspace}/mcp`, or another authorized Twenty connector). Tool names follow the workspace schema and a fixed grammar: `find_many_{objects}`, `find_one_{object}`, `create_one_{object}`, `create_many_{objects}`, `update_one_{object}`, `upsert_many_{objects}`, e.g. `find_many_companies`, `create_one_company`, `update_one_company`, `create_one_person`, `create_one_note`, `create_one_note_target`, `create_one_task`, `create_one_task_target`. Confirm the real names and fields in the connected workspace. The Twenty Cloud server checked on 2026-11-11 lists every tool directly; it has no `learn_tools` / `execute_tool` catalog mode. Use such a mode only if a connector actually offers it.
2. If no Twenty tool is available, say so, do not pretend to save, and offer the normal export instead. A server can be configured but still need sign-in (for example listed as `needs_auth`) and expose no tools: tell the operator to sign in through the host's MCP settings (in Claude Code, `/mcp`) in the session that will run the sync. Authorization done in another host or session does not carry over. Never ask for an API key, password or session credential in chat; connection is set up by the operator in the host or in Twenty (Settings → AI → MCP Server).
3. Check which of the optional custom fields below exist. Missing fields are not created by this workflow; put that content in the report Note and tell the operator which fields were missing.

## Confirmation gate for writes

Research approval does not authorize CRM writes. Before the first write of a sync:

- Show a short write plan: which customers, which record types will be created or updated (company, people, note, tasks, opportunity), and what will not be written.
- Obtain explicit confirmation for exactly that plan, e.g. “确认写入 Twenty”. Viewing the plan, exporting, asking for more candidates or silence is not confirmation.
- A changed plan (more customers, new record types, opportunities added) needs a fresh confirmation. Confirmation covers this sync only, not later ones.
- Deleting or merging existing CRM records is outside this workflow, even on request; report what the operator would need to do in Twenty.

## What may be written

| GTCBI result | Twenty record | Rules |
| --- | --- | --- |
| Researched company | Company | Find first by normalized website domain, then exact name plus country. Update the match; create only when none exists. If several match or legal entities differ, stop for that customer and ask. |
| Contacts and contact routes | Person linked to the company | Create a Person for a named individual whose current role at this entity is credible from the company's own official pages (team page, press release it issued) or another reliable dated source, even without a direct email or phone. A role without a name, a name from a single third-party mention, or an operator-supplied contact that failed verification stays in the report Note, not as a Person. If the operator explicitly asks for a Person that does not meet this bar, create it only with fields actually known and state the gap in the Note. Never fill email or phone from guessed patterns. Leave authority unstated; the Note says whether it is unknown. Find by email, then name plus company, before creating. |
| Decision and summary | Company custom fields (below), else the Note | Write the decision exactly as concluded: follow / conditional follow / defer / stop. Never invent a score. |
| Full report | Note attached to the company | Title `GTCBI 背调 {YYYY-MM-DD} {Run ID}`. Include decision, main opportunity and risk, F1–F6 summary, evidence list with sources and check dates, gaps with affected actions, missing deliverables, and evidence limits. Each sync of a new or refreshed run adds a new Note; do not overwrite earlier Notes. |
| Current and next actions | Task linked to the company | One Task per action, with its preconditions in the body. Do not mark Tasks done. |
| Email draft | Note | Title starts with `草稿 / Draft — 未发送`. Never record it as a sent email, activity or reply. |
| Follow or conditional follow decision | Opportunity | Only when the operator's confirmed plan includes it. Use the first pipeline stage; do not set amount, close date or probability unless the operator supplies them. |

Do not write: unapproved or merely selected candidates, excluded candidates, search snippets, hypotheses presented as facts, the seller's private default profile, or credentials. Stopped or incomplete runs may be saved only if the operator asks, with their real status shown in the Note. Identity-conflict pauses may be saved under the conditions below; saving does not resume research.

### Customers paused for identity conflict

A customer whose research was approved but is now paused for identity conflict may be saved when the operator explicitly confirms a write plan that includes the paused customer and its pause information. Do not require research to resume or finish before recording the pause.

- First resolve which Company record the pause belongs to using the existing matching rules. If the CRM target itself is ambiguous, ask the operator to identify it; do not guess, merge legal entities or overwrite disputed identity fields. Other customers can still proceed.
- Plan the Company and a pause Note, plus clarification Tasks if requested. Set `GTCBI status` to `identity conflict` if that field exists; otherwise put the status prominently in the Note. Label it `主体冲突暂停 / Identity conflict — paused`, not completed or verified.
- The attached Note must state the concrete pause reason, the conflicting claims and their sources/check dates where known, what remains unverified, the information or official verification needed, and the condition for resuming research. Retain the run/candidate IDs and original research dates. If the pause reason or supporting information has not been supplied or recorded, request the missing information before writing that customer's pause record; never invent it or save only an unexplained status.
- Recording the pause does not clear the conflict, resume formal research, create an Opportunity, or authorize outreach or a draft. Keep disputed contacts and claims clearly unverified in the Note rather than promoting them to verified contact or company fields.
- Read back the Company status and linked pause Note. Report it as saved with research still paused; report missing or unattached Notes as partial writes, not a fully saved pause record.

### Optional custom fields on Company

Create these once in Twenty (Settings → Data model → Companies → add field) for filtering and views. Names are suggestions; match whatever the workspace actually uses.

| Field | Type | Content |
| --- | --- | --- |
| GTCBI decision | Select: follow / conditional follow / defer / stop | Latest concluded decision |
| GTCBI research date | Date | Actual check date of the latest run |
| GTCBI run ID | Text | Latest run ID |
| GTCBI candidate ID | Text | e.g. `CAND-003`, if the company came from a discovery pool |
| GTCBI status | Select: completed / stopped / identity conflict | Execution status of the latest run |
| GTCBI key gap | Text | The gap that most affects the next action |

### Standard fields and tool inputs in a Twenty Cloud workspace (checked 2026-11-11 through MCP)

Workspaces can differ, so confirm against the connected one, but expect:

- **Company:** `name`; `domainName` is a links object whose `primaryLinkUrl` holds the bare domain (writing `aperam.com` through MCP worked); `address` is an object with `addressStreet1`, `addressStreet2`, `addressCity`, `addressPostcode`, `addressState`, `addressCountry` (**country is a sub-field of address**). Updating one address sub-field leaves the others intact. Also `linkedinLink`, `annualRevenue`, `accountOwnerId`. There is no company phone field.
- **Person:** `name {firstName, lastName}`, `emails {primaryEmail, additionalEmails}`, `phones`, `jobTitle`, `linkedinLink`, `companyId` (one company per person).
- **Note:** `title` and the body in `bodyV2: {markdown: "..."}` (not `body`). Creating a note does not attach it: write a separate `create_one_note_target` with `noteId` and `targetCompanyId`, `targetPersonId` or `targetOpportunityId`.
- **Task:** `title`, `bodyV2: {markdown}`, `status` (`TODO`, `IN_PROGRESS`, `DONE`; the UI shows `TODO` as "To do"), `dueAt`, `assigneeId`. Attach with `create_one_task_target`; one task may have several targets, e.g. the company and a person. Leave `dueAt` and `assigneeId` empty unless the operator supplies them.
- **Opportunity:** `name`, `companyId`, `pointOfContactId`, `stage` (first stage `NEW`), `amount`, `closeDate`.
- **Reading:** `find_many_*` needs `select` (`["*"]` or field names); filters are top-level arguments such as `domainName: {primaryLinkUrl: {ilike: "%example.com%"}}`, not wrapped in `filter`. It returns 10 records by default and at most 100; check `hasNextPage` before concluding a record is absent.
- **Writing:** `create_many_*` accepts at most 20 records per call. Write tools return only the record ID, so read records back before reporting them saved.

## Write safely

- Work one customer at a time and keep customers independent: a failure for one does not block or roll back the others.
- Preserve existing CRM data. Fill empty standard fields; do not overwrite a non-empty value that differs from research. Report the difference and let the operator decide. GTCBI custom fields may be updated to the latest run.
- Re-running the same sync must not create duplicates: reuse the company and persons, and skip a Note or Task whose run ID and title already exist. Check this through `find_many_note_targets` / `find_many_task_targets` filtered by the company's `targetCompanyId` (each result carries the note or task title), not by a workspace-wide title search.
- Each Note or Task is two writes: the record, then its target. If the target write fails, the record exists but is not attached; report it with its ID as unattached rather than as saved or failed.
- Use real research dates and statuses. Do not set sent, replied, meeting or deal states.
- Respect connector limits (about 100 requests per minute; `create_many_*` at most 20 records per call on the server checked); slow down or batch rather than drop records.
- The server also exposes tools this workflow never uses: `delete_*`, `merge_many_*`, `send_email`, `draft_email`, campaign tools, `create_field_metadata` and other metadata tools, and workflow tools.

## Report the outcome

After writing, read the records back, then list per customer what was created, updated, skipped and failed, with record links or IDs when the tool returns them, plus any field differences left for the operator. If a write failed or was only partial, say exactly which records exist. A record described in the conversation is not a saved record.

## 中文

把背调结果写入 Twenty CRM 是可选的独立动作，方向为单向：GTCBI → Twenty。必须先确认宿主确实连接了 Twenty 工具，再展示写入计划（哪些客户、写哪些记录），并取得明确确认（如“确认写入 Twenty”）后才写。先查重再新建；不覆盖 CRM 中已有且不同的内容；可写已获批并完成背调的客户，也可在操作人明确确认包含暂停信息的写入计划后，保存主体冲突暂停的客户。暂停记录必须注明具体缘由、冲突证据与来源（日期已知时记录）、未核实项、待补信息及恢复条件，并标为“主体冲突暂停”，不得标为已完成或已核实；信息缺失先补充，不捏造。若无法确定对应的 CRM 公司记录，先请操作人确认，不误关联。保存不代表恢复背调、创建商机或允许外联，写后须回读暂停备注与关联；邮件只作为“草稿，未发送”的备注；不标记已发送、已回复或成交状态。写完逐客户报告新建、更新、跳过和失败的记录。未连接时如实说明，改用普通导出，不索要密钥。
