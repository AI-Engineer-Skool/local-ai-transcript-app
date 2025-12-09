"""
Exercise 3: Adding Tools with @agent.tool_plain

Concept: Tools let agents perform actions. The @agent.tool_plain decorator
registers functions that don't need access to RunContext (dependencies).
The agent decides when to call tools based on the user's prompt.

Difficulty: Intermediate

Run: uv run python exercises/03_tools_simple.py
"""

import random
from datetime import datetime

from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel

# =============================================================================
# WORKING BASE CODE
# =============================================================================


def create_dice_agent() -> Agent[None, str]:
    """Create an agent with a simple dice-rolling tool.

    @agent.tool_plain is for tools that:
    - Don't need access to dependencies (RunContext)
    - Take simple arguments (primitives, not Pydantic models)
    - Return a string result
    """
    # Configure TestModel to call our tool
    # In production, the LLM decides; for testing, we configure it explicitly
    model = TestModel()

    agent: Agent[None, str] = Agent(
        model,
        instructions=(
            "You are a dice game assistant. "
            "When asked to roll dice, use the roll_dice tool. "
            "Report the result to the user."
        ),
    )

    @agent.tool_plain
    def roll_dice(sides: int = 6) -> str:
        """Roll a die with the specified number of sides.

        Args:
            sides: Number of sides on the die (default 6)

        Returns:
            String describing the roll result
        """
        result = random.randint(1, sides)
        return f"Rolled a {sides}-sided die: {result}"

    return agent


def demo_tool_call():
    """Demonstrate how an agent calls a tool."""
    print("=" * 60)
    print("DEMO: Basic Tool Call")
    print("=" * 60)

    agent = create_dice_agent()

    # Run the agent - it will decide whether to call the tool
    result = agent.run_sync("Roll a die for me")

    print("\nPrompt: 'Roll a die for me'")
    print(f"Output: {result.output}")

    # Let's see what happened in the conversation
    print("\nMessage history:")
    for msg in result.all_messages():
        print(f"  {type(msg).__name__}: {str(msg)[:100]}...")


def create_time_agent() -> Agent[None, str]:
    """Create an agent with a time-checking tool."""
    model = TestModel()

    agent: Agent[None, str] = Agent(
        model,
        instructions=(
            "You are a helpful assistant that can tell the current time. "
            "Use the get_current_time tool when asked about the time."
        ),
    )

    @agent.tool_plain
    def get_current_time() -> str:
        """Get the current date and time.

        Returns:
            Current datetime as a formatted string
        """
        now = datetime.now()
        return f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}"

    return agent


def demo_tool_without_args():
    """Demonstrate a tool that takes no arguments."""
    print("\n" + "=" * 60)
    print("DEMO: Tool Without Arguments")
    print("=" * 60)

    agent = create_time_agent()
    result = agent.run_sync("What time is it?")

    print("\nPrompt: 'What time is it?'")
    print(f"Output: {result.output}")


def demo_tool_docstring():
    """Show how tool docstrings become descriptions for the LLM."""
    print("\n" + "=" * 60)
    print("DEMO: Tool Docstrings as LLM Descriptions")
    print("=" * 60)

    agent = create_dice_agent()

    # The agent has a tools property that shows registered tools
    # In PydanticAI, the docstring becomes the tool description
    print("\nTool docstrings help the LLM understand when to use each tool.")
    print("Write clear, concise docstrings that explain:")
    print("  1. What the tool does")
    print("  2. What arguments it accepts")
    print("  3. What it returns")


if __name__ == "__main__":
    demo_tool_call()
    demo_tool_without_args()
    demo_tool_docstring()

    print("\n" + "=" * 60)
    print("BASE CODE COMPLETE - Try the challenges below!")
    print("=" * 60)


# =============================================================================
# CHALLENGES
# =============================================================================

# -----------------------------------------------------------------------------
# Challenge 1: Add a second tool and see how the agent chooses
# -----------------------------------------------------------------------------
# Add a `flip_coin` tool to the dice agent:
#
#   @agent.tool_plain
#   def flip_coin() -> str:
#       """Flip a coin and return heads or tails."""
#       return random.choice(["Heads!", "Tails!"])
#
# Then try different prompts:
#   - "Roll a die" -> should call roll_dice
#   - "Flip a coin" -> should call flip_coin
#   - "Give me a random choice" -> might call either!
#
# Note: With TestModel, you need to configure which tool gets called.
# In production, the LLM chooses based on the prompt and tool descriptions.

# -----------------------------------------------------------------------------
# Challenge 2: Add type hints with descriptions for better tool selection
# -----------------------------------------------------------------------------
# Use typing.Annotated to add descriptions to parameters:
#
#   from typing import Annotated
#   from pydantic import Field
#
#   @agent.tool_plain
#   def roll_dice(
#       sides: Annotated[int, Field(description="Number of sides on the die")] = 6,
#       count: Annotated[int, Field(description="Number of dice to roll")] = 1,
#   ) -> str:
#       """Roll one or more dice."""
#       results = [random.randint(1, sides) for _ in range(count)]
#       return f"Rolled {count}d{sides}: {results} (total: {sum(results)})"
#
# This gives the LLM better context for filling in arguments.

# -----------------------------------------------------------------------------
# Challenge 3: Make a tool return structured data (JSON string)
# -----------------------------------------------------------------------------
# Create a tool that returns JSON instead of plain text:
#
#   @agent.tool_plain
#   def get_weather(city: str) -> str:
#       """Get weather information for a city."""
#       # Simulated weather data
#       weather = {
#           "city": city,
#           "temperature": random.randint(50, 90),
#           "conditions": random.choice(["Sunny", "Cloudy", "Rainy"]),
#           "humidity": random.randint(30, 80),
#       }
#       return json.dumps(weather)
#
# The LLM can parse JSON results and incorporate them into responses.
# This pattern bridges simple tools to more complex structured outputs.
