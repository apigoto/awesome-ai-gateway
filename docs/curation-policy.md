# Curation and billing-data contracts

Reviewed 2026-10-22. These rules implement the evidence and inclusion requirements in [CONTRIBUTING.md](../CONTRIBUTING.md).

- A gateway must sit on the LLM or agent-tool request path. A standalone MCP tool, general app scanner or payment rail does not qualify merely because an agent can call it.
- Read the linked public documentation and repository before accepting a submission. Record the source and review date; an HTTP response alone is not a capability test.
- Operator submissions and canary reports remain self-reported. Only an unaffiliated reproduction can establish independently verified status. A passing canary is scoped to the tested model, endpoint, prompts and date; it does not verify privacy, billing or every catalog route.
- Integrate content against the current branch, mirror both language READMEs, preserve star markers, and credit contributors in commits and the closing reply. A conflict with the daily refresh is not grounds to reject a useful contribution.
- Label source-available licenses accurately; do not put noncommercial licenses under the open-source heading. Own-account subscription integrations retain the provider-ToS/account-ban caveat.

## Prepaid terms snapshot

`data/topup_terms.json` is the English source; `data/topup_terms.zh-CN.json` translates the same row identities. Each row must include a billing type (`prepaid`, `subscription`, `byok`), minimum purchase, fee, expiry/cycle, refund policy, HTTPS primary sources and an ISO review date no later than the snapshot's `as_of` date.

“Not stated on the reviewed page” is distinct from “never expires.” A right to expire credit is distinct from a guaranteed validity period. Monthly allowances, promotional grants and purchased balances must not be conflated. BYOK provider billing is not a gateway prepaid balance. Fees must distinguish credit-purchase fees from token markup.

`scripts/build_topup_table.py` renders the marked tables in both READMEs; `--check` rejects drift. `scripts/test_topup_terms.py` checks the data contract, translations, source/date preservation and stale-table detection. The existing freshness guard tracks the snapshot on its 30-day review cadence; never update dates without rereading sources.

Run `bash scripts/regen.sh` and `npx --yes awesome-lint` before committing.
