"""
Exercise 1: Pydantic Models for AI Tool Inputs
==============================================

In this exercise, you'll learn how Pydantic models work and why they're
the foundation for building AI agents. By the end, you'll understand:

- What BaseModel gives you (automatic validation, JSON schema)
- How Field descriptions tell the LLM what data to extract
- How validators provide FEEDBACK to the LLM when data is wrong
- The retry loop: validation errors help the LLM correct itself

Difficulty: Beginner
Time: ~30 minutes

Run: uv run python exercises/01_pydantic_models_v2.py

📚 DOCUMENTATION LINKS (bookmark these!):
- Pydantic Models: https://docs.pydantic.dev/latest/concepts/models/
- Pydantic Fields: https://docs.pydantic.dev/latest/concepts/fields/
- Pydantic Validators: https://docs.pydantic.dev/latest/concepts/validators/
- PydanticAI Retries: https://ai.pydantic.dev/agents/#retries

⚠️  IMPORTANT: When asking AI assistants for help, ALWAYS include the doc URL!
    Libraries like Pydantic evolve over time, and AI models may have outdated
    information. Grounding your questions in current docs prevents bad answers.

    ❌ Bad:  "How do I validate a field in Pydantic?"
    ✅ Good: "Read https://docs.pydantic.dev/latest/concepts/validators/ and
             show me how to validate a field"
"""

# =============================================================================
# CONCEPT: What is Pydantic and why do AI agents need it?
# =============================================================================
#
# Pydantic is a data validation library. When you create a class that inherits
# from BaseModel, you get automatic:
#
#   1. Type validation - wrong types raise errors
#   2. JSON schema generation - this is what the LLM reads!
#   3. Serialization - convert to dict/JSON easily
#
# For AI agents, the JSON schema is KEY. When your agent has a tool that
# takes a Pydantic model as input, the LLM sees the schema and knows
# exactly what data to provide.
#
# 🤖 Ask your AI assistant:
#    "Read https://docs.pydantic.dev/latest/concepts/models/ and explain
#     what BaseModel gives me that a regular Python class doesn't"
# =============================================================================

import json
from typing import Literal

from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator

# =============================================================================
# CONCEPT: Field() and descriptions - talking to the LLM
# =============================================================================
#
# Field() adds metadata to your model fields. The most important parameter
# for AI agents is `description`:
#
#   task: str = Field(description="The action item or task to be done")
#
# This description goes into the JSON schema, which the LLM reads!
# Better descriptions = better LLM understanding = better results.
#
# Without Field():  LLM sees just "task: string"
# With Field():     LLM sees "task: string - The action item or task to be done"
#
# 📚 Read more: https://docs.pydantic.dev/latest/concepts/fields/
# =============================================================================


class TaskItem(BaseModel):
    """A single task extracted from a meeting transcript.

    The Field descriptions tell the LLM what each field should contain.
    When the LLM calls a tool with this model as input, it reads these
    descriptions to understand what data to extract.
    """

    task: str = Field(
        description="The action item or task to be done"
    )
    owner: str = Field(
        description="Person responsible for this task (a real name, not 'TBD')"
    )
    priority: Literal["high", "medium", "low"] = Field(
        default="medium",
        description="Priority level: high (urgent), medium (normal), low (backlog)"
    )
    estimated_hours: float = Field(
        default=1.0,
        description="Estimated hours to complete (e.g., 0.5, 1, 2, 4)"
    )


# =============================================================================
# CONCEPT: What is Literal[]?
# =============================================================================
#
# Literal["high", "medium", "low"] means the value MUST be one of these
# exact strings. In the JSON schema, this appears as an "enum" - a fixed
# set of choices.
#
# This is powerful because:
#   - Pydantic rejects invalid values automatically
#   - The LLM sees the valid options and picks from them
#   - No need to handle "urgent", "critical", "ASAP" etc.
#
# 🤖 Ask your AI assistant:
#    "When should I use Literal[] vs a regular str type in Pydantic?"
# =============================================================================


def demo_basic_model():
    """Demonstrate basic Pydantic model usage."""
    print("=" * 60)
    print("DEMO: Basic Pydantic Model")
    print("=" * 60)

    # Creating an instance - Pydantic validates all fields
    task = TaskItem(
        task="Review the API design document",
        owner="Alice",
        priority="high",
        estimated_hours=2.0,
    )
    print(f"\nCreated task: {task}")
    print(f"  task: {task.task}")
    print(f"  owner: {task.owner}")
    print(f"  priority: {task.priority}")
    print(f"  estimated_hours: {task.estimated_hours}")

    # Using defaults
    task2 = TaskItem(task="Update docs", owner="Bob")
    print(f"\nWith defaults: priority={task2.priority}, hours={task2.estimated_hours}")


def demo_json_schema():
    """Show the JSON schema that the LLM sees."""
    print("\n" + "=" * 60)
    print("DEMO: JSON Schema (what the LLM sees)")
    print("=" * 60)

    schema = TaskItem.model_json_schema()
    print("\nThis schema is sent to the LLM when your tool uses TaskItem:")
    print(json.dumps(schema, indent=2))

    print("\n💡 Notice how Field descriptions appear in the schema!")
    print("   The LLM reads these to understand what data to provide.")


def demo_automatic_validation():
    """Show Pydantic's automatic type validation."""
    print("\n" + "=" * 60)
    print("DEMO: Automatic Type Validation")
    print("=" * 60)

    # Pydantic automatically validates types
    print("\nTrying invalid priority='urgent' (not in Literal choices)...")
    try:
        TaskItem(task="Test", owner="Alice", priority="urgent")  # type: ignore
    except ValidationError as e:
        print(f"  ❌ ValidationError: {e.errors()[0]['msg']}")

    print("\nTrying missing required field (no owner)...")
    try:
        TaskItem(task="Test")  # type: ignore
    except ValidationError as e:
        print(f"  ❌ ValidationError: {e.errors()[0]['msg']}")

    print("\n✅ Pydantic catches invalid data before it causes problems!")


# =============================================================================
# CONCEPT: Validators as LLM Feedback (The Retry Loop)
# =============================================================================
#
# This is CRUCIAL for AI agents:
#
# When the LLM provides data that fails validation, PydanticAI:
#   1. Catches the ValidationError
#   2. Sends the error message BACK to the LLM
#   3. The LLM gets a chance to RETRY with corrected data
#
# This means your validator error messages are FEEDBACK to the LLM!
#
#   # Bad - LLM doesn't know how to fix it
#   raise ValueError("Invalid")
#
#   # Good - LLM understands what went wrong
#   raise ValueError("estimated_hours must be positive (e.g., 0.5, 1, 2)")
#
# 📚 Docs: https://ai.pydantic.dev/agents/#retries
# =============================================================================


# =============================================================================
# CONCEPT: The Tradeoff - Retries Cost Tokens!
# =============================================================================
#
# ⚠️  IMPORTANT: Each retry is another API call = more tokens = more money!
#
# Example scenario:
#   - Meeting transcript says "This will take about 2 weeks full-time"
#   - LLM extracts: estimated_hours=80 (2 weeks × 40 hours)
#   - Your validator says: "max 8 hours per task"
#   - Retry 1: LLM tries 40 hours → Still fails
#   - Retry 2: LLM tries 8 hours → Passes, but is this even correct anymore?
#
# You just spent 3x the tokens, and the final answer (8 hours) doesn't
# match what the meeting actually said (80 hours)!
#
# KEY INSIGHT: Validators should catch LLM MISTAKES (wrong format,
# impossible values), not enforce BUSINESS RULES that might conflict
# with the actual content.
#
#   ✅ Good validator: "hours must be positive" (catches mistakes)
#   ⚠️  Risky validator: "hours must be under 8" (might fight the content)
#
# =============================================================================


# =============================================================================
# CONCEPT: When to Use Pydantic vs Simpler Approaches
# =============================================================================
#
# Pydantic + PydanticAI gives you:
#   ✅ Automatic validation and type safety
#   ✅ JSON schema that helps the LLM understand structure
#   ✅ Retry loops for self-correction
#   ✅ Clean, maintainable code
#
# But consider simpler approaches when:
#   - Output is very simple (just extracting one value)
#   - Token cost is a major concern
#   - You're writing a quick script, not production code
#   - The LLM is already reliable for your use case
#
# Sometimes a simple prompt + JSON parsing is enough:
#
#   response = llm.complete("Extract the task owner from: {text}. Reply with just the name.")
#   owner = response.strip()
#
# No framework, no retries, no complexity. Know when each approach fits!
#
# =============================================================================


class TaskItemWithValidation(BaseModel):
    """TaskItem with custom validators that provide LLM feedback."""

    task: str = Field(description="The action item or task to be done")
    owner: str = Field(description="Person responsible (a real name, not 'TBD')")
    priority: Literal["high", "medium", "low"] = Field(default="medium")
    estimated_hours: float = Field(
        default=1.0,
        description="Estimated hours to complete (must be positive)"
    )

    @field_validator("estimated_hours")
    @classmethod
    def hours_must_be_positive(cls, v):
        """Validate that estimated hours is a positive number.

        The error message is sent to the LLM if validation fails,
        so make it helpful!
        """
        if v <= 0:
            raise ValueError(
                f"estimated_hours must be a positive number (e.g., 0.5, 1, 2, 4). "
                f"Got: {v}"
            )
        return v


# =============================================================================
# CONCEPT: What is a decorator? (@field_validator)
# =============================================================================
#
# If you're new to Python, the @ syntax might look strange. A decorator is
# a function that wraps another function to add behavior.
#
#   @field_validator("estimated_hours")
#   @classmethod
#   def hours_must_be_positive(cls, v):
#       ...
#
# This tells Pydantic: "Run this function to validate the estimated_hours field"
#
# The @classmethod decorator is required because validators are called on
# the CLASS (TaskItem), not an instance. The `cls` parameter is the class.
#
# 🤖 Ask your AI assistant:
#    "Explain Python decorators with a simple example - how does @ work?"
# =============================================================================


def demo_field_validator():
    """Demonstrate custom field validation."""
    print("\n" + "=" * 60)
    print("DEMO: Custom Field Validator")
    print("=" * 60)

    print("\nTrying estimated_hours=-5 (negative)...")
    try:
        TaskItemWithValidation(
            task="Do something",
            owner="Alice",
            estimated_hours=-5
        )
    except ValidationError as e:
        print(f"  ❌ ValidationError: {e.errors()[0]['msg']}")

    print("\nTrying estimated_hours=0 (zero)...")
    try:
        TaskItemWithValidation(
            task="Do something",
            owner="Alice",
            estimated_hours=0
        )
    except ValidationError as e:
        print(f"  ❌ ValidationError: {e.errors()[0]['msg']}")

    print("\nTrying estimated_hours=2.5 (valid)...")
    task = TaskItemWithValidation(
        task="Do something",
        owner="Alice",
        estimated_hours=2.5
    )
    print(f"  ✅ Created successfully: {task.estimated_hours} hours")

    print("\n💡 These error messages would be sent to the LLM for retry!")


if __name__ == "__main__":
    demo_basic_model()
    demo_json_schema()
    demo_automatic_validation()
    demo_field_validator()

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
# EXERCISE 1: Add a field validator with helpful error messages
# =============================================================================
#
# Add a validator to check that `task` is not too short (at least 5 characters).
# Remember: the error message is feedback for the LLM!
#
# STEP 1: Add the validator to TaskItemWithValidation
#
#   @field_validator("task")
#   @classmethod
#   def task_must_be_descriptive(cls, v):
#       if len(v) < 5:
#           raise ValueError(
#               "_____"  # Write a helpful message for the LLM!
#           )
#       return v
#
# STEP 2: Test it
#
#   try:
#       TaskItemWithValidation(task="Do", owner="Alice")
#   except ValidationError as e:
#       print(e.errors()[0]['msg'])
#
# 💡 HINTS:
#   - Your error message should tell the LLM what's wrong AND how to fix it
#   - Example: "task must be at least 5 characters. Provide a clear description."
#
# 🤖 Stuck? Ask your AI assistant:
#   - "Read https://docs.pydantic.dev/latest/concepts/validators/ and show me
#      how to write a @field_validator that checks string length"
# =============================================================================


# =============================================================================
# EXERCISE 2: Create a model_validator (and understand the tradeoff!)
# =============================================================================
#
# A @model_validator runs after ALL fields are set. It can access all fields
# to check relationships or enforce rules.
#
# Goal: Enforce that tasks should be max 8 hours (break down large tasks)
#
# STEP 1: Add the model_validator
#
#   @model_validator(mode="after")
#   def tasks_should_be_manageable(self):
#       """Tasks over 8 hours should be broken into smaller chunks."""
#       if self.estimated_hours > 8:
#           raise ValueError(
#               f"Task estimated at {self.estimated_hours} hours is too large. "
#               "Break into smaller tasks (max 8 hours each)."
#           )
#       return self  # Always return self!
#
# STEP 2: Test it
#
#   # This should fail:
#   TaskItemWithValidation(task="Rewrite entire codebase", owner="Alice", estimated_hours=40)
#
#   # This should work:
#   TaskItemWithValidation(task="Refactor auth module", owner="Alice", estimated_hours=4)
#
# STEP 3: Think about the tradeoff! ⚠️
#
#   Imagine a meeting transcript says: "This migration will take about 2 weeks"
#   The LLM correctly extracts: estimated_hours=80
#   Your validator rejects it and triggers retries...
#
#   Q: Is this validator catching an LLM MISTAKE, or enforcing a BUSINESS RULE?
#   Q: What happens to your token costs if the LLM keeps retrying?
#   Q: Is the "corrected" value (8 hours) even accurate to what was said?
#
#   This is why the concepts above matter! Sometimes strict validation
#   causes more problems than it solves.
#
# 💡 HINTS:
#   - mode="after" means this runs AFTER field validators
#   - Always return self at the end
#   - Think critically about whether a validator helps or hurts
#
# 🤖 Stuck? Ask your AI assistant:
#   - "Read https://docs.pydantic.dev/latest/concepts/validators/#model-validators
#      and explain how @model_validator(mode='after') works"
# =============================================================================


# =============================================================================
# EXERCISE 3: Create a nested model (MeetingNote with TaskItems)
# =============================================================================
#
# Pydantic models can contain other models! This is powerful for complex data.
#
# STEP 1: Create a MeetingNote model
#
#   class MeetingNote(BaseModel):
#       """A meeting note containing multiple tasks."""
#
#       meeting_title: str = Field(description="_____")
#       attendees: list[str] = Field(description="_____")
#       tasks: list[TaskItem] = Field(description="_____")
#       summary: str = Field(description="_____")
#
# STEP 2: Create an instance with nested TaskItems
#
#   note = MeetingNote(
#       meeting_title="Sprint Planning",
#       attendees=["Alice", "Bob", "Charlie"],
#       tasks=[
#           TaskItem(task="Design API", owner="Alice", priority="high"),
#           TaskItem(task="Write tests", owner="Bob", estimated_hours=3),
#       ],
#       summary="Planned Q1 deliverables",
#   )
#   print(note)
#
# STEP 3: Look at the JSON schema for nested models
#
#   print(json.dumps(MeetingNote.model_json_schema(), indent=2))
#   # Notice how TaskItem is included as a nested definition!
#
# 💡 HINTS:
#   - list[TaskItem] tells Pydantic this is a list of TaskItem objects
#   - Pydantic handles nested validation automatically
#   - The JSON schema shows the complete structure to the LLM
#
# 🤖 Stuck? Ask your AI assistant:
#   - "Read https://docs.pydantic.dev/latest/concepts/models/ and show me
#      how to create a model with a list of nested models"
# =============================================================================


# =============================================================================
# EXERCISE 4: Think critically about validation (thought exercise)
# =============================================================================
#
# No code needed - just thinking!
#
# SCENARIO 1: Good validation (catching mistakes)
#
#   Transcript: "Alice will handle the security fix"
#   LLM generates: {"task": "Fix", "owner": "Alice", "estimated_hours": -1}
#
#   Q1: Which validator catches this? Is this a MISTAKE or BUSINESS RULE?
#   A1: _____
#
#   Q2: After retry, what's a reasonable corrected value?
#   A2: _____
#
#   Q3: Was the retry worth the extra tokens? (Yes - caught a real error)
#   A3: _____
#
#
# SCENARIO 2: Risky validation (fighting the content)
#
#   Transcript: "The database migration will take about 3 weeks of work"
#   LLM generates: {"task": "Database migration", "owner": "Bob", "estimated_hours": 120}
#
#   Q4: If you have a "max 8 hours" validator, what happens?
#   A4: _____
#
#   Q5: The LLM retries and eventually outputs 8 hours. Is this accurate?
#   A5: _____
#
#   Q6: You just paid for 3 API calls. Was this validation worth it?
#   A6: _____
#
#
# SCENARIO 3: When is Pydantic overkill?
#
#   Task: Extract just the meeting title from a transcript
#
#   Q7: Do you need a full Pydantic model with validators for this?
#   A7: _____
#
#   Q8: What's a simpler approach that might work?
#   A8: _____
#
#
# 💡 KEY INSIGHTS:
#   - Validators that catch MISTAKES (negative hours) → Worth the retries
#   - Validators that enforce BUSINESS RULES (max 8h) → Might fight the data
#   - Simple tasks don't always need complex frameworks
#   - Think about token costs when designing validation
#
# 🤖 Discuss with your AI assistant:
#   - "When should I use strict validation vs lenient validation in AI agents?"
#   - "How do I balance data quality with API costs?"
# =============================================================================


# =============================================================================
# BONUS: Design validators for your own use case
# =============================================================================
#
# Think of a real-world model you might use in an AI agent:
#   - A customer support ticket
#   - A recipe with ingredients
#   - A calendar event
#   - A product review
#
# For your model, consider:
#   1. What fields does it need?
#   2. What Field descriptions would help the LLM?
#   3. What validators would catch common mistakes?
#   4. What error messages would help the LLM retry correctly?
#
# 🤖 When you're done, ask your AI assistant:
#   - "Review my Pydantic model - are the Field descriptions clear enough
#      for an LLM to understand? Are the validator error messages helpful?"
# =============================================================================
