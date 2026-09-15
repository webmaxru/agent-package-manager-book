#!/usr/bin/env pwsh
# Launches the APM book agent fleet autonomously (headless).
# Runs the master orchestrator prompt to completion via Copilot CLI, then exits.
#
# Usage:
#   .\scripts\run-fleet.ps1                  # run the full pipeline
#   .\scripts\run-fleet.ps1 -UpdateBook       # update the existing book
#   .\scripts\run-fleet.ps1 -UpdateBook -DryRun
#
# Notes:
#   - Run from the repo root (the script cd's there itself).
#   - --allow-all-tools grants Copilot the same access you have. For isolation,
#     run inside a sandbox/container, or use `copilot --cloud`.

[CmdletBinding(DefaultParameterSetName = "Prompt")]
param(
    [switch]$DryRun,
    [Parameter(ParameterSetName = "Prompt")]
    [string]$PromptPath = ".github\prompts\run-playbook.prompt.md",
    [Parameter(Mandatory, ParameterSetName = "Update")]
    [switch]$UpdateBook,
    [Parameter(ParameterSetName = "Update")]
    [ValidatePattern('^v?(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$')]
    [string]$ApmVersion,
    [Parameter(ParameterSetName = "Update")]
    [switch]$CheckOnly
)

$ErrorActionPreference = "Stop"

# Move to repo root (parent of this script's folder)
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

if ($UpdateBook) {
    $PromptPath = ".github\prompts\update-book.prompt.md"
}

if (-not (Test-Path -LiteralPath $PromptPath -PathType Leaf)) {
    throw "Orchestrator prompt not found: $PromptPath"
}

$prompt = Get-Content -LiteralPath $PromptPath -Raw
if ($UpdateBook) {
    $mode = if ($CheckOnly) { "check" } else { "prepare" }
    $target = if ($ApmVersion) { $ApmVersion.TrimStart('v') } else { "latest stable at discovery" }
    $prompt += "`n`nInvocation inputs:`nMode: $mode`nTarget APM: $target`nNever push, tag, merge, or publish in this run."
}

if ($DryRun) {
    Write-Host "[DryRun] Prompt: $PromptPath"
    if ($UpdateBook) {
        Write-Host "[DryRun] Mode: $mode; target APM: $target; publication: disabled"
    }
    Write-Host "[DryRun] Would run: copilot -p <orchestrator-prompt> --allow-all-tools" -ForegroundColor Yellow
    return
}

if (-not (Get-Command copilot -ErrorAction SilentlyContinue)) {
    throw "Copilot CLI ('copilot') not found on PATH. Install it first: https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-cli"
}

Write-Host "Launching APM book fleet from '$PromptPath'..." -ForegroundColor Cyan

# Headless run: orchestrator drives the whole fleet and exits when done.
copilot -p $prompt --allow-all-tools
exit $LASTEXITCODE
