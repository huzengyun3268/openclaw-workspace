# 持仓监控脚本
$positions = @(
    @{Name='浙江龙盛'; Code='600352'; Shares=106700; Cost=15.91; Market='sh'},
    @{Name='特变电工'; Code='600089'; Shares=52300; Cost=24.765; Market='sh'},
    @{Name='纳百川'; Code='301667'; Shares=3000; Cost=82.715; Market='sz'},
    @{Name='亿能电力'; Code='920046'; Shares=12731; Cost=35.936; Market='bj'},
    @{Name='同花顺'; Code='300033'; Shares=600; Cost=511.22; Market='sz'},
    @{Name='普适导航'; Code='831330'; Shares=6370; Cost=20.415; Market='bj'},
    @{Name='神农种业'; Code='300189'; Shares=5000; Cost=17.099; Market='sz'},
    @{Name='圣博润'; Code='430046'; Shares=10334; Cost=0.478; Market='bj'},
    @{Name='东睦股份'; Code='600114'; Shares=9200; Cost=32.428; Market='sh'; Note='wife'},
    @{Name='南网数字'; Code='301638'; Shares=1700; Cost=32.635; Market='sz'; Note='wife'}
)

$alertRiseThreshold = 3.0
$alertFallThreshold = -3.0
$urgentFallThreshold = -5.0
$profitAlert = 10.0
$lossAlert = -10.0

$codes = ($positions | ForEach-Object {
    if ($_.Market -eq 'sh') { 'sh' + $_.Code }
    elseif ($_.Market -eq 'sz') { 'sz' + $_.Code }
    else { 'bj' + $_.Code }
}) -join ','

$apiUrl = 'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&secids=' + $codes + '&fields=f1,f2,f3,f4,f12,f14'

try {
    $response = Invoke-RestMethod -Uri $apiUrl -TimeoutSec 15 -UserAgent 'Mozilla/5.0'
    $stockData = @{}
    if ($response.data) {
        $response.data | ForEach-Object { $stockData[$_.f12] = $_ }
    }
} catch {
    Write-Error ('API请求失败: ' + $_)
    exit 1
}

$results = @()
$alerts = @()

foreach ($pos in $positions) {
    $code = $pos.Code
    $data = $stockData[$code]

    if ($null -eq $data) {
        Write-Output ('[FAIL] ' + $pos.Name + ' ' + $code)
        continue
    }

    $currentPrice = if ($data.f2 -and $data.f2 -ne -1) { $data.f2 / 100 } else { $null }
    $changePercent = if ($data.f4) { $data.f4 / 100 } else { 0 }

    if ($null -eq $currentPrice -or $currentPrice -eq 0) {
        Write-Output ('[STOP] ' + $pos.Name + ' ' + $code)
        continue
    }

    $marketValue = [math]::Round($currentPrice * $pos.Shares, 2)
    $totalCost = [math]::Round($pos.Cost * $pos.Shares, 2)
    $profit = [math]::Round($marketValue - $totalCost, 2)
    $profitPercent = [math]::Round(($currentPrice - $pos.Cost) / $pos.Cost * 100, 2)

    $alert = ''
    if ($changePercent -ge $alertRiseThreshold) { $alert = 'RISE' }
    elseif ($changePercent -le $urgentFallThreshold) { $alert = 'URGENT' }
    elseif ($changePercent -le $alertFallThreshold) { $alert = 'FALL' }
    if ($profitPercent -ge $profitAlert -and $alert -eq '') { $alert = 'BIGPROFIT' }
    if ($profitPercent -le $lossAlert -and $alert -eq '') { $alert = 'DEEPLOSS' }

    $note = if ($pos.Note) { ' | ' + $pos.Note } else { '' }
    $alertTag = if ($alert) { ' | ' + $alert } else { '' }

    Write-Output ('CHECK|' + $pos.Name + '|' + $code + '|' + $currentPrice.ToString('F2') + '|' + $changePercent.ToString('F2') + '|' + $marketValue.ToString('N0') + '|' + $pos.Cost.ToString('F2') + '|' + $profit.ToString('N0') + '|' + $profitPercent.ToString('F2') + '|' + $alert + '|' + $note)

    if ($alert -ne '') {
        $alerts += $alert + '|' + $pos.Name + '|' + $code + '|' + $currentPrice.ToString('F2') + '|' + $changePercent.ToString('F2') + '|' + $profitPercent.ToString('F2') + '|' + $note
    }
}

Write-Output ''
Write-Output '---ALERTS---'
if ($alerts.Count -eq 0) {
    Write-Output 'NONE'
} else {
    $alerts | ForEach-Object { Write-Output $_ }
}
