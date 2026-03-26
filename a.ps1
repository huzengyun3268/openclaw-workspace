#竞价监控
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$stocks = @(
    '600352',
    '300033',
    '831330',
    '000988',
    '688295',
    '600487',
    '300499',
    '601168',
    '600893',
    '920046',
    '430046',
    '600114',
    '301638',
    '600089'
)
$names = @(
    '浙江龙盛',
    '同花顺',
    '普适导航',
    '华工科技',
    '中复神鹰',
    '亨通光电',
    '高澜股份',
    '西部矿业',
    '航发动力',
    '亿能电力',
    '圣博润',
    '东睦股份',
    '南网数字',
    '特变电工'
)
$out = @()
for ($i = 0; $i -lt $stocks.Count; $i++) {
    $code = $stocks[$i]
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
        $out += "$name|$code|$price|$sign$pct%|O=$open H=$high L=$low"
    } catch {
        $out += "$name|$code|ERR"
    }
}
$out -join "`n"
