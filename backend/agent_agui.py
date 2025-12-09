"""
AG-UI streaming version of the meeting agent.

This module implements the AG-UI protocol for real-time streaming of:
- Text tokens as they're generated
- Tool call progress and arguments
- State snapshots with rich tool results (ICS content, markdown, etc.)

Key differences from the non-streaming agent.py:
- Uses StateDeps[AgentState] for AG-UI state synchronization
- Tools return ToolReturn with StateSnapshotEvent metadata
- Exposed as an ASGI app via AGUIApp for mounting in FastAPI
"""

import os
from datetime import UTC, datetime, timedelta

from ag_ui.core import EventType, StateSnapshotEvent
from pydantic_ai import Agent, RunContext, ToolReturn
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.ui import StateDeps
from pydantic_ai.ui.ag_ui.app import AGUIApp

from models import (
    AgentState,
    CalendarReminderInput,
    DecisionRecordInput,
    IncidentReportInput,
)
from tools import CalendarTool, DecisionRecordTool, IncidentTool

# =============================================================================
# Tool instances - created once, reused across all agent calls
# =============================================================================
_calendar_tool = CalendarTool()
_incident_tool = IncidentTool()
_decision_tool = DecisionRecordTool()


def create_agui_agent() -> Agent[StateDeps[AgentState], str]:
    """Create a PydanticAI agent configured for AG-UI streaming.

    This agent:
    - Streams text tokens in real-time via AG-UI TEXT_MESSAGE_* events
    - Announces tool calls via TOOL_CALL_* events
    - Synchronizes state (tool results) via STATE_SNAPSHOT events

    Returns:
        Agent configured with StateDeps for AG-UI state management
    """
    # Configure model for OpenRouter (or any OpenAI-compatible API)
    model = OpenAIChatModel(
        os.getenv("LLM_MODEL", "anthropic/claude-sonnet-4-5"),
        provider=OpenAIProvider(
            base_url=os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1"),
            api_key=os.getenv("LLM_API_KEY", ""),
        ),
    )

    agent: Agent[StateDeps[AgentState], str] = Agent(
        model,
        deps_type=StateDeps[AgentState],  # AG-UI state integration
        # Static instructions - core behavior that doesn't change
        instructions="""You are a meeting assistant that processes transcripts and extracts structured information.

Analyze the transcript and call the appropriate tool(s) to extract relevant information.

**Important**: You can call MULTIPLE tools for the same transcript if appropriate:
- Incident call -> incident report + calendar (for follow-up actions)
- Architecture review with implementation tasks -> decision record + calendar
- But if a meeting is ONLY about decisions (no immediate tasks) -> decision record ONLY

For calendar reminders: If the transcript mentions specific deadlines, set reminder_date 1-2 days before the earliest deadline. Otherwise use one week from today. Always use YYYY-MM-DD format.

After processing, provide a friendly 2-4 sentence summary explaining:
1. What you found in the transcript
2. What actions you took (which tools you called)
3. What the user should do next (if applicable)""",
    )

    # =========================================================================
    # Dynamic Instructions - inject current date context from state
    # =========================================================================

    @agent.instructions
    def add_date_context(ctx: RunContext[StateDeps[AgentState]]) -> str:
        """Inject current date into the system prompt dynamically."""
        state = ctx.deps.state
        current_day = datetime.now(tz=UTC).strftime("%A")
        return f"""**CURRENT DATE/TIME CONTEXT:**
- Today is {current_day}, {state.current_date}
- One week from now: {state.one_week_from_now}"""

    # =========================================================================
    # Tool Definitions - Return ToolReturn with StateSnapshotEvent
    # =========================================================================
    # Each tool:
    # 1. Updates state.current_tool to show progress indicator
    # 2. Executes the actual tool logic
    # 3. Appends result to state.tool_results
    # 4. Returns ToolReturn with StateSnapshotEvent to stream state to frontend

    @agent.tool
    async def create_calendar_reminder(
        ctx: RunContext[StateDeps[AgentState]], input_data: CalendarReminderInput
    ) -> ToolReturn:
        """Create a calendar reminder with meeting details, action items, and deadlines.

        Use this when the transcript contains:
        - Action items with owners and deadlines
        - Follow-up tasks that need tracking
        - Meeting outcomes that should be remembered
        """
        state = ctx.deps.state
        print(f"\n[calendar] Creating reminder: '{input_data.meeting_title}'")
        print(f"[calendar] {len(input_data.action_items)} action items")

        # Update state to show tool is running
        state.current_tool = "create_calendar_reminder"
        state.processing_status = "executing"

        # Execute the actual tool
        result = _calendar_tool.execute(input_data.model_dump())

        # Add result to state and clear current tool
        state.tool_results.append(result)
        state.current_tool = None

        # Build return message for LLM
        if result["status"] == "success":
            return_message = (
                f"Created calendar reminder '{input_data.meeting_title}' "
                f"for {input_data.reminder_date} with {len(input_data.action_items)} action items."
            )
        else:
            return_message = (
                f"Failed to create calendar reminder: {result.get('message', 'Unknown error')}"
            )

        # Return with StateSnapshotEvent to stream state to frontend
        return ToolReturn(
            return_value=return_message,
            metadata=[
                StateSnapshotEvent(
                    type=EventType.STATE_SNAPSHOT,
                    snapshot=state.model_dump(),
                ),
            ],
        )

    @agent.tool
    async def generate_incident_report(
        ctx: RunContext[StateDeps[AgentState]], input_data: IncidentReportInput
    ) -> ToolReturn:
        """Generate a structured incident report for production issues or outages.

        Use this when the transcript describes:
        - Production incidents, outages, or system failures
        - Emergency response calls
        - Critical issues affecting users or revenue
        - Post-mortem discussions
        """
        state = ctx.deps.state
        print(f"\n[incident] Generating report: '{input_data.incident_title}'")
        print(f"[incident] Severity: {input_data.severity}")

        # Update state to show tool is running
        state.current_tool = "generate_incident_report"
        state.processing_status = "executing"

        # Execute the actual tool
        result = _incident_tool.execute(input_data.model_dump())

        # Add result to state and clear current tool
        state.tool_results.append(result)
        state.current_tool = None

        # Build return message for LLM
        if result["status"] == "success":
            return_message = (
                f"Generated incident report for '{input_data.incident_title}' "
                f"(Severity: {input_data.severity.upper()}). "
                f"Root cause: {input_data.root_cause[:100]}..."
            )
        else:
            return_message = (
                f"Failed to generate incident report: {result.get('message', 'Unknown error')}"
            )

        # Return with StateSnapshotEvent to stream state to frontend
        return ToolReturn(
            return_value=return_message,
            metadata=[
                StateSnapshotEvent(
                    type=EventType.STATE_SNAPSHOT,
                    snapshot=state.model_dump(),
                ),
            ],
        )

    @agent.tool
    async def create_decision_record(
        ctx: RunContext[StateDeps[AgentState]], input_data: DecisionRecordInput
    ) -> ToolReturn:
        """Create an Architecture Decision Record (ADR) for strategic or technical decisions.

        Use this when the transcript describes:
        - Architectural decisions (technology stack, framework choices)
        - Strategic product decisions (feature prioritization)
        - Process decisions (workflow changes, methodologies)
        - Technical trade-off discussions with a final decision

        DO NOT use for:
        - Meetings with only action items (use create_calendar_reminder)
        - Incidents (use generate_incident_report)
        """
        state = ctx.deps.state
        print(f"\n[decision] Recording: '{input_data.decision_title}'")
        print(f"[decision] Status: {input_data.status}")

        # Update state to show tool is running
        state.current_tool = "create_decision_record"
        state.processing_status = "executing"

        # Execute the actual tool
        result = _decision_tool.execute(input_data.model_dump())

        # Add result to state and clear current tool
        state.tool_results.append(result)
        state.current_tool = None

        # Build return message for LLM
        if result["status"] == "success":
            options_count = len(input_data.options_considered)
            return_message = (
                f"Created decision record for '{input_data.decision_title}' "
                f"({options_count} options considered, decision: {input_data.status})."
            )
        else:
            return_message = (
                f"Failed to create decision record: {result.get('message', 'Unknown error')}"
            )

        # Return with StateSnapshotEvent to stream state to frontend
        return ToolReturn(
            return_value=return_message,
            metadata=[
                StateSnapshotEvent(
                    type=EventType.STATE_SNAPSHOT,
                    snapshot=state.model_dump(),
                ),
            ],
        )

    return agent


# =============================================================================
# Module-level agent singleton
# =============================================================================
_agent: Agent[StateDeps[AgentState], str] | None = None


def get_agui_agent() -> Agent[StateDeps[AgentState], str]:
    """Get or create the AG-UI meeting agent singleton."""
    global _agent
    if _agent is None:
        _agent = create_agui_agent()
        print("🤖 AG-UI PydanticAI agent initialized")
    return _agent


# =============================================================================
# AG-UI App Factory
# =============================================================================


def create_initial_state() -> AgentState:
    """Create initial state with current date context."""
    now = datetime.now(tz=UTC)
    return AgentState(
        tool_results=[],
        current_tool=None,
        processing_status="idle",
        current_date=now.strftime("%Y-%m-%d"),
        one_week_from_now=(now + timedelta(days=7)).strftime("%Y-%m-%d"),
    )


def create_agui_app() -> AGUIApp:
    """Create an AG-UI ASGI app for mounting in FastAPI.

    This creates a standalone ASGI app that:
    - Handles AG-UI protocol requests
    - Streams events (text, tool calls, state) to the frontend
    - Can be mounted at any path in FastAPI

    Usage in FastAPI:
        from agent_agui import create_agui_app
        app.mount("/api/agent", create_agui_app())
    """
    agent = get_agui_agent()
    initial_state = create_initial_state()

    return AGUIApp(
        agent,
        deps=StateDeps(initial_state),
    )
