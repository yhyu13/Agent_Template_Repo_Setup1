#!/usr/bin/env python3
"""GitHub issue exception inbox MVP.

Exceptions are recorded in GitHub issues so both humans and agents can read them.
This script does not use email, mobile push, or local-only inboxes as the source of truth.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

LEVELS = {"L0", "L1", "L2", "L3", "L4", "L5"}
KINDS = {"evidence", "conflict", "approval", "tooling", "scope", "other"}
ACTIONABLE = {"agent", "human"}


def exception_key(repo: str, task_id: str, kind: str, scope: str) -> str:
    material = "|".join([repo, task_id, kind, scope])
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def build_issue_payload(args: argparse.Namespace) -> dict[str, Any]:
    key = exception_key(args.repo, args.task_id, args.kind, args.scope or "")
    actionable_label = "agent-actionable" if args.actionable == "agent" else "needs-human"
    title = f"[agent-exception][{args.kind}][{args.task_id}] {args.summary}"
    labels = [
        "agent-exception",
        f"kind/{args.kind}",
        f"level/{args.level}",
        actionable_label,
    ]
    timestamp = datetime.now(timezone.utc).isoformat()
    body = "\n".join(
        [
            f"<!-- agent-exception-key: {key} -->",
            "",
            "## Agent Exception",
            "",
            f"- Task: `{args.task_id}`",
            f"- Agent: `{args.agent_id}`",
            f"- Session: `{args.session_id}`",
            f"- Level: `{args.level}`",
            f"- Kind: `{args.kind}`",
            f"- Actionable by: `{args.actionable}`",
            f"- Repo: `{args.repo}`",
            f"- Branch: `{args.branch or ''}`",
            f"- Head SHA: `{args.head_sha or ''}`",
            f"- Scope: `{args.scope or ''}`",
            f"- Reported at: `{timestamp}`",
            "",
            "### Summary",
            "",
            args.summary,
            "",
            "### Details",
            "",
            args.details or "",
            "",
            "### Requested next step",
            "",
            "If this is agent-actionable, the agent should inspect this issue, add a comment with the plan/result, and keep the issue open until resolved.",
            "If this needs human input, a human should reply in this issue; agents must not treat silence as approval.",
            "",
        ]
    )
    return {"key": key, "title": title, "body": body, "labels": labels}


def add_report_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--repo", required=True)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--agent-id", required=True)
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--level", required=True, choices=sorted(LEVELS))
    parser.add_argument("--kind", required=True, choices=sorted(KINDS))
    parser.add_argument("--summary", required=True)
    parser.add_argument("--details", default="")
    parser.add_argument("--branch", default="")
    parser.add_argument("--head-sha", default="")
    parser.add_argument("--scope", default="")
    parser.add_argument("--actionable", choices=sorted(ACTIONABLE), default="human")
    parser.add_argument("--dry-run", action="store_true")


def run_gh(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["gh", *args], text=True, capture_output=True, check=False)


def list_exception_issues(repo: str, limit: int = 200) -> list[dict[str, Any]]:
    result = run_gh(
        [
            "issue", "list",
            "--repo", repo,
            "--label", "agent-exception",
            "--state", "open",
            "--limit", str(limit),
            "--json", "number,title,body,labels,url",
        ]
    )
    if result.returncode != 0:
        raise RuntimeError(f"gh issue list failed: {result.stderr.strip()}")
    return json.loads(result.stdout or "[]")


def find_existing_issue(issues: list[dict[str, Any]], key: str) -> dict[str, Any] | None:
    marker = f"<!-- agent-exception-key: {key} -->"
    for issue in issues:
        if marker in (issue.get("body") or ""):
            return issue
    return None


def write_temp_body(body: str) -> Path:
    handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False)
    with handle:
        handle.write(body)
    return Path(handle.name)


def report_to_github(args: argparse.Namespace, payload: dict[str, Any]) -> dict[str, Any]:
    issues = list_exception_issues(args.repo)
    existing = find_existing_issue(issues, payload["key"])
    body_path = write_temp_body(payload["body"])
    try:
        if existing is not None:
            number = str(existing["number"])
            result = run_gh(
                [
                    "issue", "comment", number,
                    "--repo", args.repo,
                    "--body-file", str(body_path),
                ]
            )
            if result.returncode != 0:
                raise RuntimeError(f"gh issue comment failed: {result.stderr.strip()}")
            return {
                "action": "commented",
                "number": existing["number"],
                "url": existing.get("url", ""),
                "key": payload["key"],
            }
        command = [
            "issue", "create",
            "--repo", args.repo,
            "--title", payload["title"],
            "--body-file", str(body_path),
        ]
        for label in payload["labels"]:
            command.extend(["--label", label])
        result = run_gh(command)
        if result.returncode != 0:
            raise RuntimeError(f"gh issue create failed: {result.stderr.strip()}")
        return {
            "action": "created",
            "url": result.stdout.strip(),
            "key": payload["key"],
        }
    finally:
        try:
            body_path.unlink()
        except OSError:
            pass


def filter_issues(issues: list[dict[str, Any]], actionable: str | None) -> list[dict[str, Any]]:
    if actionable is None:
        return issues
    wanted = "agent-actionable" if actionable == "agent" else "needs-human"
    filtered = []
    for issue in issues:
        names = {label.get("name") for label in issue.get("labels", []) if isinstance(label, dict)}
        if wanted in names:
            filtered.append(issue)
    return filtered


def print_issues(issues: list[dict[str, Any]]) -> None:
    for issue in issues:
        print(json.dumps(issue, ensure_ascii=False), flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    report = sub.add_parser("report", help="Create or update an exception issue")
    add_report_args(report)

    list_parser = sub.add_parser("list", help="List open exception issues")
    list_parser.add_argument("--repo", required=True)
    list_parser.add_argument("--actionable", choices=sorted(ACTIONABLE))
    list_parser.add_argument("--limit", type=int, default=200)

    watch = sub.add_parser("watch", help="Poll GitHub issues for exceptions")
    watch.add_argument("--repo", required=True)
    watch.add_argument("--actionable", choices=sorted(ACTIONABLE))
    watch.add_argument("--interval", type=float, default=60.0)
    watch.add_argument("--limit", type=int, default=200)
    watch.add_argument("--once", action="store_true")

    args = parser.parse_args()

    try:
        if args.command == "report":
            payload = build_issue_payload(args)
            if args.dry_run:
                print(json.dumps(payload, ensure_ascii=False, indent=2))
                return 0
            result = report_to_github(args, payload)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
        if args.command == "list":
            issues = list_exception_issues(args.repo, args.limit)
            print_issues(filter_issues(issues, args.actionable))
            return 0
        if args.command == "watch":
            if args.interval <= 0:
                raise RuntimeError("--interval must be positive")
            while True:
                issues = list_exception_issues(args.repo, args.limit)
                print_issues(filter_issues(issues, args.actionable))
                if args.once:
                    return 0
                time.sleep(args.interval)
    except (RuntimeError, OSError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
