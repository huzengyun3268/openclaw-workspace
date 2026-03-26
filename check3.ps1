[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$names = Get-Content 'C:\Users\Administrator\.openclaw\workspace\cn.txt'
$codes = @('600352','300033','831330','000988','688295','600487','300499','601168','600893','920046','430046','600114','301638','600089')
for ($i = 0; $i -lt $codes.Count; $i++) {
    $code = $codes[$i]
    $name = $names[$i]
    try {
        $pref = if ($code.StartsWith('6') -or $code.StartsWith('9')) { '1' } else { '0' }
        $uri = "https://push2.eastmoney.com/api/qt/stock/get?secid=$pref.$code&fields=f43,f44,f45,f46,f170"
        $d = (Invoke-RestMethod -Uri $uri -TimeoutSec 5).data
        $price = [math]::Round($d.f43 / 100, 2)
        $pct = [math]::Round($d.f170 / 100, 2)
        $open = [math]::Round($d.f46 / 100, 2)
        $high = [math]::Round($d.f44 / 100, 2)
        $low = [math]::Round($d.f45 / 100, 2)
        $sign = if ($pct -ge 0) { '+' } else { '' }
        Write-Output "$name|$code|price=$price|pct=$sign$pct%|O=$open|H=$high|L=$low"
    } catch {
        Write-Output "$name|$code|ERR"
    }
}
