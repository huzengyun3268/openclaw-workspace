$OutputEncoding = [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$python = "python3"

$stocks = @(
    @{code="sz002471"; score="+35"; change="3.15%"},
    @{code="sh688011"; score="+35"; change="3.48%"},
    @{code="sz002491"; score="+25"; change="3.83%"},
    @{code="sh603387"; score="+10"; change="3.13%"},
    @{code="sz002431"; score="+10"; change="3.58%"},
    @{code="sh600186"; score="+10"; change="3.50%"},
    @{code="sz002246"; score="+10"; change="4.47%"},
    @{code="sh688802"; score="+10"; change="4.83%"},
    @{code="sh688667"; score="+10"; change="3.36%"},
    @{code="sz002181"; score="+5";  change="4.42%"}
)

foreach ($s in $stocks) {
    $url = "https://qt.gtimg.cn/q=$($s.code)"
    try {
        $resp = Invoke-WebRequest -Uri $url -TimeoutSec 5 -UserAgent "Mozilla/5.0"
        $raw = [System.Text.Encoding]::GetEncoding("GB18030").GetString($resp.Content)
        $parts = $raw -split '~'
        $name = if ($parts[1]) { $parts[1].Trim() } else { "N/A" }
        $price = if ($parts[3]) { $parts[3].Trim() } else { "N/A" }
        Write-Host "$($s.code) [$name] price=$price change=$($s.change) score=$($s.score)"
    } catch {
        Write-Host "$($s.code) ERROR: $($_.Exception.Message)"
    }
}
