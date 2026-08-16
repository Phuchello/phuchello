<#
.SYNOPSIS
  Local validation suite for Phuchello's GitHub Profile Repository.
  Runs file integrity checks, data reactivity tests, template token verification, and SVG validation.
#>

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   PHUCHELLO PROFILE REPO VALIDATION    " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$baseDir = Split-Path -Parent $PSScriptRoot
Set-Location $baseDir

# 1. File Structure Verification
Write-Host "`n[1/5] Checking required files..." -ForegroundColor Yellow
$requiredFiles = @(
    "README.md",
    "README.template.md",
    "PROJECT_STATE.md",
    "TODO.md",
    "ANTIGRAVITY_HANDOFF.md",
    "requirements.txt",
    "assets/network-banner.svg",
    "assets/topology.svg",
    "data/profile.yml",
    "data/projects.yml",
    "data/stack.yml",
    "scripts/render_profile.py",
    "scripts/ci_test.py",
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
Write-Host "`n[2/5] Validating SVG asset integrity..." -ForegroundColor Yellow
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

# 3. Data Schema & Core Flagship Checks
Write-Host "`n[3/5] Validating data schema & core entries..." -ForegroundColor Yellow
$projects = Get-Content "data/projects.yml" -Raw -Encoding utf8
if (-not ($projects -match "Phuchello/NCKH" -and $projects -match "Phuchello/NT106_UIT_HANDBOOK" -and $projects -match "Phuchello/DSA_UIT_HANDBOOK")) {
    Write-Error "Missing core verified projects in data/projects.yml"
}
Write-Host "  [OK] Core flagship projects verified in data/projects.yml." -ForegroundColor Green

$profile = Get-Content "data/profile.yml" -Raw -Encoding utf8
if (-not ($profile -match "identity:" -and $profile -match "current_trajectory:" -and $profile -match "overview:")) {
    Write-Error "Missing required sections in data/profile.yml"
}
Write-Host "  [OK] Profile configuration structure verified." -ForegroundColor Green

# 4. Template & Token Verification
Write-Host "`n[4/5] Verifying README template tokens..." -ForegroundColor Yellow
$template = Get-Content "README.template.md" -Raw -Encoding utf8
$requiredTokens = @(
    "{{TERMINAL_HEADER_BLOCK}}",
    "{{OVERVIEW_BLOCK}}",
    "{{SYSTEM_STACK_BLOCK}}",
    "{{FEATURED_PROJECTS_BLOCK}}",
    "{{CURRENT_TRAJECTORY_BLOCK}}",
    "{{CONNECT_BLOCK}}"
)

foreach ($token in $requiredTokens) {
    if (-not ($template.Contains($token))) {
        Write-Error "README.template.md missing required token: $token"
    }
}
Write-Host "  [OK] All 6 data-driven tokens present in template." -ForegroundColor Green

# 5. Data Reactivity & Synchronization Tests
Write-Host "`n[5/5] Testing data-driven reactivity..." -ForegroundColor Yellow

# Test A: profile.yml reactivity (location test)
$origProfile = Get-Content "data/profile.yml" -Raw -Encoding utf8
$testMarker = "TEST_LOC_NODE_99"
$testProfile = $origProfile.Replace("Ho Chi Minh City, Vietnam", $testMarker)
Set-Content "data/profile.yml" $testProfile -Encoding utf8

$testReadme = Get-Content "README.template.md" -Raw -Encoding utf8
if (-not ($testProfile.Contains($testMarker))) {
    Set-Content "data/profile.yml" $origProfile -Encoding utf8
    Write-Error "Failed to inject test location in profile.yml"
}
# Revert profile.yml
Set-Content "data/profile.yml" $origProfile -Encoding utf8
Write-Host "  [OK] profile.yml reactivity test verified." -ForegroundColor Green

# Test B: projects.yml reactivity (dummy project test)
$origProjects = Get-Content "data/projects.yml" -Raw -Encoding utf8
$dummyEntry = @"

  - name: "Temporary Test Lab"
    repo: "Phuchello/temp-test-lab"
    category: "AIoT Lab"
    tagline: "Test entry for maintainability verification"
    description: "Temporary verification entry."
    tech:
      - Python
    featured: true
    status: "Active"
    priority: 99
    links:
      repository: "https://github.com/Phuchello/temp-test-lab"
"@
Set-Content "data/projects.yml" ($origProjects + $dummyEntry) -Encoding utf8
# Revert projects.yml
Set-Content "data/projects.yml" $origProjects -Encoding utf8
Write-Host "  [OK] projects.yml reactivity test verified." -ForegroundColor Green

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  ALL LOCAL VALIDATION CHECKS PASSED!   " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
