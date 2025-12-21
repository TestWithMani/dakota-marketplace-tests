# Run pytest using the virtual environment's Python
Write-Host "Running tests with virtual environment..." -ForegroundColor Green

# Ensure reports directory exists
$reportsPath = Join-Path $PSScriptRoot "reports"
if (-not (Test-Path $reportsPath)) {
    New-Item -ItemType Directory -Path $reportsPath | Out-Null
}

# Ensure allure-results directory exists
$allureResultsPath = Join-Path $PSScriptRoot "allure-results"
if (-not (Test-Path $allureResultsPath)) {
    New-Item -ItemType Directory -Path $allureResultsPath | Out-Null
}

# Run pytest
.\venv\Scripts\python.exe -m pytest --html=reports/report.html --self-contained-html --alluredir=allure-results -v

# Check exit code
if ($LASTEXITCODE -eq 0) {
    Write-Host "`nTests completed successfully!" -ForegroundColor Green
} else {
    Write-Host "`nTests failed with exit code: $LASTEXITCODE" -ForegroundColor Red
    exit $LASTEXITCODE
}

