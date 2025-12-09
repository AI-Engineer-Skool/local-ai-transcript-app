"""
Exercise 5: Full Pattern - Pydantic Models as Tool Inputs

Concept: This exercise combines all previous concepts into the pattern used
in agent.py: Pydantic models for tool inputs, dependencies for context,
dynamic instructions, and message parsing for tool call extraction.

Difficulty: Advanced

Run: uv run python exercises/05_full_pattern.py
"""

import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Literal

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.messages import ModelResponse, ToolCallPart
from pydantic_ai.models.test import TestModel

# =============================================================================
# PYDANTIC MODELS FOR TOOL INPUTS
# =============================================================================


class ActionItem(BaseModel):
    """A single action item - nested in TaskSummaryInput."""

    task: str = Field(description="The action item or task")
    owner: str = Field(description="Person responsible")
    priority: Literal["high", "medium", "low"] = Field(
        default="medium", description="Priority level"
    )


class TaskSummaryInput(BaseModel):
    """Input model for the create_task_summary tool.

    This mirrors models like CalendarReminderInput in models.py.
    The LLM fills this out based on the transcript/prompt.
    """

    meeting_title: str = Field(description="Title of the meeting")
    summary: str = Field(description="Brief summary of what was discussed")
    action_items: list[ActionItem] = Field(
        description="Action items extracted from the meeting"
    )
    next_steps: list[str] = Field(
        default_factory=list, description="Recommended next steps"
    )


# =============================================================================
# DEPENDENCIES
# =============================================================================


@dataclass
class MeetingAgentDeps:
    """Dependencies for the meeting agent.

    Mirrors AgentDeps in models.py:
    - Runtime context (current_date, etc.)
    - Mutable state for collecting tool results
    """

    current_date: str
    current_day: str
    one_week_from_now: str
    tool_results: list[dict[str, Any]] = field(default_factory=list)


# =============================================================================
# AGENT CREATION
# =============================================================================


def create_meeting_agent() -> Agent[MeetingAgentDeps, str]:
    """Create a meeting processing agent.

    This mirrors the pattern in agent.py:
    1. Static instructions for core behavior
    2. Dynamic instructions for runtime context
    3. Tools with Pydantic model inputs
    4. Results accumulated in dependencies
    """
    model = TestModel()

    agent: Agent[MeetingAgentDeps, str] = Agent(
        model,
        deps_type=MeetingAgentDeps,
        instructions="""You are a meeting assistant that processes meeting notes.

Analyze the content and use the appropriate tool(s) to extract structured information.
After processing, provide a friendly summary of what you did.""",
    )

    # Dynamic instructions - inject current date (like agent.py does)
    @agent.instructions
    def add_date_context(ctx: RunContext[MeetingAgentDeps]) -> str:
        """Inject current date into instructions at runtime."""
        return f"""**CURRENT DATE CONTEXT:**
- Today is {ctx.deps.current_day}, {ctx.deps.current_date}
- One week from now: {ctx.deps.one_week_from_now}"""

    # Tool with Pydantic model input
    @agent.tool
    async def create_task_summary(
        ctx: RunContext[MeetingAgentDeps], input_data: TaskSummaryInput
    ) -> str:
        """Create a task summary from meeting content.

        Use this when the content contains:
        - Action items with owners
        - Tasks that need tracking
        - Meeting outcomes to document

        Args:
            ctx: RunContext with dependencies
            input_data: Validated TaskSummaryInput model
        """
        print(f"\n[tool] Creating summary: '{input_data.meeting_title}'")
        print(f"[tool] {len(input_data.action_items)} action items")

        # Store rich result in deps (for frontend/later processing)
        result = {
            "status": "success",
            "type": "task_summary",
            "data": input_data.model_dump(),
            "created_at": ctx.deps.current_date,
        }
        ctx.deps.tool_results.append(result)

        # Return string for LLM to incorporate in response
        return (
            f"Created task summary '{input_data.meeting_title}' "
            f"with {len(input_data.action_items)} action items."
        )

    return agent


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def create_deps() -> MeetingAgentDeps:
    """Create dependencies with current date context."""
    now = datetime.now()
    return MeetingAgentDeps(
        current_date=now.strftime("%Y-%m-%d"),
        current_day=now.strftime("%A"),
        one_week_from_now=(now + timedelta(days=7)).strftime("%Y-%m-%d"),
        tool_results=[],
    )


def extract_tool_calls(result: Any) -> list[dict[str, Any]]:
    """Extract tool calls from agent result messages.

    This mirrors extract_tool_calls_from_messages() in agent.py.
    """
    tool_calls = []

    for message in result.all_messages():
        if isinstance(message, ModelResponse):
            for part in message.parts:
                if isinstance(part, ToolCallPart):
                    args = part.args
                    if isinstance(args, str):
                        args = json.loads(args)
                    tool_calls.append({"name": part.tool_name, "input": args})

    return tool_calls


# =============================================================================
# DEMO
# =============================================================================


def demo_full_pattern():
    """Demonstrate the complete pattern used in agent.py."""
    print("=" * 60)
    print("DEMO: Full Pattern (mirrors agent.py)")
    print("=" * 60)

    agent = create_meeting_agent()
    deps = create_deps()

    print("\nDependencies:")
    print(f"  current_date: {deps.current_date}")
    print(f"  current_day: {deps.current_day}")
    print(f"  one_week_from_now: {deps.one_week_from_now}")

    # Process a meeting note
    meeting_note = """
    Sprint Planning Meeting - Dec 9, 2024

    Attendees: Alice, Bob, Charlie

    Discussion:
    - Reviewed Q4 roadmap progress
    - API redesign is on track
    - Need to finalize testing strategy

    Action Items:
    - Alice: Complete API documentation by Friday (high priority)
    - Bob: Set up integration tests (medium priority)
    - Charlie: Review security audit findings (high priority)

    Next meeting: Dec 16
    """

    print(f"\nProcessing meeting note ({len(meeting_note)} chars)...")

    # Run the agent
    import asyncio

    async def run():
        return await agent.run(
            f"Process this meeting note:\n\n{meeting_note}",
            deps=deps,
        )

    result = asyncio.run(run())

    # Show results
    print("\n--- RESULTS ---")
    print(f"Agent output: {result.output}")
    print("\nTool results accumulated in deps:")
    for tr in deps.tool_results:
        print(f"  {json.dumps(tr, indent=2)}")

    # Extract tool calls from messages
    tool_calls = extract_tool_calls(result)
    print("\nTool calls extracted from messages:")
    for tc in tool_calls:
        print(f"  Tool: {tc['name']}")
        print(f"  Input: {json.dumps(tc['input'], indent=4)[:200]}...")


if __name__ == "__main__":
    demo_full_pattern()

    print("\n" + "=" * 60)
    print("BASE CODE COMPLETE - Try the challenges below!")
    print("=" * 60)


# =============================================================================
# CHALLENGES
# =============================================================================

# -----------------------------------------------------------------------------
# Challenge 1: Add a second tool with a different input model
# -----------------------------------------------------------------------------
# Create an UrgentIssueInput model and add an urgent_issue_report tool:
#
#   class UrgentIssueInput(BaseModel):
#       issue_title: str = Field(description="Title of the urgent issue")
#       severity: Literal["critical", "high", "medium"] = Field(...)
#       affected_systems: list[str] = Field(...)
#       immediate_actions: list[str] = Field(...)
#
#   @agent.tool
#   async def report_urgent_issue(
#       ctx: RunContext[MeetingAgentDeps], input_data: UrgentIssueInput
#   ) -> str:
#       ...
#
# Test with a meeting note that mentions an urgent production issue.

# -----------------------------------------------------------------------------
# Challenge 2: Extract tool calls from result.all_messages()
# -----------------------------------------------------------------------------
# Enhance extract_tool_calls() to also extract:
# - Tool return values (ToolReturnPart)
# - Match them up with their corresponding calls
#
# Hint: Look at how agent.py does this in extract_tool_calls_from_messages()
#
#   from pydantic_ai.messages import ToolReturnPart
#
#   elif isinstance(part, ToolReturnPart):
#       # part.content contains the tool's return value

# -----------------------------------------------------------------------------
# Challenge 3: Create a mini transcript processor
# -----------------------------------------------------------------------------
# Build a simplified version of the main app's agent:
#
# 1. Add 2-3 tools (task summary, decision record, urgent issue)
# 2. Process different types of meeting notes
# 3. Return structured results with:
#    - tool_calls: list of tool invocations
#    - results: list of tool results (from deps.tool_results)
#    - summary: the agent's output string
#
# This is essentially what process_transcript() in agent.py does!
#
# async def process_meeting(text: str) -> dict[str, Any]:
#     agent = create_meeting_agent()
#     deps = create_deps()
#     result = await agent.run(f"Process:\n\n{text}", deps=deps)
#     tool_calls = extract_tool_calls(result)
#     return {
#         "success": True,
#         "tool_calls": tool_calls,
#         "results": deps.tool_results,
#         "summary": result.output,
#     }
