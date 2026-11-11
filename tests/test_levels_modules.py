"""Structural guard: every autonomy level lives under levels/ as its own module.

Encodes the requirement that each level's full content is under TEMPLATE and
each module has an independent, unique leaf name.
"""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MODULES = [
    ("L0-observe", "level/L0"),
    ("L1-local-draft", "level/L1"),
    ("L2-branch-pr", "level/L2"),
    ("L3-green-merge", "level/L3"),
    ("L4-bounded-repair", "level/L4"),
    ("L5-policy-proposal", "level/L5"),
]


class LevelsModulesTest(unittest.TestCase):
    def test_every_level_has_a_uniquely_named_module(self):
        for name, label in MODULES:
            readme = ROOT / "levels" / name / "README.md"
            self.assertTrue(
                readme.is_file(), f"missing module README: {readme}"
            )
            text = readme.read_text(encoding="utf-8")
            self.assertIn("## Do", text, f"{name}: no Do section")
            self.assertIn("## Don't", text, f"{name}: no Don't section")
            self.assertIn(label, text, f"{name}: does not mention {label}")

    def test_levels_index_links_every_module(self):
        index = (ROOT / "docs" / "LEVELS.md").read_text(encoding="utf-8")
        for name, _ in MODULES:
            self.assertIn(
                f"levels/{name}", index, f"docs/LEVELS.md does not link {name}"
            )

    def test_module_leaf_names_are_unique(self):
        names = [name for name, _ in MODULES]
        self.assertEqual(len(names), len(set(names)))


if __name__ == "__main__":
    unittest.main()
