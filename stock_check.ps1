$stocks = @('600352','600089','301667','920046','300033','831330','300189','430046','600114','301638')
$names = @{}
$names['600352'] = '浙江龙盛'
$names['600089'] = '特变电工'
$names['301667'] = '纳百川'
$names['920046'] = '亿能电力'
$names['300033'] = '同花顺'
$names['831330'] = '普适导航'
$names['300189'] = '神农种业'
$names['430046'] = '圣博润'
$names['600114'] = '东睦股份'
$names['301638'] = '南网数字'
$output = @()
foreach ($code in $stocks) {
    $market = if ($code.StartsWith('6')) { '1' } else { '0' }
    $url = 'https://push2.eastmoney.com/api/qt/stock/get?secid=' + $market + '.' + $code + '&fields=f43,f44,f45,f57,f58,f107,f169,f170'
    try {
        $r = Invoke-RestMethod $url -TimeoutSec 5
        if ($r.data) {
            $price = [math]::Round($r.data.f43 / 100, 3)
            $changePct = [math]::Round($r.data.f170 / 100, 2)
            $output += '$' + '' + '1|' + $names[$code] + '|$price|' + $changePct
        }
    } catch {
        $output += '$' + '' + '1|ERROR'
    }
}