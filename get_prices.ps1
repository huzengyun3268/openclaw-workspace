$codes = @('600352.SH','300033.SZ','000988.SZ','688295.SH','600487.SH','300499.SZ','601168.SH','600893.SH','600114.SH','301638.SZ','600089.SH')
$baseUrl = 'https://push2.eastmoney.com/api/qt/stock/get?ut=fa5fd1943c7b386f172d6893dbfba10b&fields=f43,f107,f58,f50&secid='
foreach ($code in $codes) {
    try {
        $resp = Invoke-WebRequest -Uri ($baseUrl + $code) -TimeoutSec 10 -UseBasicParsing
        $text = $resp.Content -replace 'jQuery\(','' -replace '\);?$',''
        $j = $text | ConvertFrom-Json
        $price = [math]::Round($j.data.f43 / 100, 3)
        $chg = $j.data.f107
        $name = $j.data.f58
        $vol = [math]::Round($j.data.f50 / 1e8, 2)
        Write-Output ('{0}|{1}|{2}|{3}|{4}' -f $name, $code, $price, $chg, $vol)
    } catch {
        Write-Output ('ERROR|{0}|{1}' -f $code, $_.Exception.Message)
    }
}
