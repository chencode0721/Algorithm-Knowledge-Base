"""Tests for eight-tier difficulty index."""
from datetime import date
from pathlib import Path
import importlib.util
import tempfile
import unittest
import sys

MODULE = Path(__file__).resolve().parents[1] / "scripts" / "generate_index.py"
spec = importlib.util.spec_from_file_location("generate_index_difficulty", MODULE)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class DifficultyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "README.md").write_text("Head\n" + mod.BEGIN + "\n" + mod.END + "\n", encoding="utf-8")

    def add(self, platform, ident, difficulty, title):
        folder = self.root / "problems" / platform / (ident + "-test")
        folder.mkdir(parents=True)
        (folder / "solution.cpp").write_text("int main(){}\n", encoding="utf-8")
        (folder / "remind.md").write_text(f"""---
platform: {platform}
id: {ident}
title: {title}
difficulty: {difficulty}
tags: Sorting, Math
status: AC
solved: 2026-10-14
review_date: 2026-10-17
url: -
---
# Notes
""", encoding="utf-8")

    def test_eight_levels_and_legacy_unclassified(self):
        self.add("UVA", "11727", "2", "Cost Cutting")
        self.add("Jisuanke", "T1001", "1", "A plus B")
        self.add("LeetCode", "1", "Beginner", "Legacy")
        ps = mod.collect(self.root)
        result = mod.render(ps, date(2026,10,14))
        self.assertIn("🔴 Lv.1 啟蒙", result)
        self.assertIn("🟠 Lv.2 基礎", result)
        self.assertIn("⚪ 未分類", result)
        # Sorting, Math section appears in ascending level order regardless of platform
        segment = result.split("### Math（3 題）")[1].split("### ")[0]
        self.assertLess(segment.index("T1001"), segment.index("11727"))
        self.assertLess(segment.index("11727"), segment.index("Legacy"))
        self.assertTrue(mod.update_readme(self.root, result, False))

    def test_all_levels(self):
        for n in range(1,9):
            self.assertIn(f"Lv.{n}", mod.difficulty_label(str(n)))
        self.assertEqual(mod.difficulty_label("Hard"), "⚪ 未分類")


if __name__ == '__main__':
    unittest.main()
