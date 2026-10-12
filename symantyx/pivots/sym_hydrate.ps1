param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

# Physical shim: hydrate text via backend API
$endpoint = "http://localhost:8000/hydrate"

if ($Args.Count -eq 0) {
    Write-Host "sym_hydrate : no text provided."
    exit 1
}

$text = ($Args -join " ")

$body = @{
    text   = $text
    domain = "default"
} | ConvertTo-Json

try {
    $result = Invoke-RestMethod -Uri $endpoint -Method Post -Body $body -ContentType "application/json"
    $result | ConvertTo-Json -Depth 10
}
catch {
    Write-Host "sym_hydrate : backend unreachable."
}
