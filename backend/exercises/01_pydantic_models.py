"""
Exercise 1: Pydantic Models for Tool Inputs

Concept: Pydantic models with Field descriptions are the foundation for PydanticAI
tool inputs. The LLM uses field descriptions to understand what data to extract.

Difficulty: Beginner

Run: uv run python exercises/01_pydantic_models.py
"""

from typing import Literal

from pydantic import BaseModel, Field, ValidationError

# =============================================================================
# WORKING BASE CODE
# =============================================================================


class TaskItem(BaseModel):
    """A single task extracted from a meeting transcript.

    In PydanticAI, this model would be used as a tool input parameter.
    The Field descriptions tell the LLM what each field should contain.
    """

    task: str = Field(description="The action item or task to be done")
    owner: str = Field(description="Person responsible for this task")
    priority: Literal["high", "medium", "low"] = Field(
        default="medium", description="Priority level of the task"
    )


def demo_basic_model():
    """Demonstrate basic Pydantic model usage."""
    print("=" * 60)
    print("DEMO: Basic Pydantic Model")
    print("=" * 60)

    # Create a valid task
    task1 = TaskItem(
        task="Review the API design document",
        owner="Alice",
        priority="high",
    )
    print(f"\nValid task: {task1}")
    print(f"  task: {task1.task}")
    print(f"  owner: {task1.owner}")
    print(f"  priority: {task1.priority}")

    # Default priority
    task2 = TaskItem(task="Update documentation", owner="Bob")
    print(f"\nWith default priority: {task2}")

    # See the JSON schema (this is what PydanticAI sends to the LLM)
    print("\nJSON Schema (sent to LLM):")
    import json

    print(json.dumps(TaskItem.model_json_schema(), indent=2))


def demo_validation():
    """Demonstrate Pydantic validation."""
    print("\n" + "=" * 60)
    print("DEMO: Validation")
    print("=" * 60)

    # Invalid priority triggers validation error
    try:
        TaskItem(task="Test", owner="Charlie", priority="urgent")  # type: ignore
    except ValidationError as e:
        print("\nValidation error for invalid priority:")
        print(f"  {e.errors()[0]['msg']}")

    # Missing required field
    try:
        TaskItem(task="Test")  # type: ignore  # Missing 'owner'
    except ValidationError as e:
        print("\nValidation error for missing field:")
        print(f"  {e.errors()[0]['msg']}")


def demo_literal_types():
    """Demonstrate Literal types for constrained choices."""
    print("\n" + "=" * 60)
    print("DEMO: Literal Types")
    print("=" * 60)

    # Literal types give the LLM a fixed set of choices
    print("\nLiteral['high', 'medium', 'low'] constrains priority to these values.")
    print("The LLM sees this in the JSON schema and picks from valid options.")

    # Show how Literal appears in the schema
    schema = TaskItem.model_json_schema()
    priority_schema = schema["properties"]["priority"]
    print(f"\nPriority schema: {priority_schema}")


if __name__ == "__main__":
    demo_basic_model()
    demo_validation()
    demo_literal_types()

    print("\n" + "=" * 60)
    print("BASE CODE COMPLETE - Try the challenges below!")
    print("=" * 60)


# =============================================================================
# CHALLENGES
# =============================================================================

# -----------------------------------------------------------------------------
# Challenge 1: Add a due_date field with validation
# -----------------------------------------------------------------------------
# Add a `due_date` field to TaskItem that:
# - Is optional (can be None)
# - When provided, must be in YYYY-MM-DD format
# - Has a helpful description for the LLM
#
# Hint: Use `field_validator` from pydantic to validate the format
#
# Example:
#   from pydantic import field_validator
#   import re
#
#   @field_validator("due_date")
#   @classmethod
#   def validate_date_format(cls, v):
#       if v is not None and not re.match(r"^\d{4}-\d{2}-\d{2}$", v):
#           raise ValueError("due_date must be in YYYY-MM-DD format")
#       return v

# -----------------------------------------------------------------------------
# Challenge 2: Create a MeetingNote model with nested TaskItem list
# -----------------------------------------------------------------------------
# Create a `MeetingNote` model that contains:
# - meeting_title: str
# - meeting_date: str (YYYY-MM-DD format)
# - attendees: list[str]
# - tasks: list[TaskItem]  (nested!)
# - summary: str
#
# Hint: Pydantic handles nested models automatically
#
# Example usage:
#   note = MeetingNote(
#       meeting_title="Sprint Planning",
#       meeting_date="2024-12-09",
#       attendees=["Alice", "Bob"],
#       tasks=[
#           TaskItem(task="Design API", owner="Alice", priority="high"),
#           TaskItem(task="Write tests", owner="Bob"),
#       ],
#       summary="Planned Q1 deliverables",
#   )

# -----------------------------------------------------------------------------
# Challenge 3: Add a custom validator for priority escalation
# -----------------------------------------------------------------------------
# Add a `model_validator` that automatically escalates priority to "high"
# if the task description contains words like "urgent", "asap", or "critical".
#
# Hint: Use `model_validator(mode="after")` to run after all fields are set
#
# Example:
#   from pydantic import model_validator
#
#   @model_validator(mode="after")
#   def escalate_urgent_tasks(self):
#       urgent_keywords = ["urgent", "asap", "critical", "immediately"]
#       if any(kw in self.task.lower() for kw in urgent_keywords):
#           self.priority = "high"
#       return self
