"""
Exercise 3: Adding Tools to Your Agent
======================================

In this exercise, you'll learn how to give your agent TOOLS - functions it
can call to perform actions or retrieve information. By the end, you'll understand:

- What tools are and why agents need them
- How to register tools with @agent.tool_plain
- How the LLM decides when to call tools
- How tool docstrings become descriptions for the LLM

Difficulty: Intermediate
Time: ~45 minutes

Run: uv run python exercises/03_tools_v2.py

📚 DOCUMENTATION LINKS (bookmark these!):
- PydanticAI Tools: https://ai.pydantic.dev/tools/
- Function Tools: https://ai.pydantic.dev/tools/#function-tools

⚠️  IMPORTANT: When asking AI assistants for help, ALWAYS include the doc URL!
    Libraries like PydanticAI evolve over time, and AI models may have outdated
    information. Grounding your questions in current docs prevents bad answers.
"""

import random
from datetime import datetime

from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel

# =============================================================================
# CONCEPT: What are Tools and why do agents need them?
# =============================================================================
#
# LLMs can only generate text - they can't actually DO anything. Tools bridge
# this gap by letting the LLM "call" functions in your code.
#
# Flow with tools:
#   1. User asks: "What time is it?"
#   2. LLM sees it has a get_time tool and decides to call it
#   3. PydanticAI runs your get_time() function
#   4. Result goes back to the LLM
#   5. LLM incorporates the result into its response
#
# Without tools, the LLM would have to guess or say "I don't know."
#
# 🤖 Ask your AI assistant:
#    "Read https://ai.pydantic.dev/tools/ and explain when an agent
#     would use tools vs just responding with text"
# =============================================================================


# =============================================================================
# CONCEPT: The @agent.tool_plain decorator
# =============================================================================
#
# PydanticAI uses DECORATORS to register functions as tools. Remember from
# Exercise 1: a decorator wraps a function to add behavior.
#
#   @agent.tool_plain
#   def my_function():
#       ...
#
# This tells PydanticAI: "The LLM can call my_function!"
#
# There are TWO tool decorators:
#   @agent.tool_plain  → Simple tools that don't need context
#   @agent.tool        → Tools that need access to dependencies (Exercise 4)
#
# Use @agent.tool_plain when your function:
#   - Doesn't need any runtime context
#   - Just takes simple arguments and returns a result
#
# 📚 Docs: https://ai.pydantic.dev/tools/#function-tools
# =============================================================================


# =============================================================================
# CONCEPT: How does the LLM know about your tools?
# =============================================================================
#
# When you register a tool, PydanticAI automatically extracts:
#
#   1. Function name → becomes the tool name
#   2. Docstring → becomes the tool description (LLM reads this!)
#   3. Parameters → become the tool's input schema
#   4. Type hints → tell the LLM what types to provide
#
# This is why DOCSTRINGS MATTER! The LLM uses them to decide:
#   - When to call your tool
#   - What arguments to pass
#
# Bad docstring:  "Does stuff"
# Good docstring: "Roll a die with the specified number of sides"
#
# 🤖 Ask your AI assistant:
#    "Read https://ai.pydantic.dev/tools/ and explain how PydanticAI
#     converts function docstrings into tool descriptions for the LLM"
# =============================================================================


# =============================================================================
# WORKING EXAMPLE: A Dice-Rolling Agent
# =============================================================================

def create_dice_agent() -> Agent[None, str]:
    """Create an agent that can roll dice."""
    model = TestModel()

    agent: Agent[None, str] = Agent(
        model,
        instructions=(
            "You are a dice game assistant. "
            "When asked to roll dice, use the roll_dice tool. "
            "Report the result to the user."
        ),
    )

    # Register a tool using the decorator
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
    print("DEMO: Agent Calling a Tool")
    print("=" * 60)

    agent = create_dice_agent()

    # When we ask about dice, the agent calls the roll_dice tool
    result = agent.run_sync("Roll a die for me")

    print("\nPrompt: 'Roll a die for me'")
    print(f"Output: {result.output}")

    # Look at the message history to see the tool call
    print("\nMessage history (notice the tool call!):")
    for msg in result.all_messages():
        print(f"  {type(msg).__name__}")


# =============================================================================
# WORKING EXAMPLE: A Time-Checking Agent
# =============================================================================

def create_time_agent() -> Agent[None, str]:
    """Create an agent that can tell the time."""
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


def demo_no_args_tool():
    """Demonstrate a tool that takes no arguments."""
    print("\n" + "=" * 60)
    print("DEMO: Tool Without Arguments")
    print("=" * 60)

    agent = create_time_agent()
    result = agent.run_sync("What time is it?")

    print("\nPrompt: 'What time is it?'")
    print(f"Output: {result.output}")


# =============================================================================
# CONCEPT: When Do You Need Tools?
# =============================================================================
#
# Tools add power but also complexity. Consider whether you need them:
#
# ✅ USE TOOLS WHEN:
#   - The LLM needs to access external data (databases, APIs, files)
#   - The LLM needs to perform actions (send email, create files)
#   - The LLM needs real-time information (current time, stock prices)
#   - You want the LLM to decide which action to take
#
# ❌ MIGHT NOT NEED TOOLS WHEN:
#   - You're just processing/transforming text
#   - All information is already in the prompt
#   - You can call the external API yourself and pass results to LLM
#
# EXAMPLE - Two ways to get weather:
#
#   WITH TOOL (LLM decides when to fetch):
#     @agent.tool_plain
#     def get_weather(city: str) -> str:
#         return fetch_weather_api(city)
#
#   WITHOUT TOOL (you control when to fetch):
#     weather_data = fetch_weather_api("Tokyo")
#     result = agent.run_sync(f"Weather is {weather_data}. Summarize it.")
#
# Both work! Tools give the LLM autonomy; no-tools give YOU control.
#
# =============================================================================


if __name__ == "__main__":
    demo_tool_call()
    demo_no_args_tool()

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
# EXERCISE 1: Add a second tool to an agent
# =============================================================================
#
# Create an agent with MULTIPLE tools and see how the LLM chooses between them.
#
# STEP 1: Create an agent with two game tools
#
#   def create_games_agent() -> Agent[None, str]:
#       model = TestModel()
#
#       agent: Agent[None, str] = Agent(
#           model,
#           instructions="You are a games assistant with dice and coins.",
#       )
#
#       @agent.tool_plain
#       def roll_dice(sides: int = 6) -> str:
#           """Roll a die with the specified number of sides."""
#           result = random.randint(1, sides)
#           return f"Rolled d{sides}: {result}"
#
#       # TODO: Add a flip_coin tool here
#       # It should:
#       #   - Take no arguments
#       #   - Return "Heads!" or "Tails!" randomly
#       #   - Have a clear docstring
#
#       @agent.tool_plain
#       def flip_coin() -> str:
#           """_____"""  # Write a good docstring!
#           _____  # Implement the function
#
#       return agent
#
# STEP 2: Test with different prompts
#
#   agent = create_games_agent()
#   print(agent.run_sync("Roll a d20").output)
#   print(agent.run_sync("Flip a coin").output)
#   print(agent.run_sync("I need a random choice").output)
#
# 💡 HINTS:
#   - Use random.choice(["Heads!", "Tails!"])
#   - Your docstring should clearly say what the function does
#   - TestModel will call all tools; real LLMs choose based on the prompt
#
# 🤖 Stuck? Ask your AI assistant:
#   - "Read https://ai.pydantic.dev/tools/ and show me how to add
#      multiple tools to a single agent"
# =============================================================================


# =============================================================================
# EXERCISE 2: Add parameter descriptions with Annotated
# =============================================================================
#
# You can add descriptions to individual parameters using Annotated and Field.
# This gives the LLM more context about what values to provide.
#
# STEP 1: Import the required types
#
#   from typing import Annotated
#   from pydantic import Field
#
# STEP 2: Create a tool with annotated parameters
#
#   @agent.tool_plain
#   def roll_dice(
#       sides: Annotated[int, Field(description="_____")] = 6,
#       count: Annotated[int, Field(description="_____")] = 1,
#   ) -> str:
#       """Roll one or more dice.
#
#       Use this for tabletop games like D&D.
#       """
#       # TODO: Roll 'count' dice, each with 'sides' sides
#       # Return something like "Rolled 3d6: [4, 2, 5] (total: 11)"
#       results = _____
#       return f"Rolled {count}d{sides}: {results} (total: {sum(results)})"
#
# STEP 3: Test it
#
#   agent = create_enhanced_dice_agent()
#   print(agent.run_sync("Roll 4d6 for stats").output)
#
# 💡 HINTS:
#   - Annotated[type, Field(...)] adds metadata to a parameter
#   - Field(description="...") is what the LLM sees
#   - Use a list comprehension: [random.randint(1, sides) for _ in range(count)]
#
# 🤖 Stuck? Ask your AI assistant:
#   - "Read https://ai.pydantic.dev/tools/ and explain how to use
#      Annotated with Field to add parameter descriptions"
# =============================================================================


# =============================================================================
# EXERCISE 3: Create a tool that returns JSON
# =============================================================================
#
# Tools can return structured data as JSON strings. The LLM can parse this
# and present it nicely to the user.
#
# STEP 1: Create a weather tool that returns JSON
#
#   import json
#
#   @agent.tool_plain
#   def get_weather(city: str) -> str:
#       """Get current weather for a city.
#
#       Args:
#           city: Name of the city to check weather for
#
#       Returns:
#           JSON string with weather data
#       """
#       # Simulated weather (real app would call an API)
#       weather = {
#           "city": city,
#           "temperature_f": random.randint(50, 90),
#           "conditions": random.choice(["Sunny", "Cloudy", "Rainy"]),
#           "humidity_percent": random.randint(30, 80),
#       }
#       return json.dumps(weather)
#
# STEP 2: Test it and observe how the LLM handles JSON
#
#   result = agent.run_sync("What's the weather in Tokyo?")
#   print(result.output)
#
# 💡 WHY JSON?
#   - Structured data is easier for the LLM to parse
#   - You could also return Pydantic models (they serialize to JSON)
#   - This pattern is common when tools call external APIs
#
# 🤖 Stuck? Ask your AI assistant:
#   - "What's the best way to return structured data from a PydanticAI tool?"
# =============================================================================


# =============================================================================
# EXERCISE 4: Examine tool calls in message history
# =============================================================================
#
# This is IMPORTANT preparation for Exercise 5! Let's see how tool calls
# appear in the message history.
#
# STEP 1: Run an agent with tools and examine messages
#
#   agent = create_dice_agent()
#   result = agent.run_sync("Roll a d20")
#
#   print("Message history with tool calls:")
#   for msg in result.all_messages():
#       print(f"\n{type(msg).__name__}:")
#       if hasattr(msg, 'parts'):
#           for part in msg.parts:
#               print(f"  {type(part).__name__}")
#               # Look for ToolCallPart and ToolReturnPart!
#
# STEP 2: Answer these questions
#
#   # Q1: Which message type contains ToolCallPart?
#   # A1: _____
#
#   # Q2: Which message type contains ToolReturnPart?
#   # A2: _____
#
#   # Q3: What information is in a ToolCallPart? (tool name? arguments?)
#   # A3: _____
#
# 💡 WHY THIS MATTERS:
#   In Exercise 5, you'll extract tool calls to display them in a UI.
#   The message history is where that data lives!
#
# 🤖 Stuck? Ask your AI assistant:
#   - "Read https://ai.pydantic.dev/results/ and explain what ToolCallPart
#      and ToolReturnPart contain in the message history"
# =============================================================================


# =============================================================================
# EXERCISE 5: Think about tool design (thought exercise)
# =============================================================================
#
# Good tool design matters! Consider these scenarios:
#
# SCENARIO A: Email sender
#
#   Option 1 - Coarse-grained tool:
#     def send_email(recipient: str, subject: str, body: str) -> str:
#         """Send an email."""
#         # ... sends the email ...
#
#   Option 2 - Fine-grained tools:
#     def draft_email(subject: str, body: str) -> str:
#         """Draft an email (doesn't send)."""
#     def send_draft(draft_id: str, recipient: str) -> str:
#         """Send a previously drafted email."""
#
#   Q: Which is safer? Why?
#   A: _____
#
#
# SCENARIO B: Database queries
#
#   Option 1 - Give LLM raw SQL:
#     def run_query(sql: str) -> str:
#         """Run any SQL query."""
#         return db.execute(sql)
#
#   Option 2 - Specific operations:
#     def get_user(user_id: str) -> str:
#         """Look up a user by ID."""
#     def list_orders(user_id: str, limit: int = 10) -> str:
#         """List recent orders for a user."""
#
#   Q: What's the security risk of Option 1?
#   A: _____
#
#
# SCENARIO C: File operations
#
#   You want the LLM to help organize files. What tools would you create?
#   Think about: What operations are safe? What should require confirmation?
#
#   Your tool list:
#   1. _____
#   2. _____
#   3. _____
#
# 💡 KEY INSIGHT:
#   Tools should be the MINIMUM power needed to accomplish the task.
#   More specific tools = safer and more predictable behavior.
#
# =============================================================================


# =============================================================================
# BONUS CHALLENGE: Dynamic tool behavior
# =============================================================================
#
# What if you want a tool's behavior to depend on some runtime value?
# That's what @agent.tool (not tool_plain) is for - it gives you access
# to the RunContext with dependencies. We'll cover this in Exercise 4!
#
# For now, try creating a tool that:
#   - Takes a "difficulty" parameter
#   - Returns different results based on difficulty
#   - Has a clear docstring explaining the difficulty levels
#
# Example:
#   from typing import Literal
#
#   @agent.tool_plain
#   def generate_challenge(difficulty: Literal["easy", "medium", "hard"]) -> str:
#       """Generate a coding challenge at the specified difficulty."""
#       challenges = {
#           "easy": "FizzBuzz",
#           "medium": "Binary search",
#           "hard": "Red-black tree",
#       }
#       return f"Your challenge: {challenges[difficulty]}"
#
# 🤖 Ready for more? Ask your AI assistant:
#   - "Read https://ai.pydantic.dev/tools/#tools-vs-plain-tools and explain
#      when I should use @agent.tool vs @agent.tool_plain"
# =============================================================================
