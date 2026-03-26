# stock check
Add-Type -AssemblyName System.Net.Http

$stocks = @{
    '600352' = '浙江龙盛'
    '300033' = '同花顺'
    '831330' = '普适导航'
    '000988' = '华工科技'
    '688295' = '中复神鹰'
    '600487' = '亨通光电'
    '300499' = '高澜股份'
    '601168' = '西部矿业'
    '600893' = '航发动力'
    '920046' = '亿能电力'
    '430046' = '圣博润'
    '600089' = '特变电工'
    '600114' = '东睦股份'
    '301638' = '南网数字'
}

$codes = $stocks.Keys -join ','
$url = "http://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&fields=f2,f3,f4,f12,f14&secids=$codes"

try {
    $wc = New-Object System.Net.WebClient
    $wc.Encoding = [System.Text.Encoding]::UTF8
    $json = $wc.DownloadString($url)
    $data = $json | ConvertFrom-Json
    $items = $data.data.diff
    foreach ($item in $items) {
        $name = $stocks[$item.f12]
        $price = $item.f2
        $chg = $item.f3
        $chg_pct = $item.f4
        Write-Host "$name ($($item.f12)): $price 涨跌:$chg% 涨跌幅:$chg_pct%"
    }
} catch {
    Write-Host "Error: $_"
}
