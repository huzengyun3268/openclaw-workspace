$json = Get-Content 'C:\Users\Administrator\.openclaw\agents\main\sessions\sessions.json' -Raw | ConvertFrom-Json
$key = 'openclaw-feishu:ou_ea447c64a0ccef262651c9780f761ca1'
if ($json.$key) {
    $json.$key.skillsSnapshot = $null
    $json | ConvertTo-Json -Depth 100 | Set-Content 'C:\Users\Administrator\.openclaw\agents\main\sessions\sessions.json' -Encoding UTF8
    Write-Host "Done - cleared skillsSnapshot"
} else {
    Write-Host "Key not found"
}
