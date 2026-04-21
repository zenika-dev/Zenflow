#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ScriptDir  = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot   = Split-Path -Parent $ScriptDir

$AgentsSrcDir       = Join-Path $RepoRoot '.github' 'agents'
$InstructionsSrcDir = Join-Path $RepoRoot '.github' 'instructions'
$TemplatesDir       = Join-Path $RepoRoot 'templates' 'guidelines'

if (-not (Test-Path $AgentsSrcDir -PathType Container)) {
    Write-Error "Error: missing agents source directory: $AgentsSrcDir"
    exit 1
}

if (-not (Test-Path $InstructionsSrcDir -PathType Container)) {
    Write-Error "Error: missing instructions source directory: $InstructionsSrcDir"
    exit 1
}

if (-not (Test-Path $TemplatesDir -PathType Container)) {
    Write-Error "Error: missing templates source directory: $TemplatesDir"
    exit 1
}

$DefaultTargetPath = Join-Path $RepoRoot 'target'
$TargetPathInput = Read-Host "Target path [$DefaultTargetPath]"
if ([string]::IsNullOrWhiteSpace($TargetPathInput)) {
    $TargetPath = $DefaultTargetPath
} else {
    $TargetPath = $TargetPathInput
}

Write-Host "Zenflow initialization"
Write-Host "The following will be generated inside the target folder ($TargetPath):"
Write-Host "  - .github/agents/        (agent definitions)"
Write-Host "  - .github/instructions/  (instruction files)"
Write-Host "  - .github/guidelines/    (architecture, review, and conventions templates)"
Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

$TargetGithubDir      = Join-Path $TargetPath '.github'
$TargetAgentsDir      = Join-Path $TargetGithubDir 'agents'
$TargetInstructionsDir = Join-Path $TargetGithubDir 'instructions'
$TargetGuidelinesDir  = Join-Path $TargetGithubDir 'guidelines'

New-Item -ItemType Directory -Force -Path $TargetAgentsDir       | Out-Null
New-Item -ItemType Directory -Force -Path $TargetInstructionsDir | Out-Null
New-Item -ItemType Directory -Force -Path $TargetGuidelinesDir   | Out-Null

function Choose-BackendStack {
    Write-Host ""
    Write-Host "Choose backend stack:"
    Write-Host "  1) java-spring-boot"
    Write-Host "  2) golang-gin"
    Write-Host "  3) python-fastapi"
    $choice = Read-Host "Enter choice [1-3]"

    switch ($choice) {
        '1' { return 'java-spring-boot.md' }
        '2' { return 'golang-gin.md' }
        '3' { return 'python-fastapi.md' }
        default {
            Write-Error "Error: invalid backend choice '$choice'."
            exit 1
        }
    }
}

function Choose-FrontendStack {
    Write-Host ""
    Write-Host "Choose frontend stack:"
    Write-Host "  1) react-typescript"
    Write-Host "  2) nextjs-app-router"
    $choice = Read-Host "Enter choice [1-2]"

    switch ($choice) {
        '1' { return 'react-typescript.md' }
        '2' { return 'nextjs-app-router.md' }
        default {
            Write-Error "Error: invalid frontend choice '$choice'."
            exit 1
        }
    }
}

function Copy-RequiredFile {
    param(
        [string]$Src,
        [string]$Dst
    )
    if (-not (Test-Path $Src -PathType Leaf)) {
        Write-Error "Error: source file not found: $Src"
        exit 1
    }
    Copy-Item $Src $Dst
}

$BackendArchFile  = Choose-BackendStack
$FrontendArchFile = Choose-FrontendStack

Write-Host ""
$includeConventions = Read-Host "Include git conventions template as .github/guidelines/conventions.md? [Y/n]"
if ([string]::IsNullOrWhiteSpace($includeConventions)) {
    $includeConventions = 'Y'
}

Write-Host ""
Write-Host "Copying agents..."
Copy-Item (Join-Path $AgentsSrcDir '*.md') $TargetAgentsDir

Write-Host "Copying instructions..."
Copy-Item (Join-Path $InstructionsSrcDir '*.md') $TargetInstructionsDir

Write-Host "Copying selected guideline templates..."
Copy-RequiredFile (Join-Path $TemplatesDir 'backend'  $BackendArchFile)  (Join-Path $TargetGuidelinesDir 'architecture-backend.md')
Copy-RequiredFile (Join-Path $TemplatesDir 'frontend' $FrontendArchFile) (Join-Path $TargetGuidelinesDir 'architecture-frontend.md')
Copy-RequiredFile (Join-Path $TemplatesDir 'review'   'backend.md')      (Join-Path $TargetGuidelinesDir 'review-backend.md')
Copy-RequiredFile (Join-Path $TemplatesDir 'review'   'frontend.md')     (Join-Path $TargetGuidelinesDir 'review-frontend.md')

switch ($includeConventions) {
    { $_ -in 'Y','y' } {
        Copy-RequiredFile (Join-Path $TemplatesDir 'git-conventions' 'default.md') (Join-Path $TargetGuidelinesDir 'conventions.md')
        $ConventionsMsg = "Included conventions.md"
    }
    { $_ -in 'N','n' } {
        $ConventionsMsg = "Skipped conventions.md"
    }
    default {
        Write-Error "Error: invalid conventions choice '$includeConventions'. Use Y or n."
        exit 1
    }
}

Write-Host ""
Write-Host "Initialization complete."
Write-Host "Target: $TargetPath"
Write-Host "- Copied agents to $TargetAgentsDir"
Write-Host "- Copied instructions to $TargetInstructionsDir"
Write-Host "- Copied architecture/review guidelines to $TargetGuidelinesDir"
Write-Host "- $ConventionsMsg"
