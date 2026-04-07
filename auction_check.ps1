Add-Type -AssemblyName System.Net.Http
$codes = @('sh600352','sz300033','sh600487','sh600893','sh601168','sh518880','sz430046','sh600114','sh600089')
$results = @()

foreach ($code in $codes) {
    try {
        $url = "http://qt.gtimg.cn/q=$code"
        $resp = (New-Object System.Net.Http.HttpClient).GetStringAsync($url).Result
        $parts = $resp -split '~'
        if ($parts.Count -gt 10) {
            $name = $parts[1]
            $yestClose = [double]$parts[3]
            $openPrice = if ([double]$parts[4] -gt 0) { [double]$parts[4] } else { $yestClose }
            $vol = if ($parts.Count -gt 6) { $parts[6] } else { "0" }
            if ($yestClose -gt 0 -and $openPrice -gt 0) {
                $chgPct = ($openPrice - $yestClose) / $yestClose * 100
            } else {
                $chgPct = 0
            }
            $results += "$name($code): 昨收=$yestClose 竞价=$openPrice 涨幅=[$('{0:+0.00;-0.00;0.00}' -f $chgPct)]%"
        } else {
            $results += "$code : 数据解析失败"
        }
    } catch {
        $results += "$code : 错误-$($_.Exception.Message)"
    }
}

$results -join "`n"
