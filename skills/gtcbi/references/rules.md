# Operating rules / 执行规则 — V2.0.4

## Configuration and scope

Use [discovery and execution gate](discovery-and-gate.md) for new research from discovery or named targets. Use the approved seller snapshot and record relevant MOQ/price/delivery/compliance/service capabilities, exclusions and language. Unknown seller capability is not a promise.

Each run records an ID, model/profile versions, target legal entity and country, research goal, mode, required modules/deliverables, start/check dates, source restrictions, budget and stopping criteria. Scope changes require a reason; never silently narrow a task to claim completion.

Modes: quick admission; standard development; targeted verification; full investigation; transaction check. Each is evaluated against its declared deliverables, not the amount of text produced. No mode waives the confirmed operator profile card; a narrower mode reduces the modules researched, not the seller context.

## Module ownership

| Generic module | Responsibility | Source Workflow 4.7.1 mapping |
| --- | --- | --- |
| F1 | Identity, legal/brand/group relations, company entry points | F1 |
| F2 | Business, products, channels, geography, suppliers | F2 and relevant F6.1/F6.5 |
| F3 | Procurement capability, demand and Why now | F3/F6.2 |
| F4 | Contacts, roles, routes and decision chain | F4/F6.3 |
| F5 | Risks, admission routing, gaps and action restrictions | F5 and relevant F6.4/TXN |
| F6 | Seller-buyer feasibility, proposal and next action | F6.5 and relevant SCORE/OPS |

Map by responsibility, not matching F numbers. A fact has one maintained owner; other modules reference its evidence ID.

## Sequence and routing

After the applicable execution gate: read existing records → establish scope → F1 → F2/F3/company routes → lightweight personnel discovery → F5 routing → justified deeper work/F6 → delivery and action assessment → transaction checks when triggered → save/read back within authorized scope.

Keep legal entity, brand, group and local subsidiary distinct. Group size or purchasing authority does not prove local scope. For a run created by the discovery or named-target gate, an F1 identity conflict pauses **all formal investigation of that client**, including otherwise independent evidence collection; preserve obtained evidence and continue other approved clients independently. Follow the [identity pause and recovery rule](discovery-and-gate.md#pause-stop-and-recover). For a historical run outside the gate, unresolved identity still blocks dependent personnel and external-action judgments.

Routes: park (evidenced mismatch/block); verify one decision-changing gap; verify multiple gaps; standard development; strategic research. Multiple gaps remain unresolved and are ordered by decision impact and cost of verification. A strategic R0 target can justify more research but is not ready for outreach. Strategic importance cannot waive identity or compliance blocks.

Each gap records question, affected judgment, affected action, evidence path, priority, owner, review date, closure condition and status. Leave unassigned fields explicit; never invent an owner or deadline. Unresolved transaction conditions do not automatically prevent an appropriate role-confirmation message.

Why now records the customer event, event/check dates, evidence state and commercial implication. A general trend, holiday post or trade-show appearance alone is not proof of buying intent. No clear trigger may be reported as none observed, with any sales hypothesis labeled separately.

## Contact verification

Store contact type separately from reachability: company entry, department, role lead or named person.

| R | Meaning |
| --- | --- |
| 0 | No reliable route or unresolved identity conflict |
| 1 | Correct company's public email, phone, form or referral entrance |
| 2 | Relevant department/role found; named person or direct access unresolved |
| 3 | Named person's current relevant role credible, with work/referral route |
| 4 | Multiple relevant people/functions and ranked primary, backup and referral paths |

Identity/current employment, functional relevance, contact route and decision authority are separate claims. An unnamed Head of Buying is a role lead, not a verified R3 person. A verified relevant person with unknown purchasing authority may be approached for role confirmation/referral; never call them the decision maker without evidence.

Record person name, employer/entity/country, current role, relevance, authority status, work route, verified profile URL if obtained, evidence, date, restrictions and ranking. A company page is not a personal profile. Do not invent URLs or private contact details. Profile verified, connection available, invite sent and reply received are separate states.

**Operator-supplied contacts.** When the operator supplies a contact (name, email, phone or signature), treat it as a claim to verify, not as evidence. As part of F1, compare the email domain with the target's official domain from its website or registry. If they differ, check, where accessible: the domain's registration date and registrar (public RDAP/WHOIS), its mail hosting (MX records), whether it serves a real website, and whether the company publishes an anti-fraud notice or an official list of email domains. A recent registration, consumer hosting, an empty site or an official statement excluding the domain is an `identity_conflict` that pauses the client; a group or regional domain the company itself documents is not. Record both domains, the facts found and their dates. Never contact the supplied address to test it, and never call it fraud: report the mismatch and the evidence. Recommend verification only through official channels the operator finds independently, not through details in the suspect message.

Lightweight discovery seeks relevant personnel plus company entrance; standard adds backups/referrals; full covers applicable decision, influence, execution and review functions. Configure roles/path coverage/budget by industry and organization. Count prior useful work toward deeper research. Stop when deliverables are adequately supported, or budget/access limits require a candid unresolved result; never manufacture searches to meet a quota.

## Feasibility and completion

For each applicable product/use case, MOQ, price, lead time, certification, customization, payment, logistics and service condition, compare buyer evidence with seller evidence. Mark match, conditional match, conflict or unknown. Sample capability does not imply low-MOQ production capability. State which proposed action is affected and what evidence would permit proceeding.

Report separately: scope execution; required person/profile/other deliverables; company-referral or named draft readiness; cooperation decision and conditions; actual handoff; optional scoring. General completion requires declared execution, required deliveries obtained or justified N/A, important conflicts handled, and actual save/readback when persistence was requested. Queries exhausted with missing deliverables means executed but target not obtained.

A negative finding can complete a research question. Park/stopped runs may finish their explicitly bounded stop assessment; do not label the originally promised outreach/full deliverables obtained.

When the current action involves contacting the target (a referral request, a role confirmation or a first message) and no email draft was requested, end the delivery by asking once whether the operator wants a draft, naming the route it would use (company entrance or verified person). Do not generate one unasked, and do not repeat the question in later turns if the operator passes over it. With an unresolved identity conflict, offer no draft. Drafts, plans and lists do not prove sending. Sales-stage changes require actual communication or transaction evidence. Keep one current priority action and label additional tasks as subsequent/conditional with dependencies.

## Evidence and refresh

Record evidence ID, entity/country, source URL/document ID, publisher/type, factual extract, publication date if known, actual check date, supported/opposed conclusion IDs, status, restrictions and refresh triggers. Separate assertion, inference, verified, unknown, conflict and inaccessible. Missing customs/review data is not zero purchasing or poor quality. For identity and domain checks, an optional list of registries, VIES, LEI and RDAP sources, with what each can and cannot show, is in [official sources](official-sources.md).

Industry/country profiles configure freshness by data type. No universal expiry is invented. Trigger earlier checks for role changes, identity anomalies, customer replies, procurement signals and changed transaction conditions. Expired evidence remains historical; do not silently delete or change ratings.

Record new feedback first, then refresh only affected facts, routing, feasibility, draft or next action. MOQ feedback ordinarily affects F3/F6; departure affects F4 and dependent drafts; entity conflict affects all dependent judgments. Preserve old/new values, source, scope and dates. Partial refresh does not reset the full-investigation date.

Source applicability, access status and evidence quality are different fields. Apply confirmed source exclusions. Use public or authorized access; official login flow for gated sources, never request passwords, verification codes or session credentials. Read access does not authorize sending, posting, form submission or CRM writes. CRM writes happen only through the separately confirmed [Twenty CRM sync](crm-twenty.md). Reuse evidence, but allow necessary pagination and fresh checks.

## Optional scoring

Default: no generic total, employee threshold or mandatory review platform. Express value, evidence sufficiency, reachability and transaction readiness independently. Enable scoring only under a confirmed versioned industry profile with weights, thresholds, N/A rules and approval state. Missing evidence is unscored, not automatically zero. Do not change weights for one prospect.

When approved rules allow intervals, calculate explicit lower/upper possible values for missing dimensions; these are not probabilistic confidence intervals. Keep provisional grade if boundaries cross. Human strategic priority is separate from evidence score. The bundled validator deliberately requests industry-specific review for any enabled numerical score.

## 中文要点

保留通用 F1–F6 含义，按职责吸收行业工作流。研究执行完毕不等于必需目标取得；岗位、人员、路径、权限分开核验。多缺口保持未决，明确影响联系、报价、寄样、签约或发货的哪一步。买方条件和卖方能力分别取证。行业评分默认关闭，人数门槛与查询预算不通用化。证据过期或客户新反馈只触发相关复核，不刷新全卡日期。邮件模块只产生获准范围的草稿，实际外联另有真实执行依据。
