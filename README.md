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

## ����

ȫ����ó�ͻ���������ģ�� **V2.0.1**������Ŀ����ȷ�Ϲ����½�����ð��ԭ V2.0 Դ��Ļָ��汾��

�����Ż���ģ��ְ��ӳ�䡢�о��뽻���ֿ����ա���ϵ����ά���顢��ȱ�ڷ�������ѡ��ҵ���֡�֤��ʱЧ��������¡��������ա�

ģ�Ͳ�д��Ա����������ҵȨ�ء���Դƽ̨��̶���ѯ������Ĭ�ϲ����֣��ʼ�ģ���ѡ��ֻ���ɲݸ塣�ı��ṹ����Ϊ�����Լ������δ����ԭ V2.0 Excel �ļ���ԭ PDF/CSV/Markdown/Excel ��������Ҳ��������������������֤��

У����ͨ��ֻ֤���ṹ������һ���Թ���ͨ�����о����������˹�����������˶�֤�ݡ���ʵ�ͻ�����Ӧ����ڶ���˽��λ�ã����ύ���˲ֿ⡣
