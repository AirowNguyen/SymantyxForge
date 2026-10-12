param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$endpoint = "http://localhost:8000/process"

if ($Args.Count -eq 0) {
    Write-Host "sym_canvas : no text provided."
    exit 1
}

$text = ($Args -join " ")

$body = @{
    text   = $text
    domain = "canvas"
} | ConvertTo-Json

try {
    $result = Invoke-RestMethod -Uri $endpoint -Method Post -Body $body -ContentType "application/json"
    $result | ConvertTo-Json -Depth 10
}
catch {
    Write-Host "sym_canvas : backend unreachable."
}
