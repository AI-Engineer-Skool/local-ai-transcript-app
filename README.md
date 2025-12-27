# AI Transcript App

A base for your portfolio piece to land your next AI engineering job.
AI-powered voice transcription with Whisper and LLM cleaning. Browser-based recording interface with FastAPI backend.

**📺 Recommended Video Tutorial:** For project structure and API details, watch the full tutorial on YouTube: https://youtu.be/WUo5tKg2lnE

**Features:**

- 🎤 Browser-based voice recording
- 🔊 English Whisper speech-to-text (runs locally)
- 🤖 LLM cleaning (removes filler words, fixes errors)
- 🔌 **OpenAI API-compatible** (works with Ollama, LM Studio, OpenAI, or any OpenAI-compatible API)
- 📋 One-click copy to clipboard

Note that the vanilla version uses a smaller language model running on your CPU.
This means the AI may not listen to system prompts that well depending on the transcript.
The challenge for you is to change this portfolio app to advance the solution and make it your own.

For example:
- Modify it for a specific industry
- Add GPU acceleration + stronger local LLM
- Use a cloud AI model
- Real-time transcription/LLM streaming
- Multi-language support beyond English

**📚 Need help and want to learn more?**

Full courses on AI Engineering are available at [https://www.skool.com/ai-engineer](https://www.skool.com/ai-engineer)

---

## Quick Start

### 🚀 Dev Container (Recommended)

**This project is devcontainer-first. The easiest way to get started:**

#### 1. Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [VS Code](https://code.visualstudio.com/)
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

#### 2. Open in Dev Container

- Click **"Reopen in Container"** in VS Code
- Or: `Cmd/Ctrl+Shift+P` → **"Dev Containers: Reopen in Container"**
- Wait ~5-10 minutes for initial build and model download

VS Code automatically:

1. Builds and starts both containers (app + Ollama)
2. Installs Python and Node.js dependencies
3. Downloads the Ollama model
4. Creates `backend/.env` with working defaults

Skip to [Running the App](#running-the-app).

---

### ☁️ GitHub Codespaces (No Powerful PC Required)

**Don't have a powerful PC?** GitHub Codespaces provides cloud-based development environments that work with this project's devcontainer.

#### 1. Create a Codespace

- Go to the [repository on GitHub](https://github.com/AI-Engineer-Skool/local-ai-transcript-app)
- Click the green **"Code"** button → **"Codespaces"** tab → **"Create codespace on main"**
- The devcontainer enforces at least **8-core / 32GB RAM**.
- Wait ~5-10 minutes for initial setup

#### 2. Access the App

The devcontainer automatically configures everything. Once ready:

- Ports are auto-forwarded (you'll see notifications for ports 3000, 8000, 11434)
- Click the port 3000 link or go to the **"Ports"** tab to access the frontend

#### 3. For Localhost-Dependent Code

If you need true `localhost` access (some code expects `localhost:8000`):

1. Install the [GitHub Codespaces extension](https://marketplace.visualstudio.com/items?itemName=GitHub.codespaces) in VS Code Desktop
2. Connect to your running Codespace from VS Code Desktop
3. Ports will forward to your actual `localhost`

> **💡 Tip:** Stop your Codespace when not in use to conserve free hours. Go to [github.com/codespaces](https://github.com/codespaces) to manage active instances.

> **📺 Video Guide:** Watch the [GitHub Codespaces setup tutorial](https://youtu.be/KkV1O-rXntM) for a walkthrough.

> **🔄 Other Platforms:** Any cloud platform supporting devcontainers (Gitpod, DevPod, etc.) can also be used with this repository's `.devcontainer` configuration.

---

### 🛠️ Manual Installation

The devcontainer is the easiest supported setup method for beginners.
If you choose to install manually, you'll need:

- Python 3.12+, Node.js 24+, [uv](https://docs.astral.sh/uv/), and an LLM server ([Ollama](https://ollama.com/) or [LM Studio](https://lmstudio.ai/))
- Copy `backend/.env.example` to `backend/.env` and configure
- Install dependencies with `uv sync` (backend) and `npm install` (frontend)
- Start your LLM server and pull models: `ollama pull llama3.1:8b`

**For detailed setup, use the devcontainer above.**

---

## Running the App

Open **two terminals** and run:

**Terminal 1 - Backend:**

```bash
cd backend
uv run uvicorn app:app --reload --host 0.0.0.0 --port 8000 --timeout-keep-alive 600
```

> **Note:** `--timeout-keep-alive 600` sets a 10-minute timeout for long audio processing

**Terminal 2 - Frontend:**

```bash
cd frontend
npm run dev
```

**Browser:** Open `http://localhost:3000`

---

## Configuration

### OpenAI API Compatibility

**This app is compatible with any OpenAI API-format LLM provider:**

- **Ollama** (default - works out of the box in devcontainer)
- **LM Studio** (local alternative)
- **OpenAI API** (cloud-based)
- Any other OpenAI-compatible API

The devcontainer automatically creates `backend/.env` with working Ollama defaults. **No configuration needed to get started.**

To use a different provider, edit `backend/.env`:

- `LLM_BASE_URL` - API endpoint
- `LLM_API_KEY` - API key
- `LLM_MODEL` - Model name

---

## Troubleshooting

**Container won't start or is very slow:**

⚠️ **This app runs an LLM on CPU and requires adequate Docker resources.**

Configure Docker Desktop resources:

1. Open **Docker Desktop** → **Settings** → **Resources**
2. Set **CPUs** to maximum available (8+ cores recommended)
3. Set **Memory** to at least 16GB
4. Click **Apply & Restart**

**Expected specs:** Modern laptop/desktop with 8+ CPU cores and 16GB RAM. More CPU = faster LLM responses.

**Microphone not working:**

- Use Chrome or Firefox (Safari may have issues)
- Check browser permissions: Settings → Privacy → Microphone

**Backend fails to start:**

- Check Whisper model downloads: `~/.cache/huggingface/`
- Ensure enough disk space (models are ~150MB)

**LLM errors:**

- Make sure Ollama service is running (it auto-starts with devcontainer)
- Check model is downloaded: Model downloads automatically during devcontainer setup
- Transcription still works without LLM (raw Whisper only)

**LLM is slow:**

- See "Container won't start or is very slow" section above for Docker resource configuration
- **Fallback option:** Switch to another model (edit `LLM_MODEL` in `backend/.env`)
  - ⚠️ **Trade-off:** 3b is faster but **significantly worse at cleaning transcripts**
- **Best alternative:** Use a cloud API like OpenAI for instant responses with excellent quality (edit `.env`)

**Cannot access localhost:3000 or localhost:8000 from host machine:**

- **Docker Desktop:** Go to **Settings** → **Resources** → **Network**
- Enable **"Use host networking"** (may require Docker Desktop restart)
- Restart the frontend and backend servers

**Port already in use:**

- Backend: Change port with `--port 8001`
- Frontend: Edit `vite.config.js`, change `port: 3000`
