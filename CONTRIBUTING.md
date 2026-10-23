# Contributing

Thanks for helping make this the best AI-gateway reference!

## Inclusion criteria

A project belongs on this list if **all** of these hold:

1. It is an actual **gateway, proxy, or router for LLM/agent traffic** — it sits on the
   request path. SDK wrappers, chat UIs, and prompt libraries are out of scope.
2. It is **publicly available** (public repo, or a commercial product with public docs).
3. It is **active within the last 12 months** — or it is historically significant and
   explicitly labeled ⚠️ stale.
4. It does **not** rely on reverse-engineered private APIs or resold stolen quota.

## How to add an entry

1. Pick the section that matches the **user pain point** the project serves best
   (an entry may appear in up to two sections).
2. Follow the entry format:

   ```markdown
   - [Name](https://github.com/owner/repo) <!--s:owner/repo-->⭐ ~1k<!--/s--> — One-sentence description ending with a period.
   ```

   - For non-GitHub/commercial products, omit the star marker.
   - The `<!--s:owner/repo-->…<!--/s-->` marker is refreshed daily by CI — put any
     rough number inside; it will be corrected on the next run.
3. If the project ships releases worth announcing, also add `owner/repo` to
   `data/projects.json` → `release_tracked_repos`.
4. Mirror your change in **both** `README.md` and `README.zh-CN.md` (a rough
   translation is fine — maintainers will polish it).
5. Descriptions must be factual and neutral: what it does, language/license if notable,
   one differentiator. No superlatives from the project's own marketing.

Maintainer acceptance and billing-data contracts: [curation policy](docs/curation-policy.md).

## PR checklist

- [ ] Entry follows the format above, in alphabetical-by-relevance position
- [ ] Added to both language READMEs
- [ ] `python -m unittest discover -s scripts -p 'test_*.py'` passes if you touched scripts
- [ ] One project per PR (easier to review)

## Badge for listed projects

If your project is listed here, you're welcome to show it — it links your users to an
independent, evidence-based comparison (and helps them verify you against the scorecard):

[![Listed in Awesome AI Gateway](https://img.shields.io/badge/listed%20in-Awesome%20AI%20Gateway-58a6ff?logo=awesomelists&logoColor=white)](https://github.com/cuihuan/awesome-ai-gateway)

```markdown
[![Listed in Awesome AI Gateway](https://img.shields.io/badge/listed%20in-Awesome%20AI%20Gateway-58a6ff?logo=awesomelists&logoColor=white)](https://github.com/cuihuan/awesome-ai-gateway)
```

Entirely optional, no strings attached. The badge doesn't change your scores or your
watch-list status — those follow the [published rubric](BENCHMARKS.md#scoring-rubric-apply-consistently)
and evidence only. (Watch-list entries: the badge is fine too; ⚠️ Unverified is a
verification status, not a verdict.)

## Report a sketchy relay (community watch list)

This list **excludes** ToS-violating "free-api" relays — but it also helps you spot
and document the ones that swap models, harvest data, overcharge, or vanish. That
watch list is built together, **on evidence, never hearsay.**

1. Generate proof. The fastest is a **canary diff**: run
   [`scripts/canary_check.py`](scripts/canary_check.py) against the relay and the
   official endpoint — it sends fixed discriminating prompts, diffs the outputs, and
   prints a verdict (`OK` / `inconclusive` / `suspicious — likely downgraded`).
   ```
   python scripts/canary_check.py \
     --relay-url https://some-relay.example/v1 --relay-key sk-... \
     --ref-url   https://api.openai.com/v1     --ref-key  sk-... --model gpt-5.5
   ```
   Other accepted evidence: a documented incident/thread, or a redacted billing screenshot.
2. Open a report with the **[⚠️ Report a sketchy relay](https://github.com/cuihuan/awesome-ai-gateway/issues/new?template=report-relay.yml)** template and attach the evidence. Redact your keys.
3. **The rule:** a relay is named only with verifiable, shareable proof — not a rumor,
   not a competitor grudge. Reports without evidence are closed. This is what keeps the
   watch list a credibility asset instead of a liability.

## Stale entries — the 12-month rule (and how it's enforced)

A listed project must be **active within the last 12 months**, or it stays only if it is
historically significant **and** explicitly labeled `⚠️ stale` / `⚠️ archived` (criterion 3).

This is enforced **mechanically** so nothing rots silently:
[`scripts/check_stale_gateways.py`](scripts/check_stale_gateways.py) runs **monthly in CI**
and flags any release-tracked repo that is archived or has had no push in 12 months **and is
not already labeled**. A green run means the promise holds; a red run is a to-do.

When an entry is flagged (or you spot one), the resolution is exactly one of:

1. **Label it** — add `⚠️ stale` / `⚠️ archived <Mon YYYY>` to the description if the project
   is historically significant and worth keeping for reference (e.g. TensorZero, Glide).
2. **Remove it** — if it is neither active nor notable enough to keep labeled.

Spotted a stale or wrong entry yourself? Open an issue with the project name and evidence
(last release date, archived repo, changed pricing). Mislabeled stale projects are bugs —
we'd rather know.
