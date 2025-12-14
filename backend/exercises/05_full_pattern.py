"""
Exercise 5: The Full Pattern - Putting It All Together
======================================================

This is the capstone exercise! You'll combine everything from Exercises 1-4
into the complete pattern used by production AI agents. By the end, you'll
understand:

- How Pydantic models become tool inputs (LLM fills them out!)
- How dependencies provide runtime context
- How dynamic instructions inject context into prompts
- How to extract tool calls from message history

This is exactly how the main agent.py in this project works.

Difficulty: Advanced
Time: ~60 minutes

Run: uv run python exercises/05_full_pattern_v2.py

📚 DOCUMENTATION LINKS (bookmark these!):
- PydanticAI Tools: https://ai.pydantic.dev/tools/
- PydanticAI Dependencies: https://ai.pydantic.dev/dependencies/
- PydanticAI Results: https://ai.pydantic.dev/results/
- Pydantic Models: https://docs.pydantic.dev/latest/concepts/models/

⚠️  IMPORTANT: When asking AI assistants for help, ALWAYS include the doc URL!
    Libraries like PydanticAI evolve over time, and AI models may have outdated
    information. Grounding your questions in current docs prevents bad answers.
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
# CONCEPT: When Do You Need This Full Pattern?
# =============================================================================
#
# The pattern in this exercise is powerful but adds complexity. Consider:
#
# ✅ USE THE FULL PATTERN WHEN:
#   - You need STRUCTURED extraction (the LLM fills out complex models)
#   - Multiple tools share runtime context (dependencies)
#   - You need to accumulate results across tool calls
#   - You're building a reusable, production agent
#   - You want type safety and validation on LLM outputs
#
# ❌ SIMPLER APPROACHES MIGHT BE BETTER WHEN:
#
#   1. Single extraction task - Just use structured output:
#      agent = Agent(model, output_type=MyModel)  # No tools needed!
#      result = agent.run_sync("Extract data from: ...")
#      data = result.output  # MyModel instance
#
#   2. Simple tool with few parameters - Skip Pydantic input models:
#      @agent.tool_plain
#      def add_numbers(a: int, b: int) -> int:
#          return a + b
#
#   3. No shared context - Skip dependencies:
#      @agent.tool_plain
#      def get_weather(city: str) -> str:
#          return fetch_weather(city)  # Tool doesn't need external context
#
#   4. One-off task - Skip agents entirely:
#      response = client.chat.completions.create(...)
#
# 💡 KEY INSIGHT: The full pattern is for when you need ALL the pieces
#    working together. Don't use it just because you can!
#
# =============================================================================


# =============================================================================
# CONCEPT: Pydantic Models as Tool Inputs - The Key Pattern!
# =============================================================================
#
# This is where Exercises 1 (Pydantic models) and 3 (tools) come together.
#
# In Exercise 3, your tools took simple arguments:
#   @agent.tool_plain
#   def roll_dice(sides: int = 6) -> str:
#       ...
#
# But tools can also take PYDANTIC MODELS as inputs:
#   @agent.tool
#   def create_summary(ctx: RunContext[Deps], input_data: MeetingSummary) -> str:
#       ...
#
# When the LLM calls this tool, it fills out ALL the model fields!
# The model's Field descriptions tell the LLM what to put in each field.
#
# This is POWERFUL because:
#   - Complex structured data from a single tool call
#   - Automatic validation via Pydantic
#   - Type safety in your code
#   - The LLM does the data extraction work
#
# 🤖 Ask your AI assistant:
#    "Read https://ai.pydantic.dev/tools/ and explain how Pydantic models
#     can be used as tool input parameters"
# =============================================================================


# =============================================================================
# PART 1: Define Pydantic Models for Tool Inputs
# =============================================================================

class ActionItem(BaseModel):
    """A single action item - used nested in TaskSummaryInput."""
    task: str = Field(description="The action item or task to be done")
    owner: str = Field(description="Person responsible for this task")
    priority: Literal["high", "medium", "low"] = Field(
        default="medium",
        description="Priority level of the task"
    )


class TaskSummaryInput(BaseModel):
    """Input model for the create_task_summary tool.

    When the LLM calls create_task_summary, it fills out this ENTIRE model
    based on the meeting transcript. The Field descriptions guide what
    the LLM extracts.
    """
    meeting_title: str = Field(
        description="Title of the meeting"
    )
    summary: str = Field(
        description="Brief 1-2 sentence summary of what was discussed"
    )
    action_items: list[ActionItem] = Field(
        description="Action items extracted from the meeting, with owners and priorities"
    )
    next_steps: list[str] = Field(
        default_factory=list,
        description="Recommended next steps after the meeting"
    )


# =============================================================================
# PART 2: Define Dependencies
# =============================================================================

@dataclass
class MeetingAgentDeps:
    """Dependencies for the meeting processing agent.

    This combines runtime context (dates) with mutable state (results).
    """
    # Runtime context - injected at call time
    current_date: str
    current_day: str
    one_week_from_now: str

    # Mutable state - accumulates during execution
    tool_results: list[dict[str, Any]] = field(default_factory=list)


def create_deps() -> MeetingAgentDeps:
    """Factory function to create deps with current date info."""
    now = datetime.now()
    return MeetingAgentDeps(
        current_date=now.strftime("%Y-%m-%d"),
        current_day=now.strftime("%A"),
        one_week_from_now=(now + timedelta(days=7)).strftime("%Y-%m-%d"),
        tool_results=[],
    )


# =============================================================================
# PART 3: Create the Agent
# =============================================================================

def create_meeting_agent() -> Agent[MeetingAgentDeps, str]:
    """Create a meeting processing agent.

    This demonstrates the full pattern:
    1. Static base instructions
    2. Dynamic instructions via @agent.instructions
    3. Tools with Pydantic model inputs
    4. Result accumulation in deps
    """
    model = TestModel()

    agent: Agent[MeetingAgentDeps, str] = Agent(
        model,
        deps_type=MeetingAgentDeps,
        instructions="""You are a meeting assistant that processes meeting transcripts.

Analyze the content and extract structured information using the appropriate tools.
After processing, provide a brief summary of what you extracted.""",
    )

    # Dynamic instructions - inject current date at runtime
    @agent.instructions
    def add_date_context(ctx: RunContext[MeetingAgentDeps]) -> str:
        """Inject date context into the system prompt."""
        return f"""
**Current Date Context:**
- Today: {ctx.deps.current_day}, {ctx.deps.current_date}
- One week from now: {ctx.deps.one_week_from_now}

Use this context when setting due dates for action items."""

    # Tool with Pydantic model input!
    @agent.tool
    async def create_task_summary(
        ctx: RunContext[MeetingAgentDeps],
        input_data: TaskSummaryInput  # The LLM fills this out!
    ) -> str:
        """Create a task summary from meeting content.

        Use this when the meeting contains:
        - Action items or tasks
        - Owners/assignees for tasks
        - Discussion that should be summarized

        Args:
            ctx: RunContext with dependencies
            input_data: Structured meeting summary (LLM fills this out)
        """
        print(f"\n[TOOL CALLED] create_task_summary")
        print(f"  Meeting: {input_data.meeting_title}")
        print(f"  Action items: {len(input_data.action_items)}")

        # Store result in deps for later retrieval
        result = {
            "tool": "create_task_summary",
            "status": "success",
            "data": input_data.model_dump(),
            "processed_at": ctx.deps.current_date,
        }
        ctx.deps.tool_results.append(result)

        return f"Created summary '{input_data.meeting_title}' with {len(input_data.action_items)} action items"

    return agent


# =============================================================================
# PART 4: Extract Tool Calls from Message History
# =============================================================================
#
# After running an agent, you often want to see what tools were called
# and what arguments were passed. This is essential for:
#
#   - Displaying tool activity in a UI
#   - Debugging agent behavior
#   - Logging for audit trails
#
# Tool calls live in the message history as ToolCallPart objects inside
# ModelResponse messages.
# =============================================================================

def extract_tool_calls(result: Any) -> list[dict[str, Any]]:
    """Extract tool calls from an agent result.

    This is a simplified version of what agent.py does.
    """
    tool_calls = []

    for message in result.all_messages():
        # Tool calls are in ModelResponse messages
        if isinstance(message, ModelResponse):
            for part in message.parts:
                # ToolCallPart contains the tool name and arguments
                if isinstance(part, ToolCallPart):
                    # Arguments might be a string (JSON) or already parsed
                    args = part.args
                    if isinstance(args, str):
                        args = json.loads(args)

                    tool_calls.append({
                        "tool_name": part.tool_name,
                        "arguments": args,
                    })

    return tool_calls


# =============================================================================
# DEMO: The Full Pattern in Action
# =============================================================================

def demo_full_pattern():
    """Demonstrate the complete pattern."""
    print("=" * 60)
    print("DEMO: Full Pattern - Meeting Processing Agent")
    print("=" * 60)

    # Create agent and deps
    agent = create_meeting_agent()
    deps = create_deps()

    print(f"\nDependencies created:")
    print(f"  Current date: {deps.current_date}")
    print(f"  Current day: {deps.current_day}")
    print(f"  One week from now: {deps.one_week_from_now}")

    # Sample meeting transcript
    meeting_transcript = """
    Sprint Planning Meeting - December 9, 2024

    Attendees: Alice, Bob, Charlie

    Discussion:
    - Reviewed Q4 roadmap progress
    - API redesign is on track for launch
    - Need to finalize testing strategy before release

    Action Items:
    - Alice: Complete API documentation by Friday (high priority)
    - Bob: Set up integration test environment (medium priority)
    - Charlie: Review security audit findings (high priority)

    Next Steps:
    - Schedule follow-up for test results review
    - Prepare demo for stakeholders
    """

    print(f"\nProcessing meeting transcript ({len(meeting_transcript)} chars)...")

    # Run the agent
    import asyncio

    async def run():
        return await agent.run(
            f"Process this meeting transcript:\n\n{meeting_transcript}",
            deps=deps,
        )

    result = asyncio.run(run())

    # Show results
    print("\n" + "-" * 60)
    print("RESULTS")
    print("-" * 60)

    print(f"\nAgent output: {result.output}")

    print(f"\nTool results accumulated in deps ({len(deps.tool_results)}):")
    for tr in deps.tool_results:
        print(f"  Tool: {tr['tool']}")
        print(f"  Status: {tr['status']}")
        data = tr['data']
        print(f"  Meeting: {data['meeting_title']}")
        print(f"  Actions: {len(data['action_items'])} items")

    # Extract tool calls from message history
    tool_calls = extract_tool_calls(result)
    print(f"\nTool calls extracted from messages ({len(tool_calls)}):")
    for tc in tool_calls:
        print(f"  {tc['tool_name']}: {list(tc['arguments'].keys())}")


if __name__ == "__main__":
    demo_full_pattern()

    print("\n" + "=" * 60)
    print("DEMO COMPLETE - Now try the exercises below!")
    print("=" * 60)


# =============================================================================
# =============================================================================
#
#   YOUR TURN: EXERCISES
#
# =============================================================================
# =============================================================================


# =============================================================================
# EXERCISE 1: Add a second tool with a different input model
# =============================================================================
#
# Create an UrgentIssueInput model and a corresponding tool for reporting
# urgent issues found in meetings.
#
# STEP 1: Define the input model
#
#   class UrgentIssueInput(BaseModel):
#       """Input for reporting urgent issues."""
#       issue_title: str = Field(description="_____")
#       severity: Literal["critical", "high", "medium"] = Field(
#           description="_____"
#       )
#       affected_systems: list[str] = Field(
#           description="_____"
#       )
#       immediate_actions: list[str] = Field(
#           description="_____"
#       )
#
# STEP 2: Add the tool to the agent
#
#   @agent.tool
#   async def report_urgent_issue(
#       ctx: RunContext[MeetingAgentDeps],
#       input_data: UrgentIssueInput
#   ) -> str:
#       """Report an urgent issue from a meeting.
#
#       Use this when the meeting discusses:
#       - Production incidents
#       - Security vulnerabilities
#       - Critical bugs
#       """
#       # Store in deps.tool_results
#       # Return a confirmation message
#       pass
#
# STEP 3: Test with an incident-focused meeting transcript
#
# 💡 HINTS:
#   - Look at TaskSummaryInput as a template
#   - Field descriptions should guide the LLM on what to extract
#   - Store results in ctx.deps.tool_results like create_task_summary does
#
# 🤖 Stuck? Ask your AI assistant:
#   - "Read https://ai.pydantic.dev/tools/ and show me how to create
#      a tool that takes a Pydantic model with nested lists"
# =============================================================================


# =============================================================================
# EXERCISE 2: Think about when to use Pydantic model inputs (thought exercise)
# =============================================================================
#
# Not every tool needs a Pydantic model input. Consider these scenarios:
#
# SCENARIO A: Calculator tool
#
#   Option 1 - Pydantic model:
#     class CalculatorInput(BaseModel):
#         operation: Literal["add", "subtract", "multiply", "divide"]
#         a: float
#         b: float
#
#   Option 2 - Simple parameters:
#     def calculate(operation: str, a: float, b: float) -> float:
#
#   Q: Which would you choose? Why?
#   A: _____
#
#
# SCENARIO B: Meeting summary with 10+ fields
#
#   The tool needs: title, attendees, date, duration, summary, decisions,
#   action_items, blockers, risks, next_meeting_date...
#
#   Q: Pydantic model or simple parameters?
#   A: _____
#
#
# SCENARIO C: Search tool
#
#   The tool takes a search query and optional filters.
#
#   Option 1: def search(query: str, max_results: int = 10)
#   Option 2: def search(input: SearchInput)
#
#   Q: When would you prefer each?
#   A: _____
#
# 💡 RULE OF THUMB:
#   - 1-3 parameters → Simple is fine
#   - 4+ parameters → Consider a Pydantic model
#   - Nested data (lists of objects) → Definitely use a model
#   - Need validation → Use a model
#
# =============================================================================


# =============================================================================
# EXERCISE 3: Build a mini transcript processor
# =============================================================================
#
# Create a complete process_transcript() function that mirrors what the
# main agent.py does. This is the capstone of all 5 exercises!
#
# STEP 1: Define the function signature
#
#   async def process_transcript(text: str) -> dict[str, Any]:
#       """Process a transcript and return structured results.
#
#       Returns:
#           {
#               "success": True/False,
#               "tool_calls": [...],  # What tools were called
#               "results": [...],     # Accumulated tool results
#               "summary": "...",     # Agent's output
#           }
#       """
#
# STEP 2: Implement it
#
#   async def process_transcript(text: str) -> dict[str, Any]:
#       agent = create_meeting_agent()  # Create agent
#       deps = create_deps()            # Create fresh deps
#
#       result = await agent.run(       # Run the agent
#           f"Process this:\n\n{text}",
#           deps=deps,
#       )
#
#       tool_calls = extract_tool_calls(result)  # Extract calls
#
#       return {
#           "success": True,
#           "tool_calls": tool_calls,
#           "results": deps.tool_results,  # From accumulation!
#           "summary": result.output,
#       }
#
# STEP 3: Test with different transcript types
#
#   import asyncio
#
#   # Sprint planning transcript
#   result1 = asyncio.run(process_transcript("Sprint planning meeting..."))
#
#   # Incident response transcript
#   result2 = asyncio.run(process_transcript("Incident: Database outage..."))
#
#   print(result1)
#   print(result2)
#
# 💡 THIS IS IT!
#   You've just built the core of an AI transcript processing system.
#   The main agent.py in this project uses this exact pattern.
#
# 🤖 When you're done, ask your AI assistant:
#   - "Review my transcript processor - does it follow the patterns from
#      https://ai.pydantic.dev/agents/ and https://ai.pydantic.dev/tools/ ?"
# =============================================================================


# =============================================================================
# EXERCISE 4: Extract tool return values from messages
# =============================================================================
#
# The extract_tool_calls function only gets the tool CALLS. But the message
# history also contains the RETURN VALUES (what the tool sent back).
#
# STEP 1: Import ToolReturnPart
#
#   from pydantic_ai.messages import ModelResponse, ToolCallPart, ToolReturnPart
#
# STEP 2: Enhance the extraction function
#
#   def extract_tool_calls_with_returns(result: Any) -> list[dict]:
#       """Extract tool calls AND their return values."""
#       calls = []
#       returns = {}  # Map tool_call_id -> return value
#
#       for message in result.all_messages():
#           if isinstance(message, ModelResponse):
#               for part in message.parts:
#                   if isinstance(part, ToolCallPart):
#                       # ... extract call info ...
#                       # Remember: part.tool_call_id links calls to returns
#                       pass
#
#           # ToolReturnPart is in ModelRequest messages (sent back to LLM)
#           if hasattr(message, 'parts'):
#               for part in message.parts:
#                   if isinstance(part, ToolReturnPart):
#                       # part.tool_call_id and part.content
#                       returns[part.tool_call_id] = part.content
#
#       # Match returns to calls
#       for call in calls:
#           call['return_value'] = returns.get(call.get('tool_call_id'))
#
#       return calls
#
# STEP 3: Test it and see the return values
#
# 💡 HINTS:
#   - ToolCallPart has tool_call_id, tool_name, args
#   - ToolReturnPart has tool_call_id, content
#   - Match them by tool_call_id
#
# 🤖 Stuck? Ask your AI assistant:
#   - "Read https://ai.pydantic.dev/results/ and explain how ToolCallPart
#      and ToolReturnPart are connected via tool_call_id"
# =============================================================================


# =============================================================================
# BONUS: Compare approaches (hands-on exercise)
# =============================================================================
#
# Implement the SAME functionality two ways and compare:
#
# APPROACH 1: Full pattern (what we built)
#   - Agent with tools
#   - Pydantic model inputs
#   - Dependencies
#   - Result extraction
#
# APPROACH 2: Structured output only (simpler)
#   - Agent with output_type=TaskSummaryInput
#   - No tools, just direct structured output
#
#   agent = Agent(
#       model,
#       output_type=TaskSummaryInput,  # Agent returns this directly!
#       instructions="Extract meeting information..."
#   )
#   result = agent.run_sync("Process this: ...")
#   data = result.output  # TaskSummaryInput instance
#
# Questions to explore:
#   Q1: Which is simpler to implement?
#   Q2: Which gives you more control?
#   Q3: When would you need tools vs just structured output?
#   Q4: What can tools do that structured output can't?
#       (Hint: think about ACTIONS, not just extraction)
#
# 🤖 Ask your AI assistant:
#   - "Read https://ai.pydantic.dev/results/#structured-result-validation
#      and explain when to use output_type vs tool inputs"
# =============================================================================


# =============================================================================
# 🎉 CONGRATULATIONS!
# =============================================================================
#
# You've completed all 5 exercises and understand the full PydanticAI pattern:
#
#   Exercise 1: Pydantic models with Field descriptions
#   Exercise 2: Creating and running agents
#   Exercise 3: Adding tools with @agent.tool_plain
#   Exercise 4: Dependency injection with RunContext
#   Exercise 5: Pydantic models as tool inputs + result extraction
#
# You now have the knowledge to:
#   ✓ Build AI agents that can call tools
#   ✓ Define structured inputs the LLM fills out
#   ✓ Inject runtime context via dependencies
#   ✓ Accumulate results across tool calls
#   ✓ Extract tool activity for display
#   ✓ Choose when to use these patterns vs simpler approaches
#
# Next steps:
#   - Study agent.py in this project
#   - Try connecting to a real LLM (OpenAI, Anthropic, etc.)
#   - Build your own agent for a different use case!
#
# 📚 Full documentation: https://ai.pydantic.dev/
# =============================================================================
