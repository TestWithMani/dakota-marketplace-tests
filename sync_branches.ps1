param(
    [string]$SourceBranch = "master",
    [string]$TargetBranch = "main",
    [switch]$Push
)

$ErrorActionPreference = "Stop"

function Exec-Git {
    param([string]$Command)
    Write-Host "git $Command"
    & git $Command.Split(" ")
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed: git $Command"
    }
}

Write-Host "Syncing '$TargetBranch' from '$SourceBranch'..."

Exec-Git "fetch --all --prune"
Exec-Git "checkout $SourceBranch"
Exec-Git "pull origin $SourceBranch"
Exec-Git "checkout $TargetBranch"
Exec-Git "merge --ff-only $SourceBranch"

if ($Push) {
    Exec-Git "push origin $TargetBranch"
    Write-Host "Pushed '$TargetBranch' to origin."
} else {
    Write-Host "Local sync complete. Use -Push to push to origin."
}

Write-Host "Done."
