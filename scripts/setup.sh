#!/bin/bash

# Setup script for Claude Multi-Plugin Agent

set -e

echo "Setting up Claude Multi-Plugin Agent..."

# Check Python version
echo "Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Check Java version
echo "Checking Java version..."
java_version=$(java -version 2>&1 | head -n 1 | awk -F '"' '{print $2}')
echo "Java version: $java_version"

# Check Maven
echo "Checking Maven..."
mvn_version=$(mvn -version 2>&1 | head -n 1 | awk '{print $3}')
echo "Maven version: $mvn_version"

# Create virtual environment
echo "Creating Python virtual environment..."
python -m venv .venv

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -e ".[dev]"

# Install Python plugin
echo "Installing Python plugin..."
cd plugins/python-plugin
pip install -e ".[dev]"
cd ../..

# Build Java plugin
echo "Building Java plugin..."
cd plugins/java-plugin
mvn clean install
cd ../..

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please update .env with your ANTHROPIC_API_KEY"
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env with your API key"
echo "2. Activate the virtual environment:"
echo "   - Windows: .venv\\Scripts\\activate"
echo "   - Unix/Mac: source .venv/bin/activate"
echo "3. Run the agent: python agent/main.py"
