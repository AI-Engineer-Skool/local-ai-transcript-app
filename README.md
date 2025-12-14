# AI Engineer Fundamentals - Exercise Generator

> **📍 You are on branch `checkpoint-1-fundamentals`**
>
> This branch contains an **AI-powered exercise generation system** for learning Python and TypeScript fundamentals. Run the student quiz to create your profile, then use the exercise generator prompt with an AI agent to generate personalized coding exercises based on your interests.
>
> **📚 This checkpoint is covered in detail in the [Classroom](https://aiengineer.community/join).**

---

## Branches

This repository uses checkpoint branches to progressively teach AI engineering concepts:

| Branch | Description | Builds On | Learning Resource |
|--------|-------------|-----------|-------------------|
| `main` | Complete transcript app with Whisper + LLM cleaning (runs fully locally, beginner friendly) | — | [YouTube Tutorial](https://youtu.be/WUo5tKg2lnE) |
| `checkpoint-1-fundamentals` | Exercise generation system for learning Python/TypeScript fundamentals | — | [Classroom](https://aiengineer.community/join) |
| `checkpoint-agentic-openrouter` | Agentic workflow with autonomous tool selection | `main` | [Classroom](https://aiengineer.community/join) |
| `checkpoint-pydanticai-openrouter` | PydanticAI framework for structured agent development | `checkpoint-agentic-openrouter` | [Classroom](https://aiengineer.community/join) |
| `checkpoint-rest-mcp-openrouter` | MCP integration with REST API and GitHub Issues | `checkpoint-pydanticai-openrouter` | [Classroom](https://aiengineer.community/join) |

> **Why "openrouter" in branch names?** These branches use [OpenRouter](https://openrouter.ai/) to access powerful cloud models that reliably support tool/function calling. Small local models struggle with agentic workflows.

Switch branches with: `git checkout <branch-name>`

---

## What's in This Branch?

This branch provides an AI-assisted learning system for programming fundamentals:

- **`exercise/student_quiz.py`** - Interactive quiz to create your learning profile
- **`exercise/EXERCISE_GENERATOR.md`** - Prompt for AI agents to generate personalized exercises
- **`exercise/python/`** - Directory for generated Python exercises
- **`exercise/typescript/`** - Directory for generated TypeScript exercises

## Quick Start

### 1. Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [VS Code](https://code.visualstudio.com/)
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### 2. Open in Dev Container

- Click **"Reopen in Container"** in VS Code
- Or: `Cmd/Ctrl+Shift+P` → **"Dev Containers: Reopen in Container"**

### 3. Create Your Student Profile

Run the student quiz to generate your personalized learning profile:

```bash
uv run exercise/student_quiz.py
```

This creates `exercise/STUDENT_PROFILE.md` with your:
- Programming background
- Skill level
- Interest theme (fitness, music, gaming, etc.)
- Learning style preferences

### 4. Generate Personalized Exercises

Open `exercise/EXERCISE_GENERATOR.md` with an AI agent (like Claude Code) and ask it to generate exercises based on your profile. The AI will create themed exercises in both Python and TypeScript.

### 5. Complete the Exercises

Work through the generated exercises:

```bash
# Run Python exercises
uv run exercise/python/01_*.py

# Run TypeScript exercises
npx tsx exercise/typescript/01_*.ts
```

---

## How It Works

1. **Student Quiz** → Captures your interests, skill level, and learning preferences
2. **AI Generator** → Reads your profile and creates themed exercises
3. **Personalized Learning** → Exercises use examples from YOUR interests (gym, music, gaming, etc.)
4. **Dual Language** → Learn both Python and TypeScript with the same concepts

---

**📚 Need help and want to learn more?**

Full courses on AI Engineering are available at [https://aiengineer.community/join](https://aiengineer.community/join)
