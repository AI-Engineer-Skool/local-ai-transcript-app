#!/bin/bash
set -e

echo "🚀 Setting up AI Transcript App development environment..."

# Ensure cache directories exist with proper permissions
mkdir -p "$HOME/.cache/uv" "$HOME/.cache/huggingface"

# Create .env from example if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "📝 Creating backend/.env from backend/.env.example..."
    cp backend/.env.example backend/.env
    echo "✅ backend/.env created"
fi

echo "🐍 Installing Python dependencies with uv..."
cd backend
uv sync
cd ..
echo "✅ Python dependencies installed"

echo "📦 Installing frontend dependencies with npm..."
cd frontend
npm install
cd ..
echo "✅ Frontend dependencies installed"

echo "🔧 Installing TypeScript globally..."
sudo npm install -g typescript@5.9.3
echo "✅ TypeScript installed globally"

# Download the Ollama model and verify it arrived. A failure must not abort the
# rest of setup, so remember it and repeat the warning at the very end.
MODEL_READY=true
bash .devcontainer/pull-model.sh || MODEL_READY=false

echo ""
echo "📋 Installed versions:"
echo "  Python: $(python --version)"
echo "  Node.js: $(node --version)"
echo "  npm: $(npm --version)"
echo "  TypeScript: $(tsc --version)"
echo "  uv: $(uv --version)"
echo "  Ollama: Running as Docker service at http://ollama:11434"

echo ""
echo "✨ Development environment ready!"
echo ""
echo "📖 To start the app, open TWO terminals:"
echo ""
echo "  Terminal 1:  cd backend && uv run uvicorn app:app --reload --host 0.0.0.0 --port 8000"
echo "  Terminal 2:  cd frontend && npm run dev"
echo "  Browser:     http://localhost:3000"
echo ""

if [ "$MODEL_READY" = false ]; then
    echo "⚠️  The Ollama model is missing, so LLM cleaning won't work yet."
    echo "   Fix: bash .devcontainer/pull-model.sh"
    echo ""
fi
