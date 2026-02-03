#!/bin/bash
# Bash script to run the backend server (for Mac/Linux)

echo "Starting ClipTheNews Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run server
echo "Starting FastAPI server on http://localhost:8000"
uvicorn main:app --reload --port 8000
