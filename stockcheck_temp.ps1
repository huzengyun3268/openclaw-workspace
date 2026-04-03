$ErrorActionPreference = 'SilentlyContinue'
$stocks = @(
    ('sh600352', '浙江龙盛'),
    ('sz300033', '同花顺'),
    ('sh600487', '亨通光电'),
    ('sh600893', '航发动力'),
    ('sh601168', '西部矿业'),
    ('sh518880', '黄金ETF'),
    ('sz430046', '圣博润'),
    ('sh600114', '东睦股份'),
    ('sh600089', '特变电工')
)

Write-Host "=== 持仓监控 2026-04-02 13:30 ==="
Write-Host ""

foreach ($s in $stocks) {
    $code = $s[0]
    $name = $s[1]
    try {
        $url = "https://qt.gtimg.cn/q=$code"
        $resp = Invoke-WebRequest -Uri $url -UserAgent "Mozilla/5.0" -TimeoutSec 5
        $data = [System.Text.Encoding]::GetEncoding('GBK').GetString($resp.Content)
        $parts = $data -split '~'
        if ($parts.Count -gt 4) {
            $price = $parts[3]
            $pct = if ($parts.Count -gt 32) { $parts[32] } else { "0" }
            Write-Host "$name($code): 现价=$price  涨跌%=$pct"
        } else {
            Write-Host "$name($code): 数据解析失败"
        }
    } catch {
        Write-Host "$name($code): 获取失败 - $($_.Exception.Message)"
    }
}
