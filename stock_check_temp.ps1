$headers = @{"User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
$codes = @("sh600352","sh600893","sz300033","sh601168","bj831330","sh600487","sh688295","bj920046","bj430046")
$names = @("\u6d59\u6c5f\u9f99\u76db","\u822a\u53d1\u52a8\u529b","\u540c\u82b1\u987a","\u897f\u90e8\u77ff\u4e1a","\u666e\u9002\u5bfc\u822a","\u4ea8\u901a\u5149\u7535","\u4e2d\u590d\u795e\u9e70","\u4ebf\u80fd\u7535\u529b","\u5723\u535a\u6da6")
$cost = @(16.52, 49.184, 423.488, 26.169, 20.361, 43.998, 37.843, 329.553, 0.478)
$stop = @(12.0, 42.0, 280, 22.0, 18.0, 38.0, 0, 0, 0)

$url = "https://qt.gtimg.cn/q=" + ($codes -join ",")
try {
    $response = Invoke-WebRequest -Uri $url -Headers $headers -TimeoutSec 10
    $lines = $response.Content -split "`n"
    Write-Host "=== \u6301\u4ed3\u76d1\u63a7 $(Get-Date -Format 'HH:mm') ==="
    $alertCount = 0
    for ($i = 0; $i -lt $names.Count; $i++) {
        $line = $lines[$i]
        if ($line -match "=""([^""]+)""") {
            $data = $matches[1] -split "~"
            if ($data.Count -gt 10) {
                $price = [double]$data[3]
                $changePct = [double]$data[32]
                $gain = ($price - $cost[$i]) * 10000
                $status = ""
                if ($stop[$i] -gt 0 -and $price -le $stop[$i]) {
                    $status = " *\u89e6\u53ca\u6b62\u635f!"
                    $alertCount++
                } elseif ($gain -lt -50000) {
                    $status = " *\u8d83\u635f\u8f83\u5927"
                }
                $gainStr = if ($gain -ge 0) { "+" + $gain.ToString("0.0") } else { $gain.ToString("0.0") }
                $pctStr = if ($changePct -ge 0) { "+" + $changePct.ToString("0.00") } else { $changePct.ToString("0.00") }
                Write-Host "$($names[$i])($($codes[$i])): $price ($pctStr%) | $gainStr\u4e07 $status"
            }
        }
    }
    if ($alertCount -eq 0) {
        Write-Host "`nAll positions normal"
    }
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}
