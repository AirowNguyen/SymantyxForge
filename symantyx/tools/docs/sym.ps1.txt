param(
    [string]$Root = "."
)

$builder = "C:\Users\airow\tools\build_path.ps1"

function Invoke-Builder {
    param([object[]]$Args)
    & $builder @Args
}

Write-Host "sym : paste mode"
Write-Host "Paste your document. Press ENTER on an empty line to finish:"
Write-Host ""

$buffer = @()

while ($true) {
    $line = Read-Host
    if ($line -eq "") { break }
    $buffer += $line
}

if ($buffer.Count -eq 0) {
    Write-Host "sym : no input provided."
    exit 1
}

$lines = $buffer |
    Where-Object {
        $_ -match "/" -or $_ -match "\." -or $_ -match "\\"
    } |
    ForEach-Object { $_.Trim() } |
    Where-Object { $_ -ne "" }

if ($lines.Count -eq 0) {
    Write-Host "sym : no paths detected."
    exit 1
}

Write-Host ""
Write-Host "sym : building paths..."
Invoke-Builder @("-Raw", ($lines -join "`n"), "-Root", $Root)
Write-Host "sym : done."
