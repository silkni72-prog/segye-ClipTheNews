# PowerShell script to run the backend server
Write-Host "Starting ClipTheNews Backend..." -ForegroundColor Green

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Run server
Write-Host "Starting FastAPI server on http://localhost:8000" -ForegroundColor Green
uvicorn main:app --reload --port 8000
