"""
Exercise 4: Dependency Injection with RunContext
================================================

In this exercise, you'll learn how to pass runtime data to your agent's tools
using dependency injection. By the end, you'll understand:

- What dependencies are and why you need them
- How to define a deps dataclass
- How to access deps via RunContext in tools
- How to use @agent.tool (vs @agent.tool_plain)
- How tools can modify dependencies (accumulating results)

Difficulty: Intermediate
Time: ~45 minutes

Run: uv run python exercises/04_dependencies_v2.py

📚 DOCUMENTATION LINKS (bookmark these!):
- PydanticAI Dependencies: https://ai.pydantic.dev/dependencies/
- Tools with Context: https://ai.pydantic.dev/tools/

⚠️  IMPORTANT: When asking AI assistants for help, ALWAYS include the doc URL!
    Libraries like PydanticAI evolve over time, and AI models may have outdated
    information. Grounding your questions in current docs prevents bad answers.
"""

from dataclasses import dataclass, field

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.test import TestModel

# =============================================================================
# CONCEPT: What are Dependencies and why do you need them?
# =============================================================================
#
# In Exercise 3, your tools were standalone - they didn't need any external
# data. But real apps often need tools that:
#
#   - Know who the current user is
#   - Have access to a database connection
#   - Know today's date
#   - Can accumulate results across multiple tool calls
#
# This runtime data is called DEPENDENCIES. PydanticAI uses dependency
# injection to pass this data to your tools cleanly.
#
# Example: An agent that greets users by name
#   - The USER NAME is a dependency (it changes per request)
#   - The tool needs to access it somehow
#
# 🤖 Ask your AI assistant:
#    "Read https://ai.pydantic.dev/dependencies/ and explain why dependency
#     injection is useful for AI agents"
# =============================================================================


# =============================================================================
# CONCEPT: Defining Dependencies with @dataclass
# =============================================================================
#
# Dependencies are typically defined as a dataclass - a simple Python class
# that holds data. The @dataclass decorator auto-generates __init__, etc.
#
#   from dataclasses import dataclass
#
#   @dataclass
#   class MyDeps:
#       user_name: str
#       user_id: int
#       is_premium: bool = False
#
# When you create an instance: deps = MyDeps(user_name="Alice", user_id=123)
#
# 📚 Python dataclasses: https://docs.python.org/3/library/dataclasses.html
# =============================================================================


# =============================================================================
# CONCEPT: @agent.tool vs @agent.tool_plain
# =============================================================================
#
# Remember from Exercise 3:
#   @agent.tool_plain → Tools that DON'T need dependencies
#   @agent.tool       → Tools that DO need dependencies
#
# The difference is the first parameter:
#
#   @agent.tool_plain
#   def simple_tool(arg1: str) -> str:    # No ctx parameter
#       return "result"
#
#   @agent.tool
#   def context_tool(ctx: RunContext[MyDeps], arg1: str) -> str:
#       name = ctx.deps.user_name         # Access deps via ctx.deps
#       return f"Hello {name}"
#
# RunContext[MyDeps] is typed! Your IDE knows ctx.deps is a MyDeps instance.
#
# 📚 Docs: https://ai.pydantic.dev/tools/#tools-vs-plain-tools
# =============================================================================


# =============================================================================
# WORKING EXAMPLE: Personalized Greeting Agent
# =============================================================================

@dataclass
class UserContext:
    """Dependencies for a personalized agent.

    This data is passed at runtime when you call agent.run_sync().
    """
    user_name: str
    preferred_greeting: str = "Hello"


def create_personalized_agent() -> Agent[UserContext, str]:
    """Create an agent that personalizes responses based on user context.

    Note the type hint: Agent[UserContext, str]
      - UserContext = the type of dependencies this agent expects
      - str = the return type (plain text)
    """
    model = TestModel()

    agent: Agent[UserContext, str] = Agent(
        model,
        deps_type=UserContext,  # Tell the agent what deps type to expect
        instructions="You are a personal assistant. Be helpful and friendly.",
    )

    # This tool needs to access user_name, so we use @agent.tool (not tool_plain)
    @agent.tool
    def greet_user(ctx: RunContext[UserContext]) -> str:
        """Generate a personalized greeting.

        The ctx parameter gives us access to the dependencies.
        """
        # Access dependencies via ctx.deps
        return f"{ctx.deps.preferred_greeting}, {ctx.deps.user_name}!"

    @agent.tool
    def get_user_info(ctx: RunContext[UserContext]) -> str:
        """Get information about the current user."""
        return f"Current user: {ctx.deps.user_name}"

    return agent


def demo_basic_deps():
    """Demonstrate passing dependencies when running an agent."""
    print("=" * 60)
    print("DEMO: Basic Dependency Injection")
    print("=" * 60)

    agent = create_personalized_agent()

    # Create dependencies for THIS specific run
    deps = UserContext(user_name="Alice", preferred_greeting="Welcome")

    # Pass deps when running the agent
    result = agent.run_sync("Greet me!", deps=deps)

    print(f"\nDeps: user_name={deps.user_name}, greeting={deps.preferred_greeting}")
    print(f"Output: {result.output}")


def demo_different_users():
    """Show how different deps create different behavior."""
    print("\n" + "=" * 60)
    print("DEMO: Same Agent, Different Users")
    print("=" * 60)

    agent = create_personalized_agent()

    # Same agent, different dependencies = different behavior!
    users = [
        UserContext(user_name="Alice", preferred_greeting="Hello"),
        UserContext(user_name="Bob", preferred_greeting="Hey"),
        UserContext(user_name="Charlie", preferred_greeting="Greetings"),
    ]

    for user_deps in users:
        result = agent.run_sync("Greet me!", deps=user_deps)
        print(f"\n{user_deps.user_name}: {result.output}")


# =============================================================================
# CONCEPT: Mutable Dependencies (Accumulating Results)
# =============================================================================
#
# Dependencies can be MUTABLE - tools can modify them! This is powerful for:
#
#   - Tracking how many times a tool was called
#   - Accumulating results from multiple tool calls
#   - Building up state during a conversation
#
# This is exactly how the main agent.py collects tool results for display.
#
#   @dataclass
#   class TrackingDeps:
#       results: list[str] = field(default_factory=list)  # Mutable!
#
#   @agent.tool
#   def do_something(ctx: RunContext[TrackingDeps]) -> str:
#       result = "Did the thing"
#       ctx.deps.results.append(result)  # Modify deps!
#       return result
#
# 📚 Note: field(default_factory=list) creates a NEW list for each instance
# =============================================================================


@dataclass
class MutableDeps:
    """Dependencies with mutable state."""
    call_count: int = 0
    results: list[str] = field(default_factory=list)


def create_tracking_agent() -> Agent[MutableDeps, str]:
    """Create an agent that tracks its own activity."""
    model = TestModel()

    agent: Agent[MutableDeps, str] = Agent(
        model,
        deps_type=MutableDeps,
        instructions="You are a helpful assistant.",
    )

    @agent.tool
    def do_task(ctx: RunContext[MutableDeps], task_name: str) -> str:
        """Perform a task and track it.

        This demonstrates how tools can modify dependencies.
        """
        ctx.deps.call_count += 1
        result = f"Completed: {task_name} (call #{ctx.deps.call_count})"
        ctx.deps.results.append(result)
        return result

    return agent


def demo_mutable_deps():
    """Show how tools can modify dependencies."""
    print("\n" + "=" * 60)
    print("DEMO: Mutable Dependencies (Accumulating Results)")
    print("=" * 60)

    agent = create_tracking_agent()
    deps = MutableDeps()

    print(f"Before: call_count={deps.call_count}, results={deps.results}")

    # Run multiple times with the SAME deps object
    agent.run_sync("Do task A", deps=deps)
    agent.run_sync("Do task B", deps=deps)
    agent.run_sync("Do task C", deps=deps)

    print(f"After: call_count={deps.call_count}")
    print(f"Results accumulated: {deps.results}")


# =============================================================================
# CONCEPT: When to Use Dependencies vs Simpler Approaches
# =============================================================================
#
# Dependencies are powerful but add complexity. Consider alternatives:
#
# ✅ USE DEPENDENCIES WHEN:
#   - Multiple tools need the same context (user info, db connection)
#   - You need to accumulate results across tool calls
#   - You want type-safe access to runtime data
#   - You're building reusable agents
#
# ❌ SIMPLER ALTERNATIVES:
#
#   1. Just include info in the prompt:
#      agent.run_sync(f"User {user_name} asks: {question}")
#
#   2. Use closure variables:
#      user_name = "Alice"
#      @agent.tool_plain
#      def greet():
#          return f"Hello {user_name}"  # Captures variable from outer scope
#
#   3. Return results normally and collect them yourself:
#      result = agent.run_sync("...")
#      collected_results.append(result.output)
#
# Dependencies shine when you have:
#   - Complex runtime context
#   - Multiple tools sharing state
#   - Need for type safety
#
# =============================================================================


if __name__ == "__main__":
    demo_basic_deps()
    demo_different_users()
    demo_mutable_deps()

    print("\n" + "=" * 60)
    print("DEMOS COMPLETE - Now try the exercises below!")
    print("=" * 60)


# =============================================================================
# =============================================================================
#
#   YOUR TURN: EXERCISES
#
# =============================================================================
# =============================================================================


# =============================================================================
# EXERCISE 1: Add dynamic instructions with @agent.instructions
# =============================================================================
#
# You can inject dynamic content into the system prompt using dependencies!
# The @agent.instructions decorator marks a function that returns extra
# instructions based on the current deps.
#
# This is how the main agent.py injects today's date into the prompt.
#
# STEP 1: Create deps with context you want to inject
#
#   @dataclass
#   class DateContext:
#       current_date: str
#       user_name: str
#
# STEP 2: Create an agent with dynamic instructions
#
#   def create_date_aware_agent() -> Agent[DateContext, str]:
#       model = TestModel()
#
#       agent: Agent[DateContext, str] = Agent(
#           model,
#           deps_type=DateContext,
#           instructions="You are a scheduling assistant.",
#       )
#
#       # This function adds to the system prompt at runtime!
#       @agent.instructions
#       def add_date_context(ctx: RunContext[DateContext]) -> str:
#           """Return additional instructions based on deps."""
#           return f"""
#           **Current Context:**
#           - Today's date: {ctx.deps.current_date}
#           - User: {ctx.deps.user_name}
#           Always consider the current date when scheduling.
#           """
#
#       return agent
#
# STEP 3: Test it with different dates
#
#   deps1 = DateContext(current_date="2024-12-09", user_name="Alice")
#   deps2 = DateContext(current_date="2024-12-25", user_name="Bob")
#   # The agent's behavior changes based on the date!
#
# 💡 HINTS:
#   - @agent.instructions functions return a string
#   - That string is added to the system prompt
#   - It's called fresh for each run with current deps
#
# 🤖 Stuck? Ask your AI assistant:
#   - "Read https://ai.pydantic.dev/agents/ and explain how to use
#      @agent.instructions for dynamic system prompts"
# =============================================================================


# =============================================================================
# EXERCISE 2: Accumulate rich results in deps
# =============================================================================
#
# Build on the mutable deps concept to accumulate STRUCTURED results.
# This is exactly what agent.py does to collect tool results for the frontend.
#
# STEP 1: Define deps with a list of dicts
#
#   from typing import Any
#   from datetime import datetime
#
#   @dataclass
#   class RichDeps:
#       tool_results: list[dict[str, Any]] = field(default_factory=list)
#
# STEP 2: Create a tool that stores rich results
#
#   @agent.tool
#   def process_item(ctx: RunContext[RichDeps], item: str) -> str:
#       """Process an item and store detailed results."""
#       result = {
#           "item": item,
#           "status": "processed",
#           "timestamp": datetime.now().isoformat(),
#           "metadata": {
#               "length": len(item),
#               "words": len(item.split()),
#           }
#       }
#       ctx.deps.tool_results.append(result)  # Accumulate!
#       return f"Processed: {item}"
#
# STEP 3: Run the agent and examine accumulated results
#
#   deps = RichDeps()
#   agent.run_sync("Process hello world", deps=deps)
#   agent.run_sync("Process foo bar baz", deps=deps)
#   print(deps.tool_results)  # Should have 2 detailed results!
#
# 💡 WHY THIS MATTERS:
#   The main app uses this exact pattern to collect all tool outputs
#   and send them to the frontend for display.
#
# 🤖 Stuck? Ask your AI assistant:
#   - "Show me how to accumulate structured results from multiple tool
#      calls using PydanticAI dependencies"
# =============================================================================


# =============================================================================
# EXERCISE 3: Create a mini "database" in deps
# =============================================================================
#
# Dependencies can hold anything - including a simulated database!
# This pattern lets you inject external services into your agent.
#
# STEP 1: Create deps with a "database"
#
#   @dataclass
#   class DatabaseDeps:
#       users_db: dict[str, dict] = field(default_factory=dict)
#
#   # Pre-populate with data
#   deps = DatabaseDeps(
#       users_db={
#           "alice": {"name": "Alice Smith", "role": "admin"},
#           "bob": {"name": "Bob Jones", "role": "user"},
#       }
#   )
#
# STEP 2: Create tools to query the database
#
#   @agent.tool
#   def get_user(ctx: RunContext[DatabaseDeps], username: str) -> str:
#       """Look up a user in the database."""
#       user = ctx.deps.users_db.get(username)
#       if user:
#           return f"Found: {user['name']} ({user['role']})"
#       return f"User '{username}' not found"
#
#   @agent.tool
#   def create_user(
#       ctx: RunContext[DatabaseDeps],
#       username: str,
#       name: str,
#       role: str = "user"
#   ) -> str:
#       """Create a new user in the database."""
#       if username in ctx.deps.users_db:
#           return f"Error: User '{username}' already exists"
#       ctx.deps.users_db[username] = {"name": name, "role": role}
#       return f"Created user: {username}"
#
# STEP 3: Test querying and creating users
#
#   result = agent.run_sync("Look up user alice", deps=deps)
#   result = agent.run_sync("Create user charlie with name Charlie Brown", deps=deps)
#   print(deps.users_db)  # Should now have charlie!
#
# 💡 WHY THIS MATTERS:
#   In real apps, deps would hold actual database connections, API clients,
#   or other external services. The pattern is the same!
#
# 🤖 Stuck? Ask your AI assistant:
#   - "Read https://ai.pydantic.dev/dependencies/ and show me how to
#      inject external services like databases into agent tools"
# =============================================================================


# =============================================================================
# EXERCISE 4: Think about dependency design (thought exercise)
# =============================================================================
#
# Not everything should be a dependency. Consider these scenarios:
#
# SCENARIO A: API key for external service
#
#   Option 1 - In deps:
#     @dataclass
#     class Deps:
#         openai_api_key: str
#
#   Option 2 - Environment variable:
#     import os
#     api_key = os.environ["OPENAI_API_KEY"]
#
#   Q: Which is better for a secret? Why?
#   A: _____
#
#
# SCENARIO B: Current timestamp
#
#   Option 1 - In deps:
#     @dataclass
#     class Deps:
#         current_time: datetime
#
#   Option 2 - Compute in tool:
#     @agent.tool_plain
#     def get_time():
#         return datetime.now()
#
#   Q: What's the tradeoff?
#   A: _____  (Hint: testing vs freshness)
#
#
# SCENARIO C: User session data
#
#   You have: user_id, user_name, is_premium, last_login, preferences
#   Multiple tools need: user_id, user_name
#   One tool needs: is_premium
#   No tools need: last_login, preferences
#
#   Q: What should go in deps? What shouldn't?
#   A: _____
#
# 💡 KEY INSIGHT:
#   Put data in deps if:
#   - Multiple tools need it
#   - It changes per request
#   - You want type safety
#
#   Keep data out of deps if:
#   - It's a secret (use env vars)
#   - Only one tool needs it (use closure or parameter)
#   - It doesn't change (use constants)
#
# =============================================================================


# =============================================================================
# BONUS CHALLENGE: Combine everything from Exercises 1-4
# =============================================================================
#
# Create an agent that:
#   1. Uses a Pydantic model for structured tool input (Exercise 1)
#   2. Has multiple tools (Exercise 3)
#   3. Uses deps for user context AND result accumulation (Exercise 4)
#   4. Has dynamic instructions with the current date
#
# This is essentially what you'll build in Exercise 5!
#
# Suggested structure:
#
#   @dataclass
#   class FullDeps:
#       user_name: str
#       current_date: str
#       tool_results: list[dict] = field(default_factory=list)
#
#   # Multiple tools that access deps and accumulate results...
#
# 🤖 When you're done, ask your AI assistant:
#   - "Review my PydanticAI agent setup - does it follow best practices from
#      https://ai.pydantic.dev/dependencies/ ?"
# =============================================================================
