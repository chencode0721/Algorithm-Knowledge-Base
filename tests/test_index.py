"""Offline tests for the README generator. Run: python -m unittest discover -s tests -v"""
from datetime import date
from pathlib import Path
import importlib.util
import tempfile
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / 'scripts' / 'generate_index.py'
spec = importlib.util.spec_from_file_location('generate_index', MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
import sys
sys.modules['generate_index'] = mod
spec.loader.exec_module(mod)


class TestReadmeGenerator(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'problems' / 'UVA' / '10038-Jolly-Jumpers').mkdir(parents=True)
        self.p = self.root / 'problems' / 'UVA' / '10038-Jolly-Jumpers'
        (self.p / 'solution.cpp').write_text('int main(){return 0;}\n', encoding='utf-8')
        (self.p / 'remind.md').write_text('''---
platform: UVA
id: 10038
title: Jolly Jumpers
status: AC
tags: Array, Math
solved: 2026-10-01
review_date: 2026-10-15
url: -
---
# 筆記
''', encoding='utf-8')
        (self.root / 'README.md').write_text('Manual intro\n\n' + mod.BEGIN + '\n' + mod.END + '\n\nManual outro\n', encoding='utf-8')

    def test_indexes_and_preserves_manual_text(self):
        entries = mod.collect(self.root)
        self.assertEqual(len(entries), 1)
        block = mod.render(entries, date(2026, 10, 14))
        self.assertIn('### Array（1 題）', block)
        self.assertIn('### Math（1 題）', block)
        self.assertIn('10038-Jolly-Jumpers/solution.cpp', block)
        self.assertIn('### 接下來 7 天', block)
        self.assertTrue(mod.update_readme(self.root, block, False))
        text = (self.root / 'README.md').read_text(encoding='utf-8')
        self.assertTrue(text.startswith('Manual intro'))
        self.assertTrue(text.endswith('Manual outro\n'))
        self.assertTrue(mod.update_readme(self.root, block, True))

    def test_due(self):
        entries = mod.collect(self.root)
        block = mod.render(entries, date(2026, 10, 16))
        self.assertIn('### 已到期\n\n- 2026-10-15', block)

    def test_reject_missing_source(self):
        (self.p / 'solution.cpp').unlink()
        with self.assertRaisesRegex(ValueError, 'solution.cpp'):
            mod.collect(self.root)

    def test_reject_duplicate_id(self):
        duplicate = self.root / 'problems' / 'UVA' / '010038-Copy'
        duplicate.mkdir()
        note = (self.p / 'remind.md').read_text(encoding='utf-8').replace('id: 10038', 'id: 010038')
        (duplicate / 'remind.md').write_text(note, encoding='utf-8')
        (duplicate / 'solution.cpp').write_text('', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, '重複題號'):
            mod.collect(self.root)

    def test_reject_ac_without_solved(self):
        note = (self.p / 'remind.md').read_text(encoding='utf-8').replace('solved: 2026-10-01', 'solved: -')
        (self.p / 'remind.md').write_text(note, encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'solved'):
            mod.collect(self.root)


if __name__ == '__main__':
    unittest.main()
