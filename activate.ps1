# PowerShell script to activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"
Write-Host "Virtual environment activated!" -ForegroundColor Green
Write-Host "Python: $(python --version)" -ForegroundColor Cyan
Write-Host "Pip: $(pip --version)" -ForegroundColor Cyan

