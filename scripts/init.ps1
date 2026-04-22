#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ScriptDir  = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot   = Split-Path -Parent $ScriptDir

function Show-Help {
    $scriptName = Split-Path -Leaf $MyInvocation.MyCommand.Path
    Write-Host "Usage: $scriptName [--help|-h]"
    Write-Host ""
    Write-Host "Initializes Zenflow target scaffolding by copying:"
    Write-Host "  - .github/agents"
    Write-Host "  - .github/instructions"
    Write-Host "  - selected templates under .github/guidelines"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -h, --help    Show this help message and exit"
}

foreach ($arg in $args) {
    switch ($arg) {
        '-h' {
            Show-Help
            exit 0
        }
        '--help' {
            Show-Help
            exit 0
        }
        default {
            Write-Error "Error: unknown argument '$arg'. Use --help for usage."
            exit 1
        }
    }
}

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

# Optional add-on tools (Copilot/VS Code is always deployed)
$opencodeInput = Read-Host "Also set up OpenCode? [Y/N]"
$DeployOpenCode = $opencodeInput -match '^[Yy]$'

$claudeInput = Read-Host "Also set up Claude Code? [Y/N]"
$DeployClaude = $claudeInput -match '^[Yy]$'

Write-Host "Zenflow initialization"
Write-Host "Target path: $TargetPath"
Write-Host "Tools:"
Write-Host "  ✓ GitHub Copilot (VS Code) — always installed"
if ($DeployOpenCode) { Write-Host "  ✓ OpenCode" }
if ($DeployClaude) { Write-Host "  ✓ Claude Code" }
Write-Host ""
Write-Host "The following will be generated:"
Write-Host "  - .github/agents/        (agent definitions)"
Write-Host "  - .github/instructions/  (instruction files)"
Write-Host "  - .github/guidelines/    (architecture, review, and conventions)"
if ($DeployOpenCode) { Write-Host "  - .opencode/skills/      (OpenCode skill definitions)" }
if ($DeployClaude) { Write-Host "  - .claude/skills/        (Claude Code skill definitions)" }
Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

$TargetGithubDir      = Join-Path $TargetPath '.github'
$TargetAgentsDir      = Join-Path $TargetGithubDir 'agents'
$TargetInstructionsDir = Join-Path $TargetGithubDir 'instructions'
$TargetGuidelinesDir  = Join-Path $TargetGithubDir 'guidelines'

# Always create .github directories (Copilot/VS Code is always deployed)
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

function Copy-AgentsAsSkills {
    param(
        [string]$TargetDir
    )

    New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null

    Get-ChildItem (Join-Path $AgentsSrcDir '*.md') | ForEach-Object {
        $agentName = $_.BaseName -replace '\.agent', ''
        $skillDir = Join-Path $TargetDir $agentName
        New-Item -ItemType Directory -Force -Path $skillDir | Out-Null
        Copy-Item $_.FullName (Join-Path $skillDir 'SKILL.md')
    }
}

# 3. Stack choices
$BackendArchFile  = Choose-BackendStack
$FrontendArchFile = Choose-FrontendStack

Write-Host ""
$includeConventions = Read-Host "Include git conventions template as .github/guidelines/conventions.md? [Y/N]"
if ([string]::IsNullOrWhiteSpace($includeConventions)) {
    $includeConventions = 'Y'
}

Write-Host ""

# Deploy Copilot/VS Code (always)
Write-Host "Deploying GitHub Copilot (VS Code) setup..."
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
    { $_ -in 'Y','y','' } {
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

# Deploy OpenCode
if ($DeployOpenCode) {
    Write-Host "Deploying OpenCode setup..."
    $TargetOpenCodeDir = Join-Path $TargetPath '.opencode' 'skills'

    # Create OpenCode skills from agent templates
    Copy-AgentsAsSkills $TargetOpenCodeDir
    Write-Host "Copied skills to $TargetOpenCodeDir"

    # Copy AGENTS.md from template to target
    $AgentsTemplate = Join-Path $RepoRoot 'templates' 'AGENTS.md'
    $AgentsTarget = Join-Path $TargetPath 'AGENTS.md'
    if (Test-Path $AgentsTemplate) {
        Copy-Item $AgentsTemplate $AgentsTarget
        Write-Host "Copied AGENTS.md to $TargetPath"
    }
    else {
        Write-Warning "Warning: AGENTS.md template not found at $AgentsTemplate"
    }
}

# Deploy Claude Code
if ($DeployClaude) {
    Write-Host "Deploying Claude Code setup..."
    $TargetClaudeDir = Join-Path $TargetPath '.claude' 'skills'

    # Create Claude skills from agent templates
    Copy-AgentsAsSkills $TargetClaudeDir
    Write-Host "Copied skills to $TargetClaudeDir"

    # Copy CLAUDE.md from template to target
    $ClaudeTemplate = Join-Path $RepoRoot 'templates' 'CLAUDE.md'
    $ClaudeTarget = Join-Path $TargetPath 'CLAUDE.md'
    if (Test-Path $ClaudeTemplate -PathType Leaf) {
        Copy-Item $ClaudeTemplate $ClaudeTarget
        Write-Host "Copied CLAUDE.md to $TargetPath"
    } else {
        Write-Warning "Warning: CLAUDE.md template not found at $ClaudeTemplate"
    }
}

Write-Host ""
Write-Host "Initialization complete."
Write-Host "Target: $TargetPath"
Write-Host "✓ GitHub Copilot (VS Code): .github/agents, instructions, and guidelines"
if ($DeployOpenCode) { Write-Host "✓ OpenCode: .opencode/skills/ and AGENTS.md" }
if ($DeployClaude) { Write-Host "✓ Claude Code: .claude/skills/ and CLAUDE.md" }
