<#
.SYNOPSIS
  Local validation suite for Phuchello's GitHub Profile Repository.
  Runs file integrity checks, template token verification, and SVG validation.
#>

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   PHUCHELLO PROFILE REPO VALIDATION    " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$baseDir = Split-Path -Parent $PSScriptRoot
Set-Location $baseDir

# 1. File Structure Verification
Write-Host "`n[1/4] Checking required files..." -ForegroundColor Yellow
$requiredFiles = @(
    "README.md",
    "README.template.md",
    "PROJECT_STATE.md",
    "TODO.md",
    "assets/network-banner.svg",
    "assets/topology.svg",
    "data/profile.yml",
    "data/projects.yml",
    "data/stack.yml",
    "scripts/render_profile.py",
    ".github/workflows/profile-check.yml"
)

foreach ($f in $requiredFiles) {
    if (Test-Path $f) {
        Write-Host "  [OK] $f" -ForegroundColor Green
    } else {
        Write-Error "Missing required file: $f"
    }
}

# 2. SVG Asset Validation
Write-Host "`n[2/4] Validating SVG asset integrity..." -ForegroundColor Yellow
foreach ($svg in @("assets/network-banner.svg", "assets/topology.svg")) {
    $content = Get-Content $svg -Raw -Encoding utf8
    if (-not ($content -match "<svg" -and $content -match "viewBox=" -and $content -match "</svg>")) {
        Write-Error "Malformed SVG file: $svg"
    }
    if ($content -match "<script" -or $content -match "javascript:") {
        Write-Error "Security violation: Embedded script found in $svg"
    }
    Write-Host "  [OK] $svg (Valid vector structure, no embedded scripts)" -ForegroundColor Green
}

# 3. Data Schema & YAML Content Checks
Write-Host "`n[3/4] Validating data integrity..." -ForegroundColor Yellow
$projects = Get-Content "data/projects.yml" -Raw -Encoding utf8
if (-not ($projects -match "Phuchello/NCKH" -and $projects -match "Phuchello/NT106_UIT_HANDBOOK" -and $projects -match "Phuchello/DSA_UIT_HANDBOOK")) {
    Write-Error "Missing core verified projects in data/projects.yml"
}
Write-Host "  [OK] Core flagship projects verified." -ForegroundColor Green

$stack = Get-Content "data/stack.yml" -Raw -Encoding utf8
if (-not ($stack -match "NETWORKING" -and $stack -match "EDGE & AIoT" -and $stack -match "INTELLIGENCE & RESEARCH")) {
    Write-Error "Missing required system layers in data/stack.yml"
}
Write-Host "  [OK] System layers configuration verified." -ForegroundColor Green

# 4. Template & README Synchronization Check
Write-Host "`n[4/4] Verifying README template tokens..." -ForegroundColor Yellow
$template = Get-Content "README.template.md" -Raw -Encoding utf8
if (-not ($template -match "\{\{SYSTEM_STACK_BLOCK\}\}" -and $template -match "\{\{FEATURED_PROJECTS_BLOCK\}\}")) {
    Write-Error "README.template.md missing required replacement tokens"
}
Write-Host "  [OK] Template tokens verified." -ForegroundColor Green

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  ALL LOCAL VALIDATION CHECKS PASSED!   " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
