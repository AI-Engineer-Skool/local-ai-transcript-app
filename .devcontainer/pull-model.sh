#!/bin/bash
# Downloads the Ollama model the app uses, then checks that Ollama really has it.
# Runs automatically when the devcontainer is created. Safe to re-run any time:
#
#   bash .devcontainer/pull-model.sh              # default model (gemma3:4b)
#   bash .devcontainer/pull-model.sh llama3.1:8b  # any other Ollama model
#
# The name must match LLM_MODEL in backend/.env exactly.
set -u

OLLAMA_URL="${OLLAMA_URL:-http://ollama:11434}"
MODEL="${1:-gemma3:4b}"
MAX_ATTEMPTS=3

# Ollama matches the full name:tag, so pulling "gemma3" does NOT give you "gemma3:4b"
model_installed() {
    curl -s "$OLLAMA_URL/api/tags" | grep -qF "\"name\":\"$MODEL\""
}

fail() {
    echo ""
    echo "❌ Ollama model $MODEL is NOT installed: $1"
    echo "   LLM cleaning won't work until it is."
    echo "   Fix: bash .devcontainer/pull-model.sh $MODEL"
    echo ""
    exit 1
}

echo "⏳ Waiting for Ollama at $OLLAMA_URL..."
for i in {1..30}; do
    curl -s "$OLLAMA_URL/api/tags" > /dev/null 2>&1 && break
    [ "$i" -eq 30 ] && fail "Ollama is not responding at $OLLAMA_URL"
    sleep 1
done

if model_installed; then
    echo "✅ Model $MODEL is already installed"
    exit 0
fi

echo "🤖 Downloading Ollama model ($MODEL)..."
echo "   This may take 5-15 minutes on first setup..."
RESPONSE_FILE=$(mktemp)
trap 'rm -f "$RESPONSE_FILE"' EXIT

for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
    # With "stream": false Ollama answers once: {"status":"success"} or {"error":"..."}
    curl -sS -X POST "$OLLAMA_URL/api/pull" \
        -d "{\"model\":\"$MODEL\",\"stream\":false}" > "$RESPONSE_FILE" 2>&1 &
    PULL_PID=$!
    while kill -0 "$PULL_PID" 2>/dev/null; do
        echo -n "."
        sleep 2
    done
    echo ""

    # Trust what Ollama lists, not curl's exit code: a failed pull can still exit 0
    if model_installed; then
        echo "✅ Model $MODEL downloaded and verified!"
        exit 0
    fi
    echo "⚠️  Attempt $attempt/$MAX_ATTEMPTS failed: $(cat "$RESPONSE_FILE")"
    [ "$attempt" -lt "$MAX_ATTEMPTS" ] && sleep 5
done

fail "download failed $MAX_ATTEMPTS times (see the errors above)"
