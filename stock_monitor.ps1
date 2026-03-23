# 持仓监控脚本 - 获取实时行情并检查异动
# 持仓数据来自 USER.md

$positions = @(
    # 华泰柏瑞账户
    @{Name="浙江龙盛"; Code="600352"; Shares=106700; Cost=15.91; Market="sh"},
    @{Name="特变电工"; Code="600089"; Shares=52300; Cost=24.765; Market="sh"},
    @{Name="纳百川"; Code="301667"; Shares=3000; Cost=82.715; Market="sz"},
    @{Name="亿能电力"; Code="920046"; Shares=12731; Cost=35.936; Market="bj"},
    @{Name="同花顺"; Code="300033"; Shares=600; Cost=511.22; Market="sz"},
    @{Name="普适导航"; Code="831330"; Shares=6370; Cost=20.415; Market="bj"},
    @{Name="神农种业"; Code="300189"; Shares=5000; Cost=17.099; Market="sz"},
    @{Name="圣博润"; Code="430046"; Shares=10334; Cost=0.478; Market="bj"},
    # 老婆账户
    @{Name="东睦股份"; Code="600114"; Shares=9200; Cost=32.428; Market="sh"; Note="老婆账户"},
    @{Name="南网数字"; Code="301638"; Shares=1700; Cost=32.635; Market="sz"; Note="老婆账户"}
)

# 异动阈值
$alertRiseThreshold = 0.03    # 涨幅超过3%警告
$alertFallThreshold = -0.03   # 跌幅超过3%警告
$urgentFallThreshold = -0.05  # 跌幅超过5%紧急
$profitAlert = 0.10           # 盈利超过10%警告
$lossAlert = -0.10            # 亏损超过10%警告

$results = @()
$alerts = @()

# 获取实时行情 (东方财富API)
$codes = ($positions | ForEach-Object { 
    if ($_.Market -eq "sh") { "sh" + $_.Code }
    elseif ($_.Market -eq "sz") { "sz" + $_.Code }
    else { "bj" + $_.Code }
}) -join ","

$apiUrl = "https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&secids=$codes&fields=f1,f2,f3,f4,f12,f14,f15,f16,f17,f18"

try {
    $response = Invoke-RestMethod -Uri $apiUrl -TimeoutSec 10 -UserAgent "Mozilla/5.0"
    $stockData = @{}
    if ($response.data) {
        $response.data | ForEach-Object { $stockData[$_.f12] = $_ }
    }
} catch {
    Write-Error "API请求失败: $_"
    exit 1
}

foreach ($pos in $positions) {
    $code = $pos.Code
    $data = $stockData[$code]
    
    if ($null -eq $data) {
        $results += [PSCustomObject]@{
            Name = $pos.Name
            Code = $code
            CurrentPrice = "N/A"
            Change = "N/A"
            ChangePercent = "N/A"
            MarketValue = "N/A"
            Profit = "N/A"
            ProfitPercent = "N/A"
            Alert = "获取失败"
        }
        continue
    }

    $currentPrice = $data.f2 / 100  # f2是当前价格，精确到分
    $change = if ($data.f3) { $data.f3 / 100 } else { 0 }  # f3是涨跌额
    $changePercent = if ($data.f4) { $data.f4 / 100 } else { 0 }  # f4是涨跌幅%

    if ($currentPrice -eq -1 -or $currentPrice -eq 0) {
        $results += [PSCustomObject]@{
            Name = $pos.Name
            Code = $code
            CurrentPrice = "停牌/无数据"
            Change = "N/A"
            ChangePercent = "N/A"
            MarketValue = "N/A"
            Profit = "N/A"
            ProfitPercent = "N/A"
            Alert = "停牌"
        }
        continue
    }

    $marketValue = [math]::Round($currentPrice * $pos.Shares, 2)
    $cost = $pos.Cost
    $totalCost = [math]::Round($cost * $pos.Shares, 2)
    $profit = [math]::Round($marketValue - $totalCost, 2)
    $profitPercent = [math]::Round(($currentPrice - $cost) / $cost * 100, 2)

    $alert = ""
    if ($changePercent -ge ($alertRiseThreshold * 100)) {
        $alert = "🚀 涨幅警示"
    } elseif ($changePercent -le ($urgentFallThreshold * 100)) {
        $alert = "🚨 紧急下跌"
    } elseif ($changePercent -le ($alertFallThreshold * 100)) {
        $alert = "⚠️ 下跌警示"
    }

    if ($profitPercent -ge ($profitAlert * 100)) {
        $alert = "💰 大幅盈利"
    } elseif ($profitPercent -le ($lossAlert * 100)) {
        $alert = "🔴 深度亏损"
    }

    $results += [PSCustomObject]@{
        Name = $pos.Name
        Code = $code
        CurrentPrice = $currentPrice.ToString("F2")
        Change = $change.ToString("F2")
        ChangePercent = $changePercent.ToString("F2") + "%"
        MarketValue = $marketValue.ToString("N0")
        Cost = $cost.ToString("F2")
        Profit = $profit.ToString("N0")
        ProfitPercent = $profitPercent.ToString("F2") + "%"
        Note = $pos.Note
        Alert = $alert
    }

    if ($alert -ne "") {
        $alerts += [PSCustomObject]@{
            Name = $pos.Name
            Code = $code
            CurrentPrice = $currentPrice.ToString("F2")
            ChangePercent = $changePercent.ToString("F2") + "%"
            ProfitPercent = $profitPercent.ToString("F2") + "%"
            Alert = $alert
            Note = $pos.Note
        }
    }
}

# 输出完整报告
Write-Output "=== 持仓监控报告 $(Get-Date -Format 'yyyy-MM-dd HH:mm') ==="
Write-Output ""
Write-Output "--- 行情总览 ---"
foreach ($r in $results) {
    $note = if ($r.Note) { " [$($r.Note)]" } else { "" }
    $alert = if ($r.Alert -ne "") { " $($r.Alert)" } else { "" }
    Write-Output "$($r.Name)($($r.Code))$note : 现价=$($r.CurrentPrice) 涨跌=$($r.Change) ($($r.ChangePercent)) | 成本=$($r.Cost) 盈亏=$($r.Profit) ($($r.ProfitPercent))$alert"
}

Write-Output ""
Write-Output "--- 异动警报 ---"
if ($alerts.Count -eq 0) {
    Write-Output "无明显异动 ✅"
} else {
    foreach ($a in $alerts) {
        $note = if ($a.Note) { " [$($a.Note)]" } else { "" }
        Write-Output "$($a.Alert) $($a.Name)($($a.Code))$note : 现价=$($a.CurrentPrice) 今日=$($a.ChangePercent) 持仓盈亏=$($a.ProfitPercent)"
    }
}

Write-Output ""
Write-Output "---JSON---"
$alerts | ConvertTo-Json -Compress
