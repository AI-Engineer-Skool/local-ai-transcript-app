"""
Exercise 2: Creating and Running a PydanticAI Agent
===================================================

In this exercise, you'll learn what an Agent is and how to use one.
By the end, you'll understand:

- What an Agent is (and isn't)
- How instructions shape the LLM's behavior
- How to run an agent and get results
- When you need an agent vs a simple LLM call

Difficulty: Beginner
Time: ~30 minutes

Run: uv run python exercises/02_basic_agent_v2.py

📚 DOCUMENTATION LINKS:
- PydanticAI Agents: https://ai.pydantic.dev/agents/
- Running Agents: https://ai.pydantic.dev/agents/#running-agents
- Agent Results: https://ai.pydantic.dev/results/

⚠️  IMPORTANT: When asking AI assistants for help, ALWAYS include the doc URL!
    Libraries evolve over time, and AI models may have outdated information.
"""

# =============================================================================
# CONCEPT: What is an Agent?
# =============================================================================
#
# An Agent is PydanticAI's way of packaging everything needed to interact
# with an LLM:
#
#   - Model: Which LLM to use (GPT-4, Claude, etc.)
#   - Instructions: How the LLM should behave (like a system prompt)
#   - Tools: Functions the LLM can call (covered in Exercise 3)
#   - Dependencies: Runtime data to pass in (covered in Exercise 4)
#   - Output type: What format the response should be in
#
# Think of an Agent as a reusable "LLM configuration" that you can call
# multiple times with different inputs.
#
# 🤖 Ask your AI assistant:
#    "Read https://ai.pydantic.dev/agents/ and summarize the main
#     components of a PydanticAI Agent"
# =============================================================================

from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel

# =============================================================================
# CONCEPT: TestModel - For Learning Without API Costs
# =============================================================================
#
# TestModel is a FAKE LLM that doesn't call any API. It returns instant,
# predictable responses. This is perfect for:
#
#   - Learning PydanticAI without spending money
#   - Writing tests for your agent code
#   - Debugging agent logic
#
# In production, you'd use a real model like:
#   - "openai:gpt-4o"
#   - "anthropic:claude-sonnet-4-20250514"
#   - "groq:llama-3.3-70b-versatile"
#
# 📚 Docs: https://ai.pydantic.dev/models/
# =============================================================================


# =============================================================================
# CONCEPT: Understanding Agent[None, str]
# =============================================================================
#
# The type hint Agent[None, str] tells you two things:
#
#   Agent[DepsType, OutputType]
#         ↑          ↑
#         |          └── What the agent returns (str = plain text)
#         └── What dependencies it needs (None = no dependencies)
#
# This typing helps your IDE provide autocomplete and catch errors.
# We'll cover dependencies in Exercise 4 - for now, None means "no deps".
#
# =============================================================================


def create_simple_agent() -> Agent[None, str]:
    """Create a basic agent with instructions."""

    # Use TestModel for learning - no API calls!
    model = TestModel()

    # Create the agent
    agent: Agent[None, str] = Agent(
        model,
        instructions=(
            "You are a helpful assistant. "
            "Be concise and friendly in your responses."
        ),
    )

    return agent


# =============================================================================
# CONCEPT: What are "instructions"?
# =============================================================================
#
# Instructions are like a system prompt - they tell the LLM how to behave
# for ALL interactions with this agent.
#
# Good instructions are:
#   - Clear about the agent's role: "You are a customer support agent"
#   - Specific about behavior: "Always ask clarifying questions"
#   - Relevant to the task: "Focus on technical Python questions"
#
# The LLM sees these instructions before every user message.
#
# =============================================================================


def demo_running_agent():
    """Show how to run an agent and get results."""
    print("=" * 60)
    print("DEMO: Running an Agent")
    print("=" * 60)

    agent = create_simple_agent()

    # run_sync() sends a message and waits for the response
    result = agent.run_sync("Hello!")

    print(f"\nInput: 'Hello!'")
    print(f"Output: {result.output}")
    print(f"Output type: {type(result.output).__name__}")


def demo_custom_response():
    """Show how TestModel can return specific text for testing."""
    print("\n" + "=" * 60)
    print("DEMO: Custom Test Responses")
    print("=" * 60)

    # Configure TestModel to return specific text
    model = TestModel(custom_output_text="I'm a test response!")

    agent: Agent[None, str] = Agent(
        model,
        instructions="You are helpful.",
    )

    result = agent.run_sync("Say something")
    print(f"\nWith custom_output_text: {result.output}")
    print("\n💡 This is useful for testing specific scenarios!")


def demo_multiple_runs():
    """Show that each run is independent."""
    print("\n" + "=" * 60)
    print("DEMO: Multiple Independent Runs")
    print("=" * 60)

    agent = create_simple_agent()

    # Each run is independent - no memory between calls
    prompts = ["First message", "Second message", "Third message"]

    for prompt in prompts:
        result = agent.run_sync(prompt)
        print(f"\nInput: '{prompt}'")
        print(f"Output: {result.output}")

    print("\n💡 By default, each run starts fresh - no conversation memory!")
    print("   (You can pass message_history to continue conversations)")


# =============================================================================
# CONCEPT: When Do You Actually Need an Agent?
# =============================================================================
#
# PydanticAI Agents are powerful, but they're not always necessary.
#
# ✅ USE AN AGENT WHEN:
#   - You need tools (functions the LLM can call)
#   - You need structured output (Pydantic model responses)
#   - You need dependency injection (runtime context)
#   - You want automatic retries on validation errors
#   - You're building something reusable
#
# ❌ CONSIDER SIMPLER APPROACHES WHEN:
#   - You just need a one-off LLM call
#   - The output is simple text
#   - You don't need tools or structured data
#   - Token cost is a major concern
#
# Simple alternative (no framework):
#
#   from openai import OpenAI
#   client = OpenAI()
#   response = client.chat.completions.create(
#       model="gpt-4o",
#       messages=[{"role": "user", "content": "Hello!"}]
#   )
#   print(response.choices[0].message.content)
#
# Know when each approach makes sense!
#
# =============================================================================


def demo_agent_overhead():
    """Illustrate that agents add structure (which may or may not be needed)."""
    print("\n" + "=" * 60)
    print("DEMO: Agent Structure vs Simple Calls")
    print("=" * 60)

    print("\n📦 With PydanticAI Agent:")
    print("   - Structured Agent object")
    print("   - Type safety with Agent[DepsType, OutputType]")
    print("   - Built-in retry logic")
    print("   - Tool registration system")
    print("   - Result object with metadata")

    print("\n📝 With direct API call:")
    print("   - Just a function call")
    print("   - String in, string out")
    print("   - You handle errors yourself")
    print("   - Simpler, less overhead")

    print("\n💡 Neither is 'better' - choose based on your needs!")


if __name__ == "__main__":
    demo_running_agent()
    demo_custom_response()
    demo_multiple_runs()
    demo_agent_overhead()

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
# EXERCISE 1: Create an agent with a specific personality
# =============================================================================
#
# Create an agent with custom instructions that give it a personality.
#
# STEP 1: Write the function
#
#   def create_pirate_agent() -> Agent[None, str]:
#       """An agent that talks like a pirate."""
#       model = TestModel(
#           custom_output_text="Ahoy! What treasure be ye seekin'?"
#       )
#
#       agent: Agent[None, str] = Agent(
#           model,
#           instructions="_____",  # Write pirate personality instructions!
#       )
#       return agent
#
# STEP 2: Test it
#
#   agent = create_pirate_agent()
#   result = agent.run_sync("Hello!")
#   print(result.output)
#
# STEP 3: Try different personalities
#   - A formal British butler
#   - An excited sports commentator
#   - A patient teacher
#
# 💡 HINTS:
#   - Instructions shape ALL responses from this agent
#   - Be specific: "Always say 'Arrr!'" vs "Talk like a pirate"
#   - custom_output_text simulates what a real LLM might say
#
# 🤖 Ask your AI assistant:
#   - "Read https://ai.pydantic.dev/agents/ and show me how instructions
#      affect agent behavior"
# =============================================================================


# =============================================================================
# EXERCISE 2: Examine the result object
# =============================================================================
#
# The result from agent.run_sync() isn't just a string - it's a rich object
# with useful information.
#
# STEP 1: Run an agent and explore the result
#
#   agent = create_simple_agent()
#   result = agent.run_sync("Tell me something")
#
#   print(f"Output: {result.output}")
#   print(f"Type: {type(result)}")
#
#   # What methods/attributes does result have?
#   print([attr for attr in dir(result) if not attr.startswith('_')])
#
# STEP 2: Look at the message history
#
#   for i, msg in enumerate(result.all_messages()):
#       print(f"\nMessage {i}: {type(msg).__name__}")
#
# STEP 3: Answer these questions
#
#   Q1: What type is the result object?
#   A1: _____
#
#   Q2: What does result.all_messages() return?
#   A2: _____
#
#   Q3: Why might you need access to the message history?
#   A3: _____  (Hint: think about tool calls in Exercise 3)
#
# 🤖 Ask your AI assistant:
#   - "Read https://ai.pydantic.dev/results/ and explain what's in
#      an AgentRunResult"
# =============================================================================


# =============================================================================
# EXERCISE 3: Think about when to use agents (thought exercise)
# =============================================================================
#
# For each scenario, decide: Agent or simple API call?
#
# SCENARIO A: Chat with customer support context
#   - Need to remember conversation history
#   - May need to look up order information (tool)
#   - Should respond in a specific format
#
#   Your answer: _____
#   Why: _____
#
#
# SCENARIO B: Summarize a document
#   - One-off task
#   - Just need a text summary back
#   - No tools or special formatting needed
#
#   Your answer: _____
#   Why: _____
#
#
# SCENARIO C: Extract structured data from emails
#   - Need specific fields (sender, subject, action items)
#   - Should validate the extracted data
#   - Will process many emails
#
#   Your answer: _____
#   Why: _____
#
#
# SCENARIO D: Generate a creative story
#   - Just need text output
#   - No validation needed
#   - Simple prompt in, story out
#
#   Your answer: _____
#   Why: _____
#
#
# 💡 KEY INSIGHT:
#   Agents shine when you need structure, tools, or validation.
#   For simple text-in-text-out tasks, direct API calls may be simpler.
#
# =============================================================================


# =============================================================================
# EXERCISE 4: Async vs Sync
# =============================================================================
#
# PydanticAI supports both synchronous and asynchronous execution:
#
#   # Synchronous (blocking)
#   result = agent.run_sync("Hello")
#
#   # Asynchronous (non-blocking)
#   result = await agent.run("Hello")
#
# STEP 1: Try the async version
#
#   import asyncio
#
#   async def main():
#       agent = create_simple_agent()
#       result = await agent.run("Hello async!")
#       print(result.output)
#
#   asyncio.run(main())
#
# STEP 2: Think about when you'd use each
#
#   Q: When would async be beneficial?
#   A: _____  (Hint: web servers, processing multiple requests)
#
#   Q: When is sync simpler?
#   A: _____  (Hint: scripts, notebooks, simple programs)
#
# 📚 Docs: https://ai.pydantic.dev/agents/#running-agents
# =============================================================================


# =============================================================================
# BONUS: Continue a conversation
# =============================================================================
#
# By default, each run_sync() call is independent. To continue a conversation,
# pass the message history from the previous result:
#
#   # First message
#   result1 = agent.run_sync("My name is Alice")
#
#   # Continue the conversation
#   result2 = agent.run_sync(
#       "What's my name?",
#       message_history=result1.all_messages()
#   )
#
# Try it! The agent should remember information from earlier messages.
#
# 🤖 Ask your AI assistant:
#   - "Read https://ai.pydantic.dev/agents/#agent-run and explain how
#      message_history enables multi-turn conversations"
# =============================================================================
