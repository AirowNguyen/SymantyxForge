param(
    [string]$ToolsRoot = "$HOME\tools"
)

Write-Host "Binding Symantyx toolchain from $ToolsRoot"

if (-not (Test-Path $ToolsRoot)) {
    New-Item -ItemType Directory -Force -Path $ToolsRoot | Out-Null
}

$profile = $PROFILE
if (-not (Test-Path $profile)) {
    New-Item -ItemType File -Force -Path $profile | Out-Null
}

# Ensure tools root in PATH
if ($env:PATH -notlike "*$ToolsRoot*") {
    $env:PATH = "$env:PATH;$ToolsRoot"
    Write-Host "Added tools root to PATH (current session)."
}

$existing = Get-Content $profile -Raw

# Bind all scripts as aliases
Get-ChildItem -Path $ToolsRoot -Filter "*.ps1" | ForEach-Object {
    $name = $_.BaseName
    $path = $_.FullName
    $aliasLine = "Set-Alias $name `"$path`""

    if ($existing -notmatch "Set-Alias $name") {
        Add-Content -Path $profile -Value "`n$aliasLine`n"
        Write-Host "Bound global alias: $name -> $path"
    } else {
        Write-Host "Alias already present for: $name"
    }
}

Write-Host "Symantyx toolchain globally bound. Restart PowerShell to activate all aliases."
