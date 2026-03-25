param([string]$codes)
$url = "http://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&fields=f12,f14,f3,f2,f4,f5&secids=$codes"
try {
    $r = Invoke-WebRequest -Uri $url -UserAgent "Mozilla/5.0" -TimeoutSec 10
    $j = [System.Text.Encoding]::UTF8.GetString($r.Content) | ConvertFrom-Json
    foreach ($item in $j.data.diff) {
        $code = $item.f12
        $name = $item.f14
        $pct = $item.f3
        $price = $item.f2
        $prev = $item.f4
        $open = $item.f5
        $sign = if($pct -gt 0){'+'} else {''}
        Write-Host "$code $name`: 现价=$price 涨幅=$sign$pct% 开盘=$open"
    }
} catch {
    Write-Host "Error: $_"
}
