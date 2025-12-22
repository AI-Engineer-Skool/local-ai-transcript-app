"""
GitHub Integration - REST API for Issue Creation

This module creates GitHub issues from transcript analysis results.

WHY REST (not MCP) HERE:
We know exactly what we want: create an issue with specific content.
No discovery needed, no dynamic tool selection - just a simple HTTP POST.
REST is the right choice for known, single operations.

For dynamic tool discovery (where an agent decides what to do),
see github_issue_agent.py which uses MCP appropriately.

Issue Format:
All issues are created with a consistent structure featuring checkbox
action items. This format is understood by both:
1. This module (creates issues)
2. The Issue Review Agent (analyzes/updates issues via MCP)

Usage:
    from github_integration import create_github_issue, write_issue

    # Direct issue creation
    result = await create_github_issue(
        title="[Incident] Payment API Outage",
        body="## Summary\\n...",
        labels=["incident", "critical"]
    )

    # From structured tool data
    result = await write_issue("incident_report", tool_data)
"""

import os
from typing import Any

import httpx

GITHUB_API_URL = "https://api.github.com"

# Label added to all issues for the review agent to find
TRANSCRIPT_APP_LABEL = "transcript-app"


def check_github_config() -> bool:
    """Check and log GitHub configuration status at startup."""
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_ISSUES_REPO")

    if not token:
        print("[github] GitHub integration: DISABLED (GITHUB_TOKEN not set)")
        return False

    if not repo:
        print("[github] GitHub integration: DISABLED (GITHUB_ISSUES_REPO not set)")
        return False

    if "/" not in repo:
        print(
            f"[github] GitHub integration: DISABLED "
            f"(invalid GITHUB_ISSUES_REPO format: '{repo}', expected 'owner/repo')"
        )
        return False

    print(f"[github] GitHub integration: ENABLED (repo={repo})")
    return True


async def create_github_issue(
    title: str,
    body: str,
    labels: list[str] | None = None,
) -> dict:
    """Create a GitHub issue via REST API.

    WHY REST: We know exactly what we want (create issue).
    No discovery needed. Simple HTTP POST.

    Args:
        title: Issue title
        body: Issue body (markdown)
        labels: Optional list of label names

    Returns:
        dict with status, issue_url, issue_number on success
        dict with status, message on error
    """
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_ISSUES_REPO")

    if not token or not repo:
        print("[github] Skipping - GITHUB_TOKEN or GITHUB_ISSUES_REPO not set")
        return {"status": "skipped", "message": "GitHub not configured"}

    try:
        owner, repo_name = repo.split("/")
    except ValueError:
        return {"status": "error", "message": f"Invalid repo format: {repo}"}

    url = f"{GITHUB_API_URL}/repos/{owner}/{repo_name}/issues"

    # Always add transcript-app label for the review agent to find
    all_labels = list(set((labels or []) + [TRANSCRIPT_APP_LABEL]))

    payload = {
        "title": title,
        "body": body,
        "labels": all_labels,
    }

    print(f"[github] Creating issue: {title}")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28",
                },
                json=payload,
                timeout=30.0,
            )

        if response.status_code == 201:
            data = response.json()
            print(f"[github] Created: {data['html_url']}")
            return {
                "status": "success",
                "issue_url": data["html_url"],
                "issue_number": data["number"],
            }

        error_msg = response.text
        print(f"[github] Failed ({response.status_code}): {error_msg}")
        return {
            "status": "error",
            "message": f"GitHub API error {response.status_code}: {error_msg}",
        }

    except httpx.TimeoutException:
        print("[github] Request timed out")
        return {"status": "error", "message": "Request timed out"}
    except httpx.RequestError as e:
        print(f"[github] Request failed: {e}")
        return {"status": "error", "message": str(e)}


def _format_action_item(item: dict) -> str:
    """Format a single action item as a GitHub checkbox.

    Format: - [ ] Task description (@owner, due: YYYY-MM-DD, priority: high)

    This consistent format is parsed by the Issue Review Agent.
    """
    task = item.get("task") or item.get("action", "No task")
    owner = item.get("owner", "unassigned")
    priority = item.get("priority", "")
    due_date = item.get("due_date", "")

    # Build metadata string
    metadata_parts = [f"@{owner}"]
    if due_date:
        metadata_parts.append(f"due: {due_date}")
    if priority and priority.lower() != "normal":
        metadata_parts.append(f"priority: {priority}")

    metadata = ", ".join(metadata_parts)
    return f"- [ ] {task} ({metadata})"


def _format_issue_from_data(content_type: str, data: dict[str, Any]) -> tuple[str, str, list[str]]:
    """Format structured data into GitHub issue title, body, and labels.

    All issue types use a consistent format with checkbox action items.
    This format is understood by the Issue Review Agent (github_issue_agent.py).

    Args:
        content_type: Type of content (e.g., 'incident_report', 'decision_record')
        data: Structured data from the tool

    Returns:
        Tuple of (title, body, labels)
    """
    if content_type == "incident_report":
        return _format_incident_issue(data)
    if content_type == "decision_record":
        return _format_decision_issue(data)
    if content_type == "meeting_summary":
        return _format_meeting_issue(data)
    return _format_generic_issue(content_type, data)


def _format_incident_issue(data: dict[str, Any]) -> tuple[str, str, list[str]]:
    """Format incident report as GitHub issue."""
    title = f"[Incident] {data.get('incident_title', data.get('title', 'Untitled'))}"
    severity = data.get("severity", "unknown").lower()
    labels = ["incident", severity]

    # Build body with consistent structure
    body_parts = [
        "## Summary",
        "",
        f"**Severity:** {severity.upper()}",
        f"**Root Cause:** {data.get('root_cause', 'Unknown')}",
        "",
    ]

    # Timeline section
    timeline = data.get("timeline", [])
    if timeline:
        body_parts.append("## Timeline")
        body_parts.append("")
        for event in timeline:
            time = event.get("time", "?")
            desc = event.get("event", "?")
            actor = event.get("actor", "")
            actor_str = f" ({actor})" if actor else ""
            body_parts.append(f"- **{time}:** {desc}{actor_str}")
        body_parts.append("")

    # Action items section (checkbox format)
    action_items = data.get("follow_up_actions", data.get("action_items", []))
    if action_items:
        body_parts.append("## Action Items")
        body_parts.append("")
        for item in action_items:
            body_parts.append(_format_action_item(item))
        body_parts.append("")

    # Footer
    body_parts.append("---")
    body_parts.append("*Created by Transcript App*")

    return title, "\n".join(body_parts), labels


def _format_consequences(consequences: dict[str, Any] | str | None) -> list[str]:
    """Format consequences into markdown lines.

    Handles both structured format (from DecisionRecordTool) and plain string.
    """
    if not consequences:
        return ["No consequences listed."]

    # Handle plain string format
    if isinstance(consequences, str):
        return [consequences]

    # Handle structured format: {positive: [], negative: [], risks: []}
    lines = []

    positive = consequences.get("positive", [])
    if positive:
        lines.append("**Positive:**")
        for item in positive:
            lines.append(f"- {item}")
        lines.append("")

    negative = consequences.get("negative", [])
    if negative:
        lines.append("**Negative:**")
        for item in negative:
            lines.append(f"- {item}")
        lines.append("")

    risks = consequences.get("risks", [])
    if risks:
        lines.append("**Risks:**")
        for item in risks:
            lines.append(f"- {item}")

    return lines if lines else ["No consequences listed."]


def _format_decision_issue(data: dict[str, Any]) -> tuple[str, str, list[str]]:
    """Format architecture decision record as GitHub issue."""
    title = f"[ADR] {data.get('title', data.get('decision_title', 'Untitled Decision'))}"
    labels = ["adr", "decision"]

    body_parts = [
        "## Summary",
        "",
        f"**Status:** {data.get('status', 'Proposed')}",
        f"**Date:** {data.get('date', data.get('decision_date', 'Unknown'))}",
        "",
        "## Context",
        "",
        data.get("context", "No context provided."),
        "",
        "## Decision",
        "",
        data.get("decision", "No decision provided."),
        "",
        "## Consequences",
        "",
        *_format_consequences(data.get("consequences")),
        "",
    ]

    # Action items for implementation
    action_items = data.get("action_items", [])
    if action_items:
        body_parts.append("## Action Items")
        body_parts.append("")
        for item in action_items:
            body_parts.append(_format_action_item(item))
        body_parts.append("")

    # Footer
    body_parts.append("---")
    body_parts.append("*Created by Transcript App*")

    return title, "\n".join(body_parts), labels


def _format_meeting_issue(data: dict[str, Any]) -> tuple[str, str, list[str]]:
    """Format meeting summary as GitHub issue."""
    meeting_type = data.get("meeting_type", "meeting").replace("_", " ").title()
    title = f"[{meeting_type}] {data.get('meeting_title', 'Untitled Meeting')}"
    labels = ["meeting", data.get("meeting_type", "general")]

    body_parts = [
        "## Summary",
        "",
        data.get("summary", "No summary provided."),
        "",
    ]

    # Key decisions
    decisions = data.get("key_decisions", [])
    if decisions:
        body_parts.append("## Key Decisions")
        body_parts.append("")
        for decision in decisions:
            body_parts.append(f"- {decision}")
        body_parts.append("")

    # Action items (checkbox format)
    action_items = data.get("action_items", [])
    if action_items:
        body_parts.append("## Action Items")
        body_parts.append("")
        for item in action_items:
            body_parts.append(_format_action_item(item))
        body_parts.append("")

    # Footer
    body_parts.append("---")
    body_parts.append("*Created by Transcript App*")

    return title, "\n".join(body_parts), labels


def _format_generic_issue(content_type: str, data: dict[str, Any]) -> tuple[str, str, list[str]]:
    """Format unknown content types as GitHub issue."""
    type_label = content_type.replace("_", " ").title()
    title = f"[{type_label}] {data.get('title', 'Untitled')}"
    labels = [content_type.replace("_", "-")]

    body_parts = [
        "## Summary",
        "",
        data.get("summary", data.get("description", "No summary provided.")),
        "",
    ]

    # Try to find action items in common field names
    action_items = (
        data.get("action_items", [])
        or data.get("tasks", [])
        or data.get("follow_up_actions", [])
    )
    if action_items:
        body_parts.append("## Action Items")
        body_parts.append("")
        for item in action_items:
            if isinstance(item, str):
                body_parts.append(f"- [ ] {item} (@unassigned)")
            else:
                body_parts.append(_format_action_item(item))
        body_parts.append("")

    # Footer
    body_parts.append("---")
    body_parts.append("*Created by Transcript App*")

    return title, "\n".join(body_parts), labels


async def write_issue(
    content_type: str,
    data: dict[str, Any],
) -> dict[str, Any] | None:
    """Format and publish a GitHub issue from structured tool data.

    This is the main entry point for agent tools that want to create issues.

    Args:
        content_type: Type of content (e.g., 'incident_report', 'decision_record')
        data: Structured data from the tool

    Returns:
        dict with status and result details, or None if GitHub not configured
    """
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_ISSUES_REPO")

    if not token or not repo:
        print("[github] Skipping issue creation - GitHub not configured")
        return None

    try:
        title, body, labels = _format_issue_from_data(content_type, data)
        result = await create_github_issue(title, body, labels)

        # Add metadata to result
        result["content_type"] = content_type
        result["repo"] = repo

        return result

    except Exception as e:
        print(f"[github] Error creating issue: {e}")
        return {"status": "error", "message": str(e)}
