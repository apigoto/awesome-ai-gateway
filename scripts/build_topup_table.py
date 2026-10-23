#!/usr/bin/env python3
"""Render the sourced billing-terms snapshot into both READMEs.

Spec: docs/curation-policy.md. Unknown terms stay unknown; BYOK and monthly
subscriptions must not be presented as non-expiring prepaid credit.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START = '<!-- TOPUP_TERMS:START -->'
END = '<!-- TOPUP_TERMS:END -->'
FIELDS = ('minimum_topup', 'topup_fee', 'credit_expiry', 'refunds')


def cell(value):
    return str(value).replace('|', '&#124;').replace('\n', ' ')


def render(data, translation=None):
    headers = (translation['headers'] if translation else
               ['Gateway / billing', 'Minimum top-up / entry price', 'Fee',
                'Credit expiry / cycle', 'Refunds', 'Sources / checked'])
    lines = ['| ' + ' | '.join(headers) + ' |',
             '| ' + ' | '.join(['---'] * len(headers)) + ' |']
    for row in data['entries']:
        label = translation['entries'][row['gateway']] if translation else row
        values = [row['gateway'] + ' / ' + label['billing_model']]
        values += [label[field] for field in FIELDS]
        sources = ', '.join(f'[{i}]({url})' for i, url in enumerate(row['sources'], 1))
        values.append(sources + ' · ' + row['checked_on'])
        lines.append('| ' + ' | '.join(cell(v) for v in values) + ' |')
    return '\n'.join(lines)


def replace_table(text, table):
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError('Expected exactly one pair of top-up table markers')
    before, rest = text.split(START)
    _, after = rest.split(END)
    return before + START + '\n' + table + '\n' + END + after


def outputs(root=ROOT):
    data = json.loads((root / 'data/topup_terms.json').read_text())
    zh = json.loads((root / 'data/topup_terms.zh-CN.json').read_text())
    return {'README.md': render(data), 'README.zh-CN.md': render(data, zh)}


def table_cells(body):
    """Compare content while allowing the existing Markdown alignment formatter."""
    rows = []
    for line in body.strip().splitlines():
        values = [value.strip() for value in line.split('|')[1:-1]]
        if values and all(set(value) <= set('-: ') for value in values):
            continue
        rows.append(values)
    return rows


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args(argv)
    stale = []
    for name, table in outputs().items():
        path = ROOT / name
        text = path.read_text()
        expected = replace_table(text, table)
        # README table alignment is a separate gate; compare cell content.
        existing = text.split(START)[1].split(END)[0]
        if args.check:
            if table_cells(existing) != table_cells(table):
                stale.append(name)
        else:
            path.write_text(expected)
    if stale:
        print('Stale top-up terms: ' + ', '.join(stale))
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
