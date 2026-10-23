"""Billing-data contracts: unknown is not never; translations cannot drop rows."""
import datetime
from contextlib import redirect_stdout
from io import StringIO
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import build_topup_table as build
from check_freshness import TRACKED, stale_entries

ROOT = Path(__file__).resolve().parent.parent


class TopupTerms(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'data/topup_terms.json').read_text())
        self.zh = json.loads((ROOT / 'data/topup_terms.zh-CN.json').read_text())

    def test_rows_have_reviewed_sources_and_separate_billing_types(self):
        names = set()
        for row in self.data['entries']:
            self.assertNotIn(row['gateway'], names)
            names.add(row['gateway'])
            self.assertIn(row['billing_model'], ('prepaid', 'subscription', 'byok'))
            self.assertTrue(row['sources'])
            self.assertTrue(all(u.startswith('https://') for u in row['sources']))
            self.assertLessEqual(datetime.date.fromisoformat(row['checked_on']),
                                 datetime.date.fromisoformat(self.data['as_of']))
            for field in build.FIELDS:
                self.assertTrue(row[field].strip())
        self.assertEqual(names, set(self.zh['entries']))
        self.assertEqual({r['billing_model'] for r in self.data['entries']},
                         {'prepaid', 'subscription', 'byok'})

    def test_unknown_and_contractual_expiry_are_not_invented(self):
        rows = {r['gateway']: r for r in self.data['entries']}
        self.assertIn('not stated', rows['Vercel AI Gateway']['credit_expiry'].lower())
        self.assertIn('May expire', rows['OpenRouter']['credit_expiry'])
        self.assertIn('N/A', rows['INFRO']['credit_expiry'])
        self.assertIn('rollover not stated', rows['Standard Compute']['credit_expiry'])

    def test_render_preserves_sources_and_review_date_in_both_languages(self):
        for translation in (None, self.zh):
            rendered = build.render(self.data, translation)
            for row in self.data['entries']:
                self.assertIn(row['gateway'], rendered)
                self.assertIn(row['checked_on'], rendered)
                for source in row['sources']:
                    self.assertIn(source, rendered)

    def test_cell_escapes_pipes_and_newlines(self):
        self.assertEqual(build.cell('A|B\nC'), 'A&#124;B C')

    def test_replace_fails_on_missing_or_duplicate_markers(self):
        for text in ('missing', build.START + build.END + build.START):
            with self.assertRaises(ValueError):
                build.replace_table(text, 'table')
        self.assertEqual(build.replace_table('before' + build.START + 'old' + build.END + 'after', 'new'),
                         'before' + build.START + '\nnew\n' + build.END + 'after')

    def test_freshness_watch_includes_topup_terms(self):
        self.assertIn('data/topup_terms.json', [p for _, p in TRACKED])
        self.assertTrue(stale_entries([('terms', self.data['as_of'])],
                                     datetime.date.fromisoformat(self.data['as_of']) + datetime.timedelta(days=31), 30))

    def test_published_tables_match_snapshot(self):
        self.assertEqual(build.main(['--check']), 0)

    def test_check_rejects_a_stale_table_and_does_not_write(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ('README.md', 'README.zh-CN.md'):
                (root / name).write_text(build.START + '\nstale\n' + build.END)
            with patch.object(build, 'ROOT', root), patch.object(build, 'outputs', return_value=build.outputs()), redirect_stdout(StringIO()):
                self.assertEqual(build.main(['--check']), 1)
                self.assertIn('stale', (root / 'README.md').read_text())
                self.assertEqual(build.main([]), 0)
                self.assertEqual(build.main(['--check']), 0)
