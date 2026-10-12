param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$endpoint = "http://localhost:8000/cmd"

if ($Args.Count -eq 0) {
    Write-Host "sym_build : no command provided."
    exit 1
}

$cmd = $Args[0]
$cmdArgs = $Args[1..($Args.Count - 1)]

$body = @{
    cmd   = $cmd
    args  = $cmdArgs
    domain = "cmdline_operator"
} | ConvertTo-Json

try {
    $result = Invoke-RestMethod -Uri $endpoint -Method Post -Body $body -ContentType "application/json"
    $result | ConvertTo-Json -Depth 10
}
catch {
    Write-Host "sym_build : backend unreachable."
}
