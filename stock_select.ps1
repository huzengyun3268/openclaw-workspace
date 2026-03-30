$headers = @{'Content-Type' = 'application/json'}
$body = @{"sentence" = "涨幅大于3%小于10%;非ST;非一字涨停"} | ConvertTo-Json -Compress
try {
    $resp = Invoke-WebRequest -Uri 'https://stockboot.jiuma.cn/api/dynamic-select/execute' -Method POST -Headers $headers -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) -TimeoutSec 15
    $content = $resp.Content | ConvertFrom-Json
    $stocks = $content.data.stocks
    Write-Host "符合条件的股票数量: $($content.data.totalCount)"
    foreach ($s in $stocks) {
        Write-Host "$($s.code) $($s.name) 涨幅: $([math]::Round($s.changeRate, 2))%"
    }
} catch {
    Write-Host "FAIL: $($_.Exception.Message)"
}
