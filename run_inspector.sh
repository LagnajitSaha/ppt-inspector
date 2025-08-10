#!/bin/bash

# PowerPoint Inspector - Unix/Linux/macOS Shell Script
# This file makes it easy to run the PowerPoint Inspector tool on Unix-like systems

echo
echo "========================================"
echo "    PowerPoint Inspector Tool"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERROR: Python is not installed or not in PATH"
        echo "Please install Python 3.8+ and try again"
        echo
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo "ERROR: Python 3.8+ is required. Found version $PYTHON_VERSION"
    echo "Please upgrade Python and try again"
    echo
    exit 1
fi

echo "Using Python: $($PYTHON_CMD --version)"

# Check if virtual environment exists
if [ -f "venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "No virtual environment found. Creating one..."
    $PYTHON_CMD -m venv venv
    source venv/bin/activate
    
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo
    echo "WARNING: .env file not found!"
    echo "Please create a .env file with your GEMINI_API_KEY"
    echo "You can copy .env.example and fill in your API key"
    echo
    echo "Example .env file content:"
    echo "GEMINI_API_KEY=your_api_key_here"
    echo
fi

echo
echo "Running PowerPoint Inspector..."
echo

# Run the tool with all arguments passed to this script
$PYTHON_CMD ppt_inspector.py "$@"

echo
echo "Tool execution completed."
echo
