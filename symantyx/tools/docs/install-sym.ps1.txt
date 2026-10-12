param(
    [string]$ToolsRoot = "$HOME\tools"
)

Write-Host "Symantyx Installer: using tools root $ToolsRoot"

if (-not (Test-Path $ToolsRoot)) {
    New-Item -ItemType Directory -Force -Path $ToolsRoot | Out-Null
}

$profile = $PROFILE
if (-not (Test-Path $profile)) {
    New-Item -ItemType File -Force -Path $profile | Out-Null
}

if ($env:PATH -notlike "*$ToolsRoot*") {
    $env:PATH = "$env:PATH;$ToolsRoot"
}

$synPath = Join-Path $ToolsRoot "sym.ps1"
if (Test-Path $synPath) {
    $aliasLine = "Set-Alias sym `"$synPath`""
    $content = Get-Content $profile -Raw
    if ($content -notmatch "Set-Alias sym") {
        Add-Content -Path $profile -Value "`n$aliasLine`n"
    }
}

Write-Host "Symantyx installer complete."
