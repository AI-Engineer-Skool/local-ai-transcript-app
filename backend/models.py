"""
Pydantic models for tool inputs.

These replace the manual JSON schemas in each tool's input_schema property.
With PydanticAI, the LLM response is automatically validated against these models.
"""

from dataclasses import dataclass, field
from typing import Any, Literal

from pydantic import BaseModel, Field

# =============================================================================
# Shared Models (used across multiple tools)
# =============================================================================


class ActionItem(BaseModel):
    """A single action item from a meeting."""

    task: str = Field(description="The action item or task")
    owner: str = Field(description="Person responsible")
    priority: Literal["high", "medium", "low"] = Field(
        default="medium", description="Priority level"
    )
    due_date: str | None = Field(
        default=None, description="When it's due (e.g., 'end of week', 'Dec 10')"
    )


class Blocker(BaseModel):
    """A blocker or impediment mentioned in the meeting."""

    blocker: str
    affected_person: str


class UrgentIssue(BaseModel):
    """A critical or urgent issue requiring attention."""

    issue: str
    severity: Literal["critical", "high", "medium"]


# =============================================================================
# CalendarTool Input Model
# =============================================================================


class CalendarReminderInput(BaseModel):
    """Input for creating a calendar reminder from meeting details.

    Replaces the 75-line JSON schema in calendar_tool.py.
    """

    meeting_title: str = Field(description="Title or topic of the meeting")
    meeting_type: Literal[
        "standup",
        "planning",
        "brainstorm",
        "review",
        "client_call",
        "interview",
        "status_update",
        "retrospective",
        "other",
    ] = Field(description="Type of meeting")
    meeting_summary: str = Field(
        description="2-3 sentence summary of what was discussed"
    )
    key_points: list[str] = Field(
        description="Important points or decisions from the meeting"
    )
    action_items: list[ActionItem] = Field(description="Action items from the meeting")
    blockers: list[Blocker] = Field(
        default_factory=list, description="Blockers or impediments mentioned"
    )
    urgent_issues: list[UrgentIssue] = Field(
        default_factory=list, description="Critical or urgent issues"
    )
    reminder_date: str = Field(
        description="Calendar reminder date in YYYY-MM-DD format"
    )


# =============================================================================
# IncidentTool Input Model
# =============================================================================


class TimelineEvent(BaseModel):
    """A single event in the incident timeline."""

    time: str = Field(description="Time of the event (e.g., '10:15 AM')")
    event: str = Field(description="What happened at this time")
    actor: str | None = Field(
        default=None, description="Who performed the action or discovered the event"
    )


class BusinessImpact(BaseModel):
    """Quantitative and qualitative business impact of an incident."""

    description: str = Field(description="Overall description of business impact")
    downtime_duration: str | None = Field(
        default=None, description="Duration of downtime (e.g., '15 minutes')"
    )
    affected_users: str | None = Field(
        default=None, description="Number of affected users (e.g., '200 users')"
    )
    failed_transactions: str | None = Field(
        default=None, description="Number of failed transactions"
    )
    revenue_impact: str | None = Field(
        default=None, description="Revenue loss or financial impact"
    )


class FollowUpAction(BaseModel):
    """A follow-up action to prevent incident recurrence."""

    action: str = Field(description="Follow-up action to prevent recurrence")
    owner: str = Field(description="Person responsible for the action")
    priority: Literal["high", "medium", "low"] = Field(
        default="medium", description="Priority level"
    )
    due_date: str | None = Field(
        default=None, description="When the action should be completed"
    )


class IncidentReportInput(BaseModel):
    """Input for generating an incident report.

    Replaces the 130-line JSON schema in incident_tool.py.
    """

    incident_title: str = Field(
        description="Clear, concise title describing the incident"
    )
    severity: Literal["critical", "high", "medium", "low"] = Field(
        description="Severity level based on business impact"
    )
    start_time: str = Field(description="When the incident started")
    detection_time: str | None = Field(
        default=None, description="When the incident was detected"
    )
    resolution_time: str | None = Field(
        default=None, description="When resolved, or 'ongoing'"
    )
    root_cause: str = Field(description="Root cause if identified")
    business_impact: BusinessImpact = Field(
        description="Business impact of the incident"
    )
    timeline: list[TimelineEvent] = Field(
        description="Chronological timeline of events"
    )
    resolution_steps: list[str] = Field(description="Steps taken to resolve")
    stakeholders_notified: list[str] = Field(
        default_factory=list, description="People or teams notified"
    )
    follow_up_actions: list[FollowUpAction] = Field(
        default_factory=list, description="Post-incident follow-up actions"
    )
    additional_notes: str | None = Field(
        default=None, description="Additional context or notes"
    )


# =============================================================================
# DecisionRecordTool Input Model
# =============================================================================


class OptionConsidered(BaseModel):
    """An option that was considered during decision-making."""

    option: str = Field(description="The option/alternative considered")
    pros: list[str] = Field(default_factory=list, description="Advantages")
    cons: list[str] = Field(default_factory=list, description="Disadvantages")


class Consequences(BaseModel):
    """Expected consequences and trade-offs of a decision."""

    positive: list[str] = Field(
        default_factory=list, description="Positive outcomes and benefits"
    )
    negative: list[str] = Field(
        default_factory=list, description="Negative consequences or trade-offs"
    )
    risks: list[str] = Field(
        default_factory=list, description="Potential risks to monitor"
    )


class DecisionRecordInput(BaseModel):
    """Input for creating an Architecture Decision Record (ADR).

    Replaces the 90-line JSON schema in decision_record_tool.py.
    """

    decision_title: str = Field(description="Clear, concise title of the decision")
    decision_date: str = Field(description="Date in YYYY-MM-DD format")
    status: Literal["proposed", "accepted", "rejected", "deprecated", "superseded"] = (
        Field(description="Status of the decision")
    )
    context: str = Field(
        description="Background - what problem or need led to this decision?"
    )
    options_considered: list[OptionConsidered] = Field(
        description="All options/alternatives considered"
    )
    decision: str = Field(description="The final decision - which option was chosen")
    rationale: str = Field(
        description="Why this decision was made - the reasoning and key factors"
    )
    consequences: Consequences | None = Field(
        default=None, description="Expected consequences and trade-offs"
    )
    decision_makers: list[str] = Field(
        default_factory=list, description="People who participated in making this"
    )
    additional_notes: str | None = Field(
        default=None, description="Additional context or constraints"
    )


# =============================================================================
# Dependencies for PydanticAI RunContext
# =============================================================================


@dataclass
class AgentDeps:
    """Dependencies injected into the PydanticAI agent via RunContext.

    Access in tools via: ctx.deps.current_date

    The tool_results list accumulates rich execution results during processing.
    Each tool appends its full result dict (with content, markdown, filenames, etc.)
    so the frontend receives complete data for rendering.
    """

    current_date: str
    one_week_from_now: str
    current_day: str
    tool_results: list[dict[str, Any]] = field(default_factory=list)
