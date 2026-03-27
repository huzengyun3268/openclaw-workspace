$wc = [System.Net.WebClient]::new()
try {
    $r1 = $wc.DownloadString("https://push2.eastmoney.com/api/qt/stock/get?secid=0.831330&fields=f43,f170,f171")
    Write-Host "831330: $r1"
} catch { Write-Host "831330 Error" }
try {
    $r2 = $wc.DownloadString("https://push2.eastmoney.com/api/qt/stock/get?secid=0.430046&fields=f43,f170,f171")
    Write-Host "430046: $r2"
} catch { Write-Host "430046 Error" }
