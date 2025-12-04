#!/bin/bash
# ExtendOPS Environment Setup
# Usage: source setup_env.sh

# Ensure we are in the project root
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$PROJECT_ROOT"

# Check for venv
if [ ! -d "venv_daily" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv_daily
fi

# Activate venv
source venv_daily/bin/activate

# Install dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "⚠️ requirements.txt not found!"
fi

# Set PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

echo "✅ ExtendOPS Environment Ready"
echo "📂 Core: $PROJECT_ROOT/core"
echo "🐍 Python: $(which python)"
