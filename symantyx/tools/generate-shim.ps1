param(
    [Parameter(Mandatory=$true)]
    [string]$ScriptPath,
    [Parameter(Mandatory=$true)]
    [string]$CommandName,
    [string]$ToolsRoot = "$HOME\tools"
)

if (-not (Test-Path $ToolsRoot)) {
    New-Item -ItemType Directory -Force -Path $ToolsRoot | Out-Null
}

$fullScript = Resolve-Path $ScriptPath
$shimPath   = Join-Path $ToolsRoot "$CommandName.ps1"

$shim = @"
param([Parameter(ValueFromRemainingArguments=\$true)][object[]]\$Args)
& "$fullScript" @Args
"@

Set-Content -Path $shimPath -Value $shim -Encoding UTF8
Write-Host "Shim generated: $CommandName -> $fullScript"
Write-Host "Shim path: $shimPath"
