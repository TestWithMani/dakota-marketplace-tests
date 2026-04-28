param(
    [switch]$IncludeVenv
)

$ErrorActionPreference = "Stop"

$paths = @(
    ".pytest_cache",
    "__pycache__",
    "reports",
    "allure-results",
    "allure-report"
)

if ($IncludeVenv) {
    $paths += "venv"
}

foreach ($path in $paths) {
    if (Test-Path $path) {
        Write-Host "Removing $path"
        Remove-Item -Path $path -Recurse -Force -ErrorAction SilentlyContinue
    } else {
        Write-Host "Skipping $path (not found)"
    }
}

Write-Host "Cleanup complete."
