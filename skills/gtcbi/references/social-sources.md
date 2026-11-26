# Social media leads and logged-in reading — V2.0.9

Social media links (LinkedIn, Instagram, Facebook, TikTok, YouTube, X, Xiaohongshu, Douyin, Weibo and similar) can be leads, discovery sources or evidence. They never replace the official website and domain check in F1.

## Social links as leads

- Accept a profile link, a post/reel/video link or a short link as a manual candidate's only lead, the same as a company name, website or email. Record the platform and the link type: **profile** (company page, account, channel) or **content** (post, reel, video, story, event).
- A profile is close to the company but is not its website. From it, find the official website and domain, then verify identity as usual.
- A content link only shows where the operator saw something. First identify who published it (the company itself, a distributor, agency, media outlet, employee or unrelated person), then go from that account to the official website. Do not treat claims in a post as company facts; record them as source assertions with the link and date.
- Before approval, classify links from the URL alone and do not open them; label a short link (e.g. `vt.tiktok.com`, `lnkd.in`, `t.co`, `youtu.be`) as "需先展开 / expand first". Expanding links and tracing publishers belong to F1 after the start confirmation. A redirect to an unrelated site is a risk signal, not a lead.
- Deduplicate by normalized link (without tracking parameters) as well as by name and domain.

## Reading order

1. Public content without login.
2. Public oEmbed or preview data where the platform provides it.
3. Pages visible in the operator's own logged-in browser, only under the limits below.
4. If none works, mark the content "无法读取 / not readable", state why, and continue with other sources.

## Reading through the operator's own logged-in account

This is the operator's own access, not a bypass, but platforms such as LinkedIn restrict automated reading and may limit or ban the account. Apply these limits:

- **Ask first.** Before the first logged-in read in a session, tell the operator which platform, which accounts or pages, roughly how many pages, and that automated reading carries a risk of rate limits or account restrictions. Read only after an explicit yes. A yes covers this session and the stated scope, not later sessions or new targets.
- **Operator signs in.** The operator logs in in the host browser themselves. Never ask for, type or store passwords, verification codes, cookies or session tokens, and never import browser cookies on your own initiative.
- **Read only.** Do not like, follow, connect, comment, message, post, join, save, react, accept requests or change any setting. Do not click ads or "contact" buttons.
- **Keep volume low.** Per customer and platform, read only the pages needed (normally the company page, its about/people section and the specific posts supplied, at most about 10 page views). Across all customers, stay within about 30 page views per platform per session. Scroll at most a few screens per page; do not page through search results or follower lists in bulk.
- **Go slowly.** Leave several seconds (about 10 or more) between page loads, and do not open many tabs on the same platform at once.
- **Mind people's profiles.** On LinkedIn, viewing a person's profile while logged in can notify them. Prefer the company page; open individual profiles only when a contact needs verifying and the operator has agreed, either to those named people in advance or person by person.
- **Stop on warnings.** On any CAPTCHA, security check, "unusual activity" notice, rate-limit message or forced logout, stop reading that platform immediately, tell the operator what appeared, and do not retry, switch accounts or try another route around it. Resume only if the operator has cleared the check themselves and explicitly asks to continue; then go more slowly, and on a second warning stop that platform for the rest of the session. Do not use proxies, multiple accounts or anti-detection tricks.
- **Keep only what is needed.** Record the specific facts used as evidence with link, date and "seen via operator's logged-in account". Do not bulk copy or export profiles, follower lists or comments, and keep private personal data out of the repository.

## Not used

Login-wall bypasses, scraping through rotated or fake accounts, proxies for evasion, CAPTCHA solving and leaked or purchased session data are never used. Third-party scraping APIs (such as ScrapeCreators or Apify) are not part of this version; if adopted later, they need the operator's own key stored outside the chat and their results stay unverified leads.

## 中文

社媒链接（主页、帖子、Reels、短视频、短链）可以作为手动客户的唯一线索。主页离公司近但不等于官网；帖子只说明在哪里看到，须先追溯发布者，再从账号找官网和官方域名，帖子里的说法只作来源陈述。短链先展开再分类。读取顺序：公开内容 → 平台公开预览 → 操作人自己已登录的浏览器 → 都不行就标“无法读取”。使用操作人账号读取时：每次会话先说明平台、范围、页数和封号风险并取得同意；由操作人自己登录，不经手密码、验证码或 cookie；只读不操作（不点赞、关注、加好友、评论、私信）；每家客户每个平台约 10 个页面以内、每个平台每次会话约 30 个页面以内、页面间隔约 10 秒以上；领英尽量看公司页，查看个人主页会通知对方，须经同意；遇到验证码、安全验证、异常提示或被登出立即停止并告知，不重试、不换号、不绕过。不使用代理、多账号或反检测手段。
