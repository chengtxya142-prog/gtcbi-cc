# Interactive intake forms — V2.0.9

When the host can render an interactive form whose submission comes back to the conversation (see the capability check below; in the Claude desktop app and claude.ai this is the inline widget tool), present the operator profile card, the candidate list and manual candidate entry as forms. Otherwise use the text cards and explicit text confirmations in [discovery and execution gate](discovery-and-gate.md). Forms change how input is collected, never what counts as confirmation.

[`assets/intake-form.html`](../assets/intake-form.html) is a working reference implementation; adapt its data and labels, keep its behaviour. It contains no HTML comments (widget tools reject them) and calls `sendPrompt(text)` on submit.

## Capability check

Decide this before showing the profile card, every time; do not assume text mode from memory.

1. Look for a tool that renders inline HTML widgets in the conversation and lets a widget send a message back. In the Claude desktop app (Chat and Code tabs) and claude.ai this is the visualize widget tool (e.g. `show_widget`, often listed with a setup or "read me" tool). It is frequently **deferred**: if a tool search facility exists, search for "widget" or "visualize" and load it before deciding. Call any required setup tool first, as that tool instructs.
2. If found, render the form with it, using [`assets/intake-form.html`](../assets/intake-form.html) as the widget body (fill `REV`, `PROFILE`, `SUGGEST`, `KEYWORDS_CONFIRMED` and `CANDIDATES`; keep `sendPrompt` as the submit call). Say in one line above it what the form is for and that its submit button sends the confirmation text.
3. If no such tool exists (e.g. Codex, Gemini or Antigravity without MCP Apps, command-line hosts), use text cards.

- Use a form only when the host really renders it and returns the submitted text. Never present Markdown boxes or a description of a form as if they were clickable, and never claim a click was received when no submission arrived.
- A host with only limited choice prompts (e.g. at most a few options per question) may use them for short choices, but candidate selection and free-text profile fields fall back to text.
- If a form fails to render or nothing comes back, say so and switch to text in the same turn.

## Profile form (`PROFILE-rN`)

- One form with six free-text fields: company, industry, products/services, target markets, customer types, cooperation objective. Every field accepts free text; offer common values only as optional suggestions (e.g. a datalist), never as a closed list.
- Prefill only retrievable defaults with a known source, or values the operator stated about their own business in the current conversation, and show each prefill's source. Words describing the target (e.g. "德国的包装分销商") are not the seller's own market or customer type unless the operator says so; leave unknown fields empty with a short example placeholder. All six are required.
- A separate **确认画像 / Confirm profile** button. Validate on click and show which fields are still empty; do not accept a partial card.
- Editing any field after confirming returns the card to "edited, needs re-confirmation" and disables candidate actions until confirmed again. A material edit creates the next revision (`PROFILE-r2`).
- Submission text states the revision and every field, e.g. `确认画像 PROFILE-r1：公司=…；行业=…；产品=…；市场=…；客户类型=…；合作目标=…`. Record that text as the confirmation basis.

## Candidate list form

- Show discovered candidates only after the profile and keyword pack are confirmed; before that, show the list disabled with the reason. Manual entry may be shown and used before confirmation (registering a target approves nothing), and a list made only of manual targets needs the profile but no keyword pack. In the reference form, set `KEYWORDS_CONFIRMED` to the real state; it defaults to `false`.
- One row per candidate with an **unchecked** checkbox, stable ID, company, country, website and preliminary match reason plus discovery source. Mark missing values "待核实 / unverified"; never fill them by guessing.
- Ticking boxes only updates a counter ("已选 N 家，尚未开始"); it starts nothing.
- A separate **开始背调 / Start research** button. Validate that the profile is confirmed and at least one box is ticked. Submission text: `选择 CAND-001、CAND-003，确认开始背调`. Record that text, the IDs and the revision as the confirmation basis; a later change of selection needs a new submission.

## Manual candidate entry

- Fields: company name, website, social media link, contact email, country, reason for checking. **Any one** of name, website, social link or email is enough; the rest may be empty. Show a hint saying so, and an inline error only when all four are empty.
- Also offer a bulk paste box, one company per line. Classify each line as email, social link (by platform domain), website (other URLs or bare domains) or company name.
- Deduplicate against every shown, selected and excluded candidate by normalized domain, case-insensitive name and normalized social link (without tracking parameters). Report skipped duplicates with the existing ID instead of adding them.
- Give each new entry the next unused sequential ID, a "手动添加 / manual" label and the source "操作人提供，未独立核实 / operator-supplied, not independently checked". Manual entries appear unchecked in the same list and are not discovery-batch results.
- Social links show the platform and type: profile, content ("需追溯发布者 / trace publisher") or short link ("需先展开 / expand first"); handle them as in [social sources](social-sources.md). An unrecognized link is not guessed as a platform; suggest entering it as a website.
- Adding a candidate never approves research.

## Recording

- The submitted message is the operator's real input. Quote it, do not paraphrase it into a broader approval, and do not invent timestamps.
- Ticks without a submission are invisible to you. If the operator only describes ticking boxes, say nothing has started and ask for the start submission or the equivalent text.
- Keyword packs stay as text confirmation in this version.
- If the submitted text is ambiguous (unknown ID, missing revision, contradictory fields), ask in text before acting.
- Forms run in the operator's view only; they write nothing to files, CRM or external services.

## 中文

宿主能渲染并回传提交内容时（Claude 桌面版和 claude.ai 有内嵌组件工具 `show_widget`，常为延迟加载，须先搜索“widget/visualize”并加载后再判断，每次显示画像卡前都要检查），画像卡、候选清单和手动添加客户用表单；否则沿用文字确认。表单只改变输入方式，不改变确认标准。画像表单六项都可自由输入（常用值只作提示），全部必填，单独点“确认画像”，确认后修改须重新确认；候选默认不勾，勾选只计数，须单独点“开始背调”，提交原文即确认依据；手动添加只需公司名、官网、社媒链接、邮箱任一项，支持每行一家批量粘贴并自动识别、查重、续编号，标“手动添加、操作人提供未核实”，社媒链接标平台和类型（主页 / 帖子需追溯发布者 / 短链需展开）。不得把文字方框当成可点击控件。
