# Official verification sources / 官方核验来源 — V2.0.4 (optional)

An optional starting list for F1 identity checks and for operator-supplied contacts. It is not required, not exhaustive and not a source quota: use what the host can actually reach, apply configured source exclusions first, and prefer the target's own country registry over aggregators. Addresses and access rules change; if a source is unreachable, record it as inaccessible and use another applicable one.

## What each source can and cannot show

| Need | Source type | Shows | Does not show |
| --- | --- | --- | --- |
| Legal existence and status | National company registry | Legal name, registration number, status (active/struck off), registered address, legal form, often officers and filings | Trading activity, buying intent, contact people, whether a brand name belongs to this entity |
| EU VAT number | EU VIES | Whether a VAT number is valid on the check date | For some member states (e.g. Spain, Germany) the name and address are withheld; a valid result then does not confirm which company holds the number |
| Group and cross-border entity | GLEIF LEI search | Legal name, address, LEI status and, where reported, parent relationships | Entities without an LEI; small companies often have none |
| Email or website domain | RDAP / WHOIS, DNS (MX, SPF) | Registration date, registrar, name servers, mail hosting | Who controls the domain when redacted; that a domain is fraudulent |
| Company's own claims | Official website legal notice / imprint (Aviso legal, Mentions légales, Impressum), anti-fraud notice, staff or contact pages | Self-declared legal name, tax ID, address, official email domains, named staff | Independent confirmation; treat as the company's assertion |

A registry or VIES match supports identity only. It is not evidence of creditworthiness, compliance or demand. Record the actual check date, the identifier queried and the exact result, including "valid, name not disclosed".

## Starting points by country (check availability on use)

| Country / scope | Source | Notes |
| --- | --- | --- |
| EU | VIES — `ec.europa.eu/taxation_customs/vies` | Free; validity only for some states (see above) |
| Global | GLEIF — `search.gleif.org` | Free LEI lookup |
| France | Annuaire des Entreprises — `annuaire-entreprises.data.gouv.fr`; API `recherche-entreprises.api.gouv.fr` | Free; SIREN/SIRET, status, address, activity code, officers |
| United Kingdom | Companies House — `find-and-update.company-information.service.gov.uk` | Free; officers and filings |
| Spain | BORME — `boe.es/borme`; Registradores de España — `registradores.org` | BORME is the free official gazette of registry acts; full registry extracts (nota simple) are paid |
| Germany | Handelsregister — `handelsregister.de` | Basic search free; some documents paid |
| Netherlands | KVK — `kvk.nl` | Basic search free; extracts paid |
| Belgium | KBO / BCE Public Search — `kbopub.economie.fgov.be` | Free |
| Italy | Registro Imprese — `registroimprese.it` | Search free; documents paid |
| Domains | RDAP via `rdap.org` or the registry's RDAP server; ICANN lookup — `lookup.icann.org` | Free; personal registrant data is often redacted |

Third-party aggregators (company databases, directories, prospecting tools) can point to a registry record but are not official sources; cite the registry once found.

## Rules of use

- Use public or authorized access only. Do not bypass logins, CAPTCHAs or paywalls, and do not ask for credentials. Paid extracts are bought only on the operator's explicit request; otherwise list the extract as a gap with the action it affects (usually signing or payment).
- A name match alone is not identity: compare legal form, address, registration number and domain. Keep legal entity, brand and group distinct.
- Disagreement between the registry and the company's own claims (name, legal form, address, tax ID) is recorded as a conflict with both values, sources and dates; a material one follows the identity pause rule.
- These checks belong to F1 and are reused by F4 and F5; they do not replace the operator profile confirmation or the start confirmation.
