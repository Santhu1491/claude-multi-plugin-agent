#!/bin/bash

# Run Python plugin

set -e

echo "Starting Python Plugin..."

cd plugins/python-plugin

# Activate virtual environment if it exists
if [ -d "../../.venv" ]; then
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source ../../.venv/Scripts/activate
    else
        source ../../.venv/bin/activate
    fi
fi

# Run the plugin
python -m python_plugin.main "$@"
