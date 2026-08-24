#!/bin/bash

# Run the multi-plugin agent

set -e

echo "Starting Claude Multi-Plugin Agent..."

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source .venv/Scripts/activate
    else
        source .venv/bin/activate
    fi
else
    echo "Warning: Virtual environment not found. Run scripts/setup.sh first."
    exit 1
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Please create it from .env.example"
    exit 1
fi

# Run the agent
python agent/main.py "$@"
