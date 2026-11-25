#Requires -Version 5.1
<#
.SYNOPSIS
    Installs the OpenCode skills + plugins kit into an OpenCode config directory.

.DESCRIPTION
    One-file installer. It copies the packaged skills and plugins into the target
    OpenCode config directory, then merges the two config keys the kit owns
    ("plugins" and "skills") into opencode.jsonc / opencode.json. Every other
    setting in your config is left untouched. The config is backed up first.

.PARAMETER Target
    Home  -> $HOME\.config\opencode   (default)
    Project -> <current directory>\.opencode

.PARAMETER TargetDir
    Override the destination directory explicitly (useful for testing).

.PARAMETER ConfigFile
    Override the config file to merge into. Auto-detected otherwise.

.PARAMETER SkipNpm
    Skip installing the npm-declared plugins.

.EXAMPLE
    .\install.ps1
    Installs into the current user's global OpenCode config.

.EXAMPLE
    .\install.ps1 -Target Project -WhatIf
    Shows what would happen for a project-local install.
#>
[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'Medium')]
param(
    [ValidateSet('Home', 'Project')][string]$Target = 'Home',
    [string]$TargetDir,
    [string]$ConfigFile,
    [switch]$SkipNpm
)

$ErrorActionPreference = 'Stop'
$KitRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

if ($IsLinux -or $IsMacOS) {
    throw "This installer is Windows-only (robocopy). Use a bash variant for Linux/macOS."
}
if (-not (Test-Path (Join-Path $KitRoot 'skills'))) {
    throw "Kit payload missing: $KitRoot\skills"
}
if (-not (Test-Path (Join-Path $KitRoot 'plugins'))) {
    throw "Kit payload missing: $KitRoot\plugins"
}

if (-not $TargetDir) {
    if ($Target -eq 'Home') {
        $TargetDir = Join-Path $HOME '.config\opencode'
    } else {
        $TargetDir = Join-Path (Get-Location) '.opencode'
    }
}
$TargetDir = [System.IO.Path]::GetFullPath($TargetDir)

Write-Host "Kit root   : $KitRoot" -ForegroundColor Cyan
Write-Host "Target dir : $TargetDir" -ForegroundColor Cyan

function Copy-KitPayload {
    param([string]$From, [string]$To, [string]$Label)

    if (-not (Test-Path $From)) { throw "Missing payload: $From" }
    if (-not $PSCmdlet.ShouldProcess($To, "Install $Label")) { return }

    New-Item -ItemType Directory -Force -Path $To | Out-Null
    # /E copies subdirectories including empty ones. Extra files already in the
    # destination are left alone, so this is idempotent and non-destructive.
    $null = & robocopy $From $To /E /NFL /NDL /NJH /NJS /NP /R:1 /W:1
    $rc = $LASTEXITCODE
    if ($rc -ge 8) { throw "robocopy failed for $Label with exit code $rc" }
    Write-Host "  [ok] $Label -> $To" -ForegroundColor Green
}

function Remove-JsonComments {
    param([string]$Text)
    # Removes // and /* */ comments without touching URLs inside strings.
    $sb = New-Object System.Text.StringBuilder
    $inString = $false; $escaped = $false; $inLine = $false; $inBlock = $false
    for ($i = 0; $i -lt $Text.Length; $i++) {
        $c = $Text[$i]
        $n = if ($i + 1 -lt $Text.Length) { $Text[$i + 1] } else { [char]0 }
        if ($inLine) {
            if ($c -eq "`n") { $inLine = $false; [void]$sb.Append($c) }
            continue
        }
        if ($inBlock) {
            if ($c -eq '*' -and $n -eq '/') { $inBlock = $false; $i++ }
            continue
        }
        if ($inString) {
            [void]$sb.Append($c)
            if ($escaped) { $escaped = $false }
            elseif ($c -eq '\') { $escaped = $true }
            elseif ($c -eq '"') { $inString = $false }
            continue
        }
        if ($c -eq '"') { $inString = $true; [void]$sb.Append($c); continue }
        if ($c -eq '/' -and $n -eq '/') { $inLine = $true; $i++; continue }
        if ($c -eq '/' -and $n -eq '*') { $inBlock = $true; $i++; continue }
        [void]$sb.Append($c)
    }
    return $sb.ToString()
}

function Merge-ConfigArray {
    param($Existing, [object[]]$Desired)
    $items = New-Object System.Collections.Generic.List[object]
    if ($null -ne $Existing) {
        foreach ($item in @($Existing)) { if ($null -ne $item -and -not $items.Contains($item)) { $items.Add($item) } }
    }
    foreach ($item in $Desired) { if (-not $items.Contains($item)) { $items.Add($item) } }
    return $items.ToArray()
}

Copy-KitPayload -From (Join-Path $KitRoot 'skills')  -To (Join-Path $TargetDir 'skills')  -Label 'skills'
Copy-KitPayload -From (Join-Path $KitRoot 'plugins') -To (Join-Path $TargetDir 'plugins') -Label 'plugins'

# ---- Config merge -----------------------------------------------------------
$kitConfigPath = Join-Path $KitRoot 'config\opencode.kit.json'
$kitConfig = (Get-Content $kitConfigPath -Raw | ConvertFrom-Json)

if (-not $ConfigFile) {
    foreach ($candidate in @('opencode.jsonc', 'opencode.json')) {
        $p = Join-Path $TargetDir $candidate
        if (Test-Path $p) { $ConfigFile = $p; break }
    }
    if (-not $ConfigFile) { $ConfigFile = Join-Path $TargetDir 'opencode.jsonc' }
}
$ConfigFile = [System.IO.Path]::GetFullPath($ConfigFile)
Write-Host "Config     : $ConfigFile" -ForegroundColor Cyan

if (-not $PSCmdlet.ShouldProcess($ConfigFile, 'Merge plugins/skills keys')) {
    Write-Host "  [skip] config merge (WhatIf)" -ForegroundColor Yellow
} else {
    $isNew = -not (Test-Path $ConfigFile)
    if ($isNew) {
        $config = [pscustomobject]@{}
    } else {
        $raw = Get-Content $ConfigFile -Raw
        $config = (Remove-JsonComments -Text $raw | ConvertFrom-Json)
        if ($config -isnot [pscustomobject]) { throw "Config root is not an object: $ConfigFile" }
        $backup = "$ConfigFile.bak-install-$(Get-Date -Format yyyyMMdd-HHmmss)"
        Copy-Item -LiteralPath $ConfigFile -Destination $backup -Force
        Write-Host "  [ok] backup -> $backup" -ForegroundColor Green
    }

    foreach ($key in @('plugins', 'skills')) {
        $desired = @($kitConfig.$key)
        if ($config.PSObject.Properties.Name -contains $key) {
            $merged = Merge-ConfigArray -Existing $config.$key -Desired $desired
            $config | Add-Member -NotePropertyName $key -NotePropertyValue $merged -Force
        } else {
            $config | Add-Member -NotePropertyName $key -NotePropertyValue $desired -Force
        }
    }

    $json = $config | ConvertTo-Json -Depth 100
    [System.IO.File]::WriteAllText($ConfigFile, $json, (New-Object System.Text.UTF8Encoding($false)))
    Write-Host "  [ok] merged keys: plugins, skills" -ForegroundColor Green
}

# ---- npm plugins ------------------------------------------------------------
if ($SkipNpm) {
    Write-Host "npm plugins: skipped (-SkipNpm)" -ForegroundColor Yellow
} elseif ($PSCmdlet.ShouldProcess($TargetDir, 'Install npm-declared plugins')) {
    $pkg = Join-Path $TargetDir 'package.json'
    if (-not (Test-Path $pkg)) {
        Copy-Item -LiteralPath (Join-Path $KitRoot 'package.json') -Destination $pkg -Force
        Write-Host "  [ok] wrote package.json" -ForegroundColor Green
    }
    Push-Location $TargetDir
    try {
        npm install --no-audit --no-fund --omit=dev
        if ($LASTEXITCODE -ne 0) {
            Write-Warning "npm install exited with $LASTEXITCODE; skills/plugins are installed but npm plugins may need manual install."
        }
    } finally {
        Pop-Location
    }
}

Write-Host "Done. Start OpenCode with this config directory to load the kit." -ForegroundColor Cyan
