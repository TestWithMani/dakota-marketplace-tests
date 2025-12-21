# Setup script for new environment
Write-Host "Setting up Dakota MP test project..." -ForegroundColor Cyan

# Check if venv exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
} else {
    Write-Host "Virtual environment already exists." -ForegroundColor Green
}

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
.\venv\Scripts\python.exe -m pip install --upgrade pip

# Install dependencies
Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Yellow
.\venv\Scripts\python.exe -m pip install -r requirements.txt

Write-Host "`nSetup complete!" -ForegroundColor Green
Write-Host "To activate the virtual environment, run: .\activate.ps1" -ForegroundColor Cyan
Write-Host "To run tests, use: .\run_tests.ps1" -ForegroundColor Cyan

