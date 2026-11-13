"""Structural guard: the agent-facing contracts must ship with the template.

Each assertion below protects a document that only works if an agent actually
reads it. Deleting or hollowing one out should break CI, not silently degrade
the template for every project copied from it.
"""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


class MemoryLayerTest(unittest.TestCase):
    def test_memory_layer_ships_with_the_template(self):
        for rel in (
            "memory/README.md",
            "memory/symptom-routing.md",
            "memory/invariants.md",
        ):
            self.assertTrue((ROOT / rel).is_file(), f"missing {rel}")

    def test_symptom_routing_defines_its_line_format(self):
        text = read("memory/symptom-routing.md")
        self.assertIn("## Format", text)
        self.assertIn("## Rules", text)

    def test_invariants_requires_rule_reason_and_check(self):
        text = read("memory/invariants.md")
        self.assertIn("because", text)
        self.assertIn("check:", text)


class DecisionAuthorityTest(unittest.TestCase):
    def test_decisions_doc_covers_all_three_classes(self):
        text = read("docs/DECISIONS.md")
        for token in ("Class **A", "Class **B", "Class **C"):
            self.assertIn(token.split("**")[1], text, f"{token} missing")

    def test_decisions_doc_states_silence_is_not_approval(self):
        self.assertIn("Silence is not approval", read("docs/DECISIONS.md"))


class AgentEntryPointTest(unittest.TestCase):
    def test_agents_md_points_at_memory_and_decisions(self):
        text = read("AGENTS.md")
        self.assertIn("memory/README.md", text)
        self.assertIn("docs/DECISIONS.md", text)

    def test_agents_md_states_verifier_independence(self):
        self.assertIn("验证者不得是实现者", read("AGENTS.md"))

    def test_agents_md_sedimentation_has_two_outlets(self):
        text = read("AGENTS.md")
        self.assertIn("memory/symptom-routing.md", text)
        self.assertIn("memory/invariants.md", text)


class WorkflowDocTest(unittest.TestCase):
    def test_workflow_has_independent_verifier_role(self):
        text = read("docs/GIT_WORKFLOW.md")
        self.assertIn("| Verifier |", text)

    def test_workflow_has_gate_provenance_section(self):
        self.assertIn("门禁血统", read("docs/GIT_WORKFLOW.md"))


if __name__ == "__main__":
    unittest.main()
