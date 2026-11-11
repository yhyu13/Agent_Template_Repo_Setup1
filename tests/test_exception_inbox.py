"""Public CLI tests for the GitHub issue exception inbox MVP."""

from __future__ import annotations

import contextlib
import io
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "exception_inbox.py"
sys.path.insert(0, str(SCRIPT.parent))

import exception_inbox  # noqa: E402


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        text=True,
        capture_output=True,
        check=False,
    )


class DryRunReportTests(unittest.TestCase):
    def test_report_dry_run_outputs_stable_issue_payload(self):
        result = run_cli(
            "report",
            "--repo", "example/project",
            "--task-id", "task-123",
            "--agent-id", "cindy",
            "--session-id", "session-abc",
            "--level", "L2",
            "--kind", "evidence",
            "--summary", "Missing iPad evidence",
            "--details", "Same-version iPad verification is missing.",
            "--actionable", "human",
            "--dry-run",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(
            payload["title"],
            "[agent-exception][evidence][task-123] Missing iPad evidence",
        )
        self.assertEqual(
            payload["labels"],
            ["agent-exception", "kind/evidence", "level/L2", "needs-human"],
        )
        self.assertEqual(len(payload["key"]), 64)
        self.assertIn(f"<!-- agent-exception-key: {payload['key']} -->", payload["body"])
        self.assertIn("Missing iPad evidence", payload["body"])
        self.assertIn("session-abc", payload["body"])

    def test_report_dry_run_key_is_stable_for_same_exception(self):
        args = [
            "report",
            "--repo", "example/project",
            "--task-id", "task-123",
            "--agent-id", "cindy",
            "--session-id", "session-abc",
            "--level", "L2",
            "--kind", "evidence",
            "--summary", "Missing iPad evidence",
            "--dry-run",
        ]
        first = run_cli(*args)
        second = run_cli(*args)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(json.loads(first.stdout)["key"], json.loads(second.stdout)["key"])


class GitHubReportTests(unittest.TestCase):
    def args(self, *extra: str) -> list[str]:
        return [
            "exception_inbox.py",
            "report",
            "--repo", "example/project",
            "--task-id", "task-123",
            "--agent-id", "cindy",
            "--session-id", "session-abc",
            "--level", "L2",
            "--kind", "evidence",
            "--summary", "Missing iPad evidence",
            *extra,
        ]

    @mock.patch("exception_inbox.subprocess.run")
    def test_report_creates_issue_when_no_existing(self, run: mock.Mock):
        run.side_effect = [
            subprocess.CompletedProcess(args=[], returncode=0, stdout="[]", stderr=""),
            subprocess.CompletedProcess(args=[], returncode=0, stdout="https://github.com/example/project/issues/1\n", stderr=""),
        ]
        with mock.patch.object(sys, "argv", self.args()):
            result = exception_inbox.main()
        self.assertEqual(result, 0)
        self.assertEqual(run.call_count, 2)
        create_args = run.call_args_list[1].args[0]
        self.assertIn("create", create_args)
        self.assertIn("--title", create_args)

    @mock.patch("exception_inbox.subprocess.run")
    def test_report_comments_on_existing_exception_instead_of_duplicating(self, run: mock.Mock):
        payload = exception_inbox.build_issue_payload(
            argparse_namespace(
                repo="example/project",
                task_id="task-123",
                kind="evidence",
                scope="",
                actionable="human",
                level="L2",
                agent_id="cindy",
                session_id="session-abc",
                summary="Missing iPad evidence",
                details="",
                branch="",
                head_sha="",
            )
        )
        existing = [{"number": 7, "title": "existing", "body": f"<!-- agent-exception-key: {payload['key']} -->", "labels": [], "url": "https://github.com/example/project/issues/7"}]
        run.side_effect = [
            subprocess.CompletedProcess(args=[], returncode=0, stdout=json.dumps(existing), stderr=""),
            subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr=""),
        ]
        with mock.patch.object(sys, "argv", self.args()):
            result = exception_inbox.main()
        self.assertEqual(result, 0)
        self.assertEqual(run.call_count, 2)
        comment_args = run.call_args_list[1].args[0]
        self.assertIn("comment", comment_args)
        self.assertNotIn("create", comment_args)


def argparse_namespace(**kwargs):
    import argparse
    return argparse.Namespace(**kwargs)


class WatchTests(unittest.TestCase):
    @mock.patch("exception_inbox.subprocess.run")
    def test_watch_once_filters_agent_actionable_issues(self, run: mock.Mock):
        issues = [
            {"number": 1, "title": "agent can retry", "body": "", "labels": [{"name": "agent-exception"}, {"name": "agent-actionable"}], "url": "https://github.com/example/project/issues/1"},
            {"number": 2, "title": "needs human", "body": "", "labels": [{"name": "agent-exception"}, {"name": "needs-human"}], "url": "https://github.com/example/project/issues/2"},
        ]
        run.return_value = subprocess.CompletedProcess(args=[], returncode=0, stdout=json.dumps(issues), stderr="")
        output = io.StringIO()
        with mock.patch.object(sys, "argv", ["exception_inbox.py", "watch", "--repo", "example/project", "--once", "--actionable", "agent"]):
            with contextlib.redirect_stdout(output):
                result = exception_inbox.main()
        self.assertEqual(result, 0)
        lines = [json.loads(line) for line in output.getvalue().splitlines() if line.strip()]
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0]["number"], 1)


if __name__ == "__main__":
    unittest.main()
