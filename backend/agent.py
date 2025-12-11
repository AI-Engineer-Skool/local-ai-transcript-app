"""
PydanticAI agent for transcript processing.

Key differences from raw OpenAI function calling:
- Tools are defined with @agent.tool decorators (not JSON schemas)
- Tool inputs are validated Pydantic models (not json.loads())
- Dependencies are injected via RunContext (not manual passing)
- Date context is injected via @agent.instructions (not a separate tool)
- Tool call names/inputs extracted from result.all_messages()
- Rich tool results (files, markdown) accumulated in ctx.deps.tool_results
"""

import json
import os
from datetime import UTC, datetime, timedelta
from typing import Any

from pydantic_ai import Agent, RunContext
from pydantic_ai.messages import (
    ModelMessage,
    ModelResponse,
    ToolCallPart,
    ToolReturnPart,
)
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from models import (
    AgentDeps,
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


def create_meeting_agent() -> Agent[AgentDeps, str]:
    """Create a PydanticAI agent configured for meeting transcript processing.

    Returns an Agent that:
    - Analyzes transcripts and decides which tools to call
    - Automatically validates tool inputs against Pydantic models
    - Returns a natural language summary of what was done
    """
    # Configure model for OpenRouter (or any OpenAI-compatible API)
    model = OpenAIChatModel(
        os.getenv("LLM_MODEL", "anthropic/claude-sonnet-4-5"),
        provider=OpenAIProvider(
            base_url=os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1"),
            api_key=os.getenv("LLM_API_KEY", ""),
        ),
    )

    agent: Agent[AgentDeps, str] = Agent(
        model,
        deps_type=AgentDeps,
        # Static instructions - core behavior that doesn't change
        instructions="""You are a meeting assistant that processes transcripts and extracts structured information.

Analyze the transcript and call the appropriate tool(s) to extract relevant information.

**Important**: You can call MULTIPLE tools for the same transcript if appropriate:
- Incident call -> incident report + calendar (for follow-up actions)
- Architecture review with implementation tasks -> decision record + calendar
- But if a meeting is ONLY about decisions (no immediate tasks) -> decision record ONLY

For calendar reminders: If the transcript mentions specific deadlines, set reminder_date 1-2 days before the earliest deadline. Otherwise use one week from today. Always use YYYY-MM-DD format.

After processing, provide a well-formatted summary using Markdown:
- A brief opening sentence about what you found
- A bulleted list of actions taken (use **bold** for key items)
- Any next steps for the user

Use proper Markdown formatting:
- Use **bold** for emphasis on important items
- Use bullet points (`-`) for lists
- Keep paragraphs separated with blank lines
- Be concise but clear (3-5 short paragraphs or bullet sections)

IMPORTANT: Do NOT use emojis or excited openings like "Analysis Complete!" or "Great news!". Just start directly with the content in a professional tone.""",
    )

    # =========================================================================
    # Dynamic Instructions - inject current date context
    # =========================================================================
    # This is the idiomatic PydanticAI way to provide runtime context,
    # instead of creating a separate "get_current_date" tool.

    @agent.instructions
    def add_date_context(ctx: RunContext[AgentDeps]) -> str:
        """Inject current date into the system prompt dynamically."""
        return f"""**CURRENT DATE/TIME CONTEXT:**
- Today is {ctx.deps.current_day}, {ctx.deps.current_date}
- One week from now: {ctx.deps.one_week_from_now}"""

    # =========================================================================
    # Tool Definitions - Using @agent.tool decorator
    # =========================================================================
    # Each tool receives:
    # - ctx: RunContext[AgentDeps] with injected dependencies
    # - Pydantic model with validated input (no json.loads needed!)
    #
    # Tools return a string describing the result, which PydanticAI uses
    # to inform subsequent LLM responses.

    @agent.tool
    async def create_calendar_reminder(
        ctx: RunContext[AgentDeps], input_data: CalendarReminderInput
    ) -> str:
        """Create a calendar reminder with meeting details, action items, and deadlines.

        Use this when the transcript contains:
        - Action items with owners and deadlines
        - Follow-up tasks that need tracking
        - Meeting outcomes that should be remembered
        """
        print(f"\n[calendar] Creating reminder: '{input_data.meeting_title}'")
        print(f"[calendar] {len(input_data.action_items)} action items")

        result = _calendar_tool.execute(input_data.model_dump())
        ctx.deps.tool_results.append(result)  # Store full result for frontend

        if result["status"] == "success":
            return (
                f"Created calendar reminder '{input_data.meeting_title}' "
                f"for {input_data.reminder_date} with {len(input_data.action_items)} action items."
            )
        return f"Failed to create calendar reminder: {result.get('message', 'Unknown error')}"

    @agent.tool
    async def generate_incident_report(
        ctx: RunContext[AgentDeps], input_data: IncidentReportInput
    ) -> str:
        """Generate a structured incident report for production issues or outages.

        Use this when the transcript describes:
        - Production incidents, outages, or system failures
        - Emergency response calls
        - Critical issues affecting users or revenue
        - Post-mortem discussions
        """
        print(f"\n[incident] Generating report: '{input_data.incident_title}'")
        print(f"[incident] Severity: {input_data.severity}")

        result = _incident_tool.execute(input_data.model_dump())
        ctx.deps.tool_results.append(result)  # Store full result for frontend

        if result["status"] == "success":
            return (
                f"Generated incident report for '{input_data.incident_title}' "
                f"(Severity: {input_data.severity.upper()}). "
                f"Root cause: {input_data.root_cause[:100]}..."
            )
        return f"Failed to generate incident report: {result.get('message', 'Unknown error')}"

    @agent.tool
    async def create_decision_record(
        ctx: RunContext[AgentDeps], input_data: DecisionRecordInput
    ) -> str:
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
        print(f"\n[decision] Recording: '{input_data.decision_title}'")
        print(f"[decision] Status: {input_data.status}")

        result = _decision_tool.execute(input_data.model_dump())
        ctx.deps.tool_results.append(result)  # Store full result for frontend

        if result["status"] == "success":
            options_count = len(input_data.options_considered)
            return (
                f"Created decision record for '{input_data.decision_title}' "
                f"({options_count} options considered, decision: {input_data.status})."
            )
        return f"Failed to create decision record: {result.get('message', 'Unknown error')}"

    return agent


# =============================================================================
# Module-level agent singleton
# =============================================================================
_agent: Agent[AgentDeps, str] | None = None


def get_agent() -> Agent[AgentDeps, str]:
    """Get or create the meeting agent singleton."""
    global _agent
    if _agent is None:
        _agent = create_meeting_agent()
        print("🤖 PydanticAI agent initialized")
    return _agent


# =============================================================================
# Message History Parsing - Extract tool calls from PydanticAI messages
# =============================================================================


def extract_tool_calls_from_messages(
    messages: list[ModelMessage],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Extract tool calls and results from PydanticAI message history.

    This is the idiomatic way to get tool call information - by parsing
    the message history rather than manually tracking in dependencies.

    Returns:
        tuple of (tool_calls, results) where:
        - tool_calls: list of {"name": str, "input": dict}
        - results: list of tool execution results
    """
    tool_calls: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []

    # Map tool_call_id to its arguments for pairing with results
    call_id_to_args: dict[str, dict[str, Any]] = {}

    for message in messages:
        if isinstance(message, ModelResponse):
            # Extract tool calls from ModelResponse
            for part in message.parts:
                if isinstance(part, ToolCallPart):
                    # Parse args - could be dict or JSON string
                    args = part.args
                    if isinstance(args, str):
                        args = json.loads(args)

                    tool_calls.append(
                        {
                            "name": part.tool_name,
                            "input": args,
                        }
                    )
                    call_id_to_args[part.tool_call_id] = args

                elif isinstance(part, ToolReturnPart):
                    # Tool return contains the result
                    # The content is the string returned by our tool function
                    result_content = part.content

                    # For frontend compatibility, wrap in expected format
                    # Our tools return success/failure strings
                    if "Failed" in str(result_content):
                        results.append(
                            {
                                "status": "error",
                                "message": result_content,
                            }
                        )
                    else:
                        results.append(
                            {
                                "status": "success",
                                "message": result_content,
                                "type": _infer_result_type(part.tool_name),
                            }
                        )

    return tool_calls, results


def _infer_result_type(tool_name: str) -> str:
    """Infer the result type from tool name for frontend display."""
    type_map = {
        "create_calendar_reminder": "calendar",
        "generate_incident_report": "incident",
        "create_decision_record": "decision",
    }
    return type_map.get(tool_name, "unknown")


# =============================================================================
# Main Processing Function
# =============================================================================


async def process_transcript(transcript: str) -> dict[str, Any]:
    """Process a transcript using the PydanticAI agent.

    This replaces the old 3-phase workflow (select tools, execute, summarize)
    with PydanticAI's automatic tool handling.

    Args:
        transcript: The meeting transcript to process

    Returns:
        dict with:
        - success: bool
        - tool_calls: list of tool invocations with inputs
        - results: list of tool execution results
        - summary: natural language summary from the agent
    """
    if not transcript:
        return {
            "success": True,
            "tool_calls": [],
            "results": [],
            "summary": "No transcript provided.",
        }

    print("\n🤖 Processing transcript with PydanticAI agent...")
    preview = transcript[:150] + "..." if len(transcript) > 150 else transcript
    print(f"📋 Preview: {preview}\n")

    # Create dependencies with current date context
    # tool_results will accumulate rich execution results during processing
    now = datetime.now(tz=UTC)
    deps = AgentDeps(
        current_date=now.strftime("%Y-%m-%d"),
        current_day=now.strftime("%A"),
        one_week_from_now=(now + timedelta(days=7)).strftime("%Y-%m-%d"),
        tool_results=[],
    )

    try:
        agent = get_agent()
        result = await agent.run(
            f"Process this meeting transcript:\n\n{transcript}",
            deps=deps,
        )

        # Extract tool calls from message history (for names and inputs)
        tool_calls, _ = extract_tool_calls_from_messages(result.all_messages())

        # Use the rich results captured during tool execution (stored in deps)
        # These contain full data: ICS content, markdown, filenames, etc.
        results = deps.tool_results

        print(f"\n✅ Processing complete: {len(tool_calls)} tool(s) executed")
        print(f"📝 Summary: {result.output[:200]}...")

        return {
            "success": True,
            "tool_calls": tool_calls,
            "results": results,
            "summary": result.output,
        }

    except Exception as e:
        print(f"\n⚠️  Agent error: {e}")
        return {
            "success": False,
            "tool_calls": [],
            "results": [],
            "summary": f"Error processing transcript: {str(e)}",
            "error": str(e),
        }
