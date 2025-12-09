"""
Exercise 2: Creating and Running a Basic PydanticAI Agent

Concept: Learn to create an Agent with instructions, run it with prompts,
and access the result. No tools yet - just basic agent conversation.

Difficulty: Beginner

Run: uv run python exercises/02_basic_agent.py
"""

from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel

# =============================================================================
# WORKING BASE CODE
# =============================================================================


def create_greeting_agent() -> Agent[None, str]:
    """Create a simple agent that greets users.

    The Agent class is the core of PydanticAI. Key parameters:
    - model: The LLM to use (TestModel for exercises, real model in production)
    - instructions: System prompt that shapes agent behavior
    - deps_type: Type of dependencies (None here, more in Exercise 4)
    - output_type: Return type (str here, Pydantic model for structured output)
    """
    # TestModel is a mock - no API calls, instant results, perfect for learning
    model = TestModel()

    agent: Agent[None, str] = Agent(
        model,
        instructions=(
            "You are a friendly assistant. "
            "Greet users warmly and offer to help with their tasks."
        ),
    )

    return agent


def demo_basic_run():
    """Demonstrate running an agent and accessing results."""
    print("=" * 60)
    print("DEMO: Basic Agent Run")
    print("=" * 60)

    agent = create_greeting_agent()

    # run_sync() is the synchronous way to run an agent
    # (There's also await agent.run() for async code)
    result = agent.run_sync("Hello!")

    print("\nPrompt: 'Hello!'")
    print(f"Output: {result.output}")

    # The result object contains more than just output
    print(f"\nResult type: {type(result)}")
    print(f"Output type: {type(result.output)}")


def demo_multiple_prompts():
    """Show that each run is independent (no conversation memory by default)."""
    print("\n" + "=" * 60)
    print("DEMO: Multiple Independent Runs")
    print("=" * 60)

    agent = create_greeting_agent()

    prompts = [
        "Hi there!",
        "What can you help me with?",
        "Thanks!",
    ]

    for prompt in prompts:
        result = agent.run_sync(prompt)
        print(f"\nPrompt: '{prompt}'")
        print(f"Output: {result.output}")


def demo_custom_test_response():
    """Show how TestModel can return custom responses for testing."""
    print("\n" + "=" * 60)
    print("DEMO: Custom Test Responses")
    print("=" * 60)

    # TestModel can be configured to return specific responses
    # This is useful for testing specific scenarios
    model = TestModel(custom_output_text="Welcome to PydanticAI exercises!")

    agent: Agent[None, str] = Agent(
        model,
        instructions="You are a tutorial guide.",
    )

    result = agent.run_sync("Start the tutorial")
    print("\nWith custom_output_text:")
    print(f"Output: {result.output}")


if __name__ == "__main__":
    demo_basic_run()
    demo_multiple_prompts()
    demo_custom_test_response()

    print("\n" + "=" * 60)
    print("BASE CODE COMPLETE - Try the challenges below!")
    print("=" * 60)


# =============================================================================
# CHALLENGES
# =============================================================================

# -----------------------------------------------------------------------------
# Challenge 1: Change instructions to create a different personality
# -----------------------------------------------------------------------------
# Create an agent with instructions that make it:
# - Act as a pirate who speaks in pirate slang
# - Or a formal butler
# - Or a enthusiastic sports commentator
#
# Run it with the same prompts and see how the personality changes.
#
# Hint: The instructions parameter is just a string - be creative!
#
# Example:
#   pirate_agent = Agent(
#       TestModel(),
#       instructions="You are a pirate. Speak in pirate slang, use 'Arrr!' and nautical terms.",
#   )

# -----------------------------------------------------------------------------
# Challenge 2: Add output_type to get structured output
# -----------------------------------------------------------------------------
# Create an agent that returns structured data instead of plain text.
# Define a Pydantic model for the output and set output_type on the Agent.
#
# Hint: Import BaseModel from pydantic and create a model like:
#
#   class GreetingResponse(BaseModel):
#       greeting: str
#       mood: Literal["happy", "neutral", "excited"]
#       suggested_topics: list[str]
#
#   agent = Agent(
#       TestModel(),
#       instructions="Generate structured greetings",
#       output_type=GreetingResponse,  # <-- This makes agent return GreetingResponse
#   )
#
# Note: TestModel won't actually populate fields intelligently, but in production
# with a real LLM, you'd get properly structured responses.

# -----------------------------------------------------------------------------
# Challenge 3: Examine result.all_messages() to see conversation history
# -----------------------------------------------------------------------------
# The result object contains the full message history from the run.
# Explore what's in result.all_messages() to understand the conversation flow.
#
# Example:
#   result = agent.run_sync("Hello!")
#   for i, message in enumerate(result.all_messages()):
#       print(f"\nMessage {i}: {type(message).__name__}")
#       print(f"  {message}")
#
# You should see:
# - ModelRequest (user message)
# - ModelResponse (assistant response)
#
# This is important for Exercise 5 where we extract tool calls from messages.
