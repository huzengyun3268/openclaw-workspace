$stocks = @(
    @{name='特变电工'; code='600089'; cost=24.765; shares=52300},
    @{name='浙江龙盛'; code='600352'; cost=15.912; shares=141700},
    @{name='锡华科技'; code='603248'; cost=35.490; shares=2000},
    @{name='同花顺'; code='300033'; cost=511.220; shares=600},
    @{name='神农种业'; code='300189'; cost=17.099; shares=5000},
    @{name='亿能电力'; code='920046'; cost=35.936; shares=12731},
    @{name='普适导航'; code='831330'; cost=20.415; shares=6370},
    @{name='圣博润'; code='430046'; cost=0.478; shares=10334}
)

$secids = ($stocks | ForEach-Object {
    if ($_.code -match '^00|^60|^68|^30') { "1.$($_.code)" }
    elseif ($_.code -match '^920|^430') { "0.$($_.code)" }
    else { "1.$($_.code)" }
}) -join ','

$url = "https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&fields=f12,f14,f3,f2&secids=$secids"

try {
    $resp = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 15
    $json = $resp.Content | ConvertFrom-Json
    $prices = @{}
    if ($json.data -and $json.data.diff) {
        foreach ($item in $json.data.diff) {
            $prices[$item.f12] = @{price=$item.f2; change=$item.f3; name=$item.f14}
        }
    }
    $priceFetched = $true
} catch {
    Write-Host "Price fetch failed: $_"
    $priceFetched = $false
}

$totalCost = 0
$totalValue = 0
$results = @()

foreach ($s in $stocks) {
    $code = $s.code
    $fetchedPrice = $null
    if ($priceFetched -and $prices[$code]) {
        $fetchedPrice = $prices[$code].price
    }

    $price = if ($fetchedPrice -ne $null) { $fetchedPrice } else { $s.cost }
    $change = if ($prices[$code]) { $prices[$code].change } else { 0 }

    $costAmt = $s.cost * $s.shares
    $value = $price * $s.shares
    $pnl = $value - $costAmt
    if ($costAmt -ne 0) { $pnlPct = ($pnl / $costAmt) * 100 } else { $pnlPct = 0 }

    $totalCost += $costAmt
    $totalValue += $value

    $results += @{
        name=$s.name
        code=$code
        price=$price
        cost=$s.cost
        shares=$s.shares
        pnl=$pnl
        pnlPct=$pnlPct
        change=$change
    }
}

$totalPnL = $totalValue - $totalCost
if ($totalCost -ne 0) { $totalPnLPct = ($totalPnL / $totalCost) * 100 } else { $totalPnLPct = 0 }

$msg = "📊 **股票早报** | 2026/03/20`n`n"

foreach ($r in $results) {
    $sign = if ($r.pnl -ge 0) { '+' } else { '' }
    $arrow = if ($r.pnl -ge 0) { '▲' } else { '▼' }
    $csign = if ($r.change -ge 0) { '+' } else { '' }
    $carrow = if ($r.change -ge 0) { '▲' } else { '▼' }

    $msg += "**$($r.name)** ($($r.code))`n"
    $msg += "  现价 $($r.price.ToString('F3'))  $carrow $csign$($r.change.ToString('F2'))%`n"
    $msg += "  成本 $($r.cost.ToString('F3'))  |  盈亏 ${sign}$($r.pnl.ToString('F2'))元 (${sign}$($r.pnlPct.ToString('F2'))%)`n`n"
}

$ts = if ($totalPnL -ge 0) { '+' } else { '' }
$ta = if ($totalPnL -ge 0) { '▲' } else { '▼' }
$msg += "──────────────────`n"
$msg += "**合计**  总市值 $($totalValue.ToString('F2'))元  总成本 $($totalCost.ToString('F2'))元`n"
$msg += "${ta} 总盈亏 ${ts}$($totalPnL.ToString('F2'))元 (${ts}$($totalPnLPct.ToString('F2'))%)`n"
if ($priceFetched) { $msg += "`n⚠️ 行情数据仅供参考，实际以交易软件为准" }

Write-Output $msg
