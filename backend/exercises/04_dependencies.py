"""
Exercise 4: Dependency Injection with RunContext

Concept: Dependencies let you pass runtime data to tools and instructions.
Use @dataclass for deps, access them via ctx.deps in @agent.tool functions.
This is how the main agent.py injects date context and accumulates results.

Difficulty: Intermediate

Run: uv run python exercises/04_dependencies.py
"""

from dataclasses import dataclass, field

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.test import TestModel

# =============================================================================
# WORKING BASE CODE
# =============================================================================


@dataclass
class UserContext:
    """Dependencies injected into the agent.

    This mirrors AgentDeps in models.py. Dependencies can include:
    - User information (name, preferences)
    - Runtime context (current date, session ID)
    - Mutable state (accumulated results, counters)
    - External services (database connections, API clients)
    """

    user_name: str
    preferred_greeting: str = "Hello"


def create_personalized_agent() -> Agent[UserContext, str]:
    """Create an agent that uses dependencies for personalization.

    Key differences from @agent.tool_plain:
    - @agent.tool receives ctx: RunContext[DepsType] as first parameter
    - Access deps via ctx.deps.field_name
    - Must specify deps_type in Agent constructor
    """
    model = TestModel()

    agent: Agent[UserContext, str] = Agent(
        model,
        deps_type=UserContext,  # Tell agent what type of deps to expect
        instructions="You are a personal assistant. Be helpful and friendly.",
    )

    @agent.tool
    def get_user_name(ctx: RunContext[UserContext]) -> str:
        """Get the current user's name.

        Note: @agent.tool (not @agent.tool_plain) because we need RunContext.
        """
        return f"The user's name is {ctx.deps.user_name}"

    @agent.tool
    def greet_user(ctx: RunContext[UserContext]) -> str:
        """Generate a personalized greeting for the user."""
        return f"{ctx.deps.preferred_greeting}, {ctx.deps.user_name}!"

    return agent


def demo_basic_deps():
    """Demonstrate basic dependency injection."""
    print("=" * 60)
    print("DEMO: Basic Dependency Injection")
    print("=" * 60)

    agent = create_personalized_agent()

    # Create dependencies for this run
    deps = UserContext(user_name="Alice", preferred_greeting="Welcome")

    # Pass deps when running the agent
    result = agent.run_sync("Greet me!", deps=deps)

    print(f"\nDeps: {deps}")
    print("Prompt: 'Greet me!'")
    print(f"Output: {result.output}")


def demo_different_deps():
    """Show how different deps change behavior."""
    print("\n" + "=" * 60)
    print("DEMO: Different Deps = Different Behavior")
    print("=" * 60)

    agent = create_personalized_agent()

    users = [
        UserContext(user_name="Alice", preferred_greeting="Hello"),
        UserContext(user_name="Bob", preferred_greeting="Hey"),
        UserContext(user_name="Charlie", preferred_greeting="Greetings"),
    ]

    for user in users:
        result = agent.run_sync("Greet me!", deps=user)
        print(f"\n{user.user_name}: {result.output}")


@dataclass
class MutableDeps:
    """Dependencies with mutable state (like AgentDeps.tool_results)."""

    call_count: int = 0
    results: list[str] = field(default_factory=list)


def create_tracking_agent() -> Agent[MutableDeps, str]:
    """Create an agent that tracks tool calls in dependencies."""
    model = TestModel()

    agent: Agent[MutableDeps, str] = Agent(
        model,
        deps_type=MutableDeps,
        instructions="You are a helpful assistant.",
    )

    @agent.tool
    def do_something(ctx: RunContext[MutableDeps], action: str) -> str:
        """Perform an action and track it in deps.

        This pattern is used in agent.py to accumulate tool results:
        ctx.deps.tool_results.append(result)
        """
        ctx.deps.call_count += 1
        result = f"Did: {action} (call #{ctx.deps.call_count})"
        ctx.deps.results.append(result)
        return result

    return agent


def demo_mutable_deps():
    """Show how tools can modify dependencies."""
    print("\n" + "=" * 60)
    print("DEMO: Mutable Dependencies")
    print("=" * 60)

    agent = create_tracking_agent()
    deps = MutableDeps()

    print(f"Before: call_count={deps.call_count}, results={deps.results}")

    # Run the agent multiple times with same deps
    agent.run_sync("Do task 1", deps=deps)
    agent.run_sync("Do task 2", deps=deps)
    agent.run_sync("Do task 3", deps=deps)

    print(f"After: call_count={deps.call_count}, results={deps.results}")


if __name__ == "__main__":
    demo_basic_deps()
    demo_different_deps()
    demo_mutable_deps()

    print("\n" + "=" * 60)
    print("BASE CODE COMPLETE - Try the challenges below!")
    print("=" * 60)


# =============================================================================
# CHALLENGES
# =============================================================================

# -----------------------------------------------------------------------------
# Challenge 1: Add @agent.instructions that uses deps dynamically
# -----------------------------------------------------------------------------
# Use the @agent.instructions decorator to add dynamic instructions based on deps.
# This is how agent.py injects the current date into the system prompt.
#
# Example:
#   @agent.instructions
#   def add_user_context(ctx: RunContext[UserContext]) -> str:
#       """Inject user info into the system prompt."""
#       return f"The user's name is {ctx.deps.user_name}. Address them by name."
#
# This function is called for each run and its return value is added to instructions.

# -----------------------------------------------------------------------------
# Challenge 2: Create a tool that modifies deps (accumulate results)
# -----------------------------------------------------------------------------
# Extend the tracking agent to accumulate richer results:
#
#   @dataclass
#   class RichDeps:
#       tool_results: list[dict[str, Any]] = field(default_factory=list)
#
#   @agent.tool
#   def process_item(ctx: RunContext[RichDeps], item: str) -> str:
#       result = {
#           "item": item,
#           "status": "processed",
#           "timestamp": datetime.now().isoformat(),
#       }
#       ctx.deps.tool_results.append(result)
#       return f"Processed: {item}"
#
# After running, deps.tool_results contains all the rich results.
# This is exactly how agent.py collects tool outputs for the frontend.

# -----------------------------------------------------------------------------
# Challenge 3: Add a database-like dependency and query it
# -----------------------------------------------------------------------------
# Create deps with a "database" (dict) and tools to query it:
#
#   @dataclass
#   class DatabaseDeps:
#       users_db: dict[str, dict[str, Any]] = field(default_factory=dict)
#
#   # Pre-populate with some data
#   deps = DatabaseDeps(
#       users_db={
#           "alice": {"name": "Alice", "role": "admin"},
#           "bob": {"name": "Bob", "role": "user"},
#       }
#   )
#
#   @agent.tool
#   def get_user(ctx: RunContext[DatabaseDeps], username: str) -> str:
#       user = ctx.deps.users_db.get(username)
#       if user:
#           return f"Found user: {user}"
#       return f"User '{username}' not found"
#
# This pattern lets you inject any external service (real databases, APIs, etc.)
