# Stock T Selection - 2:30买入策略
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Get-StockData {
    param([string]$code, [string]$name="未知")
    $result = @{success=$false; price=0; pct=0; high=0; low=0; vol=0; name=$name; src=""}
    $isSz = $code -match "^000|^001|^002|^003|^300|^301|^302|^080|^399"
    $isBj = $code -match "^920"
    if ($isSz) { $prefix = "sz" } elseif ($isBj) { $prefix = "bj" } else { $prefix = "sh" }
    try {
        $url = "https://qt.gtimg.cn/q=${prefix}${code}"
        $req = [System.Net.WebRequest]::Create($url)
        $req.UserAgent = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)"
        $req.Timeout = 6000
        $resp = $req.GetResponse()
        $stream = $resp.GetResponseStream()
        $sr = New-Object System.IO.StreamReader($stream, [System.Text.Encoding]::UTF8)
        $data = $sr.ReadToEnd(); $sr.Close(); $resp.Close()
        $parts = $data.Split('~')
        if ($parts.Length -gt 35 -and $parts[1] -ne "pv_none_match" -and $parts[3] -ne "" -and $parts[3] -ne "0") {
            $result.success = $true
            $result.price = [double]$parts[3]
            $result.pct = [double]$parts[32]
            $result.high = [double]$parts[33]
            $result.low = [double]$parts[34]
            $result.vol = [int]$parts[6]
            $result.name = $parts[1]
            $result.src = "T"
            return $result
        }
    } catch {}
    return $result
}

# ============ 候选股票池（今日重点观察）============
# 策略：涨幅>2%、股价在当日中高位运行、量比>1.5
$candidates = @(
    # 今日强势股（涨幅>2%，供参考）
    @{code="600406"; name="国电南瑞"; reason="电力设备龙头"}
    @{code="600487"; name="亨通光电"; reason="今日强势+2.3%"}
    @{code="688295"; name="中复神鹰"; reason="碳纤维题材"}
    @{code="600893"; name="航发动力"; reason="军工板块"}
    @{code="300750"; name="宁德时代"; reason="锂电龙头"}
    @{code="300274"; name="阳光电源"; reason="光伏逆变器"}
    @{code="601012"; name="隆基绿能"; reason="光伏组件"}
    @{code="002466"; name="天齐锂业"; reason="锂资源"}
    @{code="600089"; name="特变电工"; reason="特高压+业绩好"}
    @{code="300059"; name="东方财富"; reason="券商互联网"}
    @{code="688012"; name="中微公司"; reason="半导体设备"}
    @{code="002371"; name="北方华创"; reason="半导体设备"}
    @{code="601919"; name="中远海控"; reason="航运周期"}
    @{code="600019"; name="中国平安"; reason="保险龙头"}
    @{code="000858"; name="五粮液"; reason="白酒消费"}
)

Write-Host "=== 明日T+1 选股池初步筛选 ==="
Write-Host "筛选条件：涨幅>1%、量比>1.5、当日价格在中高位"
Write-Host ""

$results = @()
foreach ($c in $candidates) {
    $r = Get-StockData -code $c.code -name $c.name
    if ($r.success) {
        $nearHigh = if ($r.high > 0) { [Math]::Round(($r.price / $r.high - 1) * 100, 1) } else { 0 }
        $nearLow = if ($r.low > 0 -and $r.price -gt $r.low) { [Math]::Round(($r.price - $r.low) / $r.low * 100, 1) } else { 0 }
        $results += [PSCustomObject]@{
            Code = $c.code
            Name = $r.name
            Price = $r.price
            Pct = $r.pct
            High = $r.high
            NearHigh = $nearHigh
            Vol = $r.vol
            Reason = $c.reason
        }
    }
}

# 排序：涨幅高的优先
$results = $results | Sort-Object { [Math]::Abs($_.Pct) } -Descending

Write-Host "符合条件（涨幅>1%）："
Write-Host ""
foreach ($r in $results) {
    if ($r.Pct -gt 1) {
        $arrow = if ($r.Pct -gt 0) { "+" } else { "" }
        $mark = if ($r.Pct -gt 3) { "**" } elseif ($r.Pct -gt 2) { "*" } else { "" }
        Write-Host "$mark $($r.Name)($($r.Code)): $($r.Price) $arrow$($r.Pct)% [距高点$($r.NearHigh)%] 原因:$($r.Reason) $mark"
    }
}

Write-Host ""
Write-Host "提示：以上仅为初步筛选，明日T+1操作需结合:"
Write-Host "1. 明日开盘竞价涨幅（<2%入场较好）"
Write-Host "2. 大盘整体情绪"
Write-Host "3. 严格止损：跌3%无条件出"
Write-Host "4. 仓位控制：每只不超过总资金10%"
