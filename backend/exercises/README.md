# PydanticAI Practice Exercises

Learn PydanticAI concepts progressively before extending the main transcript processing agent.

## Quick Start

```bash
cd backend
uv run python exercises/01_pydantic_models.py
```

## Exercise Overview

| #   | File                    | Concept                                 | Difficulty   |
| --- | ----------------------- | --------------------------------------- | ------------ |
| 1   | `01_pydantic_models.py` | Pydantic models with Field descriptions | Beginner     |
| 2   | `02_basic_agent.py`     | Creating and running a PydanticAI agent | Beginner     |
| 3   | `03_tools_simple.py`    | Adding tools with `@agent.tool_plain`   | Intermediate |
| 4   | `04_dependencies.py`    | Dependency injection with `RunContext`  | Intermediate |
| 5   | `05_full_pattern.py`    | Full pattern with Pydantic tool inputs  | Advanced     |

## How Each Exercise Works

Each file contains:

1. **Working base code** - Complete, runnable example demonstrating the concept
2. **3 Challenges** - Progressive tasks to extend and deepen understanding

Run the base code first to see it work, then tackle the challenges.

## Concept Map

```
Exercise 1: Pydantic Models
    └── Foundation: Field(), Literal, validation
           │
           ▼
Exercise 2: Basic Agent
    └── Agent(), instructions, run_sync()
           │
           ▼
Exercise 3: Simple Tools
    └── @agent.tool_plain, tool returns strings
           │
           ▼
Exercise 4: Dependencies
    └── @dataclass deps, RunContext[Deps], @agent.instructions
           │
           ▼
Exercise 5: Full Pattern
    └── Pydantic models as tool inputs (mirrors agent.py)
```

## No API Key Required

All exercises use `TestModel` from PydanticAI - a mock model that:

- Requires no API key
- Runs instantly (no network calls)
- Produces deterministic results
- Perfect for learning patterns

## Connecting to the Main Codebase

After completing these exercises, you'll understand the patterns in:

- `backend/agent.py` - The main PydanticAI agent
- `backend/models.py` - Pydantic models for tool inputs

The exercises mirror these files so the transition is smooth.
