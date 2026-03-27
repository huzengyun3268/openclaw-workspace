# Stock Multi-Source Monitor v2 - 沪深+北交所全覆盖
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Get-StockPrice {
    param([string]$code)
    $result = @{success=$false; price=$null; pct=$null; volume=$null; source=""; error=""; name=""}

    # Determine prefix
    $isSz = $code -match "^000|^001|^002|^003|^300|^301|^302|^080|^399"
    $isBj = $code -match "^920"
    if ($isSz) { $prefix = "sz" }
    elseif ($isBj) { $prefix = "bj" }
    else { $prefix = "sh" }
    $apiCode = "${prefix}${code}"

    # 1. Tencent
    try {
        $url = "https://qt.gtimg.cn/q=$apiCode"
        $req = [System.Net.WebRequest]::Create($url)
        $req.UserAgent = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)"
        $req.Timeout = 6000
        $resp = $req.GetResponse()
        $stream = $resp.GetResponseStream()
        $sr = New-Object System.IO.StreamReader($stream, [System.Text.Encoding]::UTF8)
        $data = $sr.ReadToEnd(); $sr.Close(); $resp.Close()
        $parts = $data.Split('~')
        if ($parts.Length -gt 35 -and $parts[1] -ne "pv_none_match" -and $parts[3] -ne "" -and $parts[3] -ne "0") {
            $result.success = $true; $result.price = [double]$parts[3]
            $result.pct = [double]$parts[32]; $result.volume = $parts[6]
            $result.name = $parts[1]; $result.source = "Tencent"
            return $result
        }
    } catch {}

    # 2. EastMoney
    try {
        if ($isSz) { $mkt = 0 } elseif ($isBj) { $mkt = 50 } else { $mkt = 1 }
        $url = "https://push2.eastmoney.com/api/qt/stock/get?fields=f43,f57,f58,f170,f47&secid=${mkt}.${code}&ut=fa5fd1943c7b386f172d6893dbfba10b"
        $req = [System.Net.WebRequest]::Create($url)
        $req.UserAgent = "Mozilla/5.0"; $req.Timeout = 6000
        $req.Referer = "https://quote.eastmoney.com/"
        $resp = $req.GetResponse()
        $stream = $resp.GetResponseStream()
        $jr = New-Object System.IO.StreamReader($stream, [System.Text.Encoding]::UTF8)
        $jd = [System.Text.Json.JsonDocument]::Parse($jr.ReadToEnd())
        $jr.Close(); $resp.Close()
        $d = $jd.RootElement.GetProperty("data")
        $result.success = $true
        $result.price = [double]($d.GetProperty("f43").GetInt64()) / 100
        $result.pct = [double]($d.GetProperty("f170").GetInt64()) / 100
        $result.volume = $d.GetProperty("f47").GetString()
        $result.name = $d.GetProperty("f58").GetString(); $result.source = "EastMoney"
        return $result
    } catch {}

    # 3. Sina
    try {
        $sinaCode = if ($isBj) { "bj${code}" } elseif ($isSz) { "sz${code}" } else { "sh${code}" }
        $url = "https://hq.sinajs.cn/list=${sinaCode}"
        $req = [System.Net.WebRequest]::Create($url)
        $req.UserAgent = "Mozilla/5.0"; $req.Timeout = 6000
        $req.Headers["Referer"] = "https://finance.sina.com.cn"
        $resp = $req.GetResponse()
        $stream = $resp.GetResponseStream()
        $sr = New-Object System.IO.StreamReader($stream, [System.Text.Encoding]::GetEncoding("GB2312"))
        $data = $sr.ReadToEnd(); $sr.Close(); $resp.Close()
        if ($data -match "=""([^""]+)""") {
            $f = $matches[1].Split(',')
            if ($f.Length -gt 5 -and $f[3] -ne "" -and $f[3] -ne "0") {
                $result.success = $true; $result.price = [double]$f[3]
                if ([double]$f[2] -ne 0) { $result.pct = [Math]::Round(([double]$f[3] - [double]$f[2]) / [double]$f[2] * 100, 2) }
                $result.name = $f[0]; $result.source = "Sina"
                return $result
            }
        }
    } catch {}

    $result.error = "3sources failed"; return $result
}

# Query all holdings
Write-Host "=== Multi-Source Monitor v2 === $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
Write-Host ""

$holdings = @(
    @{code="600352"; name="ZheJiangLongSheng"; cost=16.52; stop=12.0},
    @{code="600893"; name="HangFaDongLi"; cost=49.184; stop=42.0},
    @{code="300033"; name="TongHuaShun"; cost=423.488; stop=280},
    @{code="601168"; name="XiBuKuangYe"; cost=26.169; stop=22.0},
    @{code="600487"; name="HengTongGuangDian"; cost=43.998; stop=38.0},
    @{code="688295"; name="ZhongFuShenYing"; cost=37.843; stop=0},
    @{code="920046"; name="YiNengDianLi"; cost=329.553; stop=27; note="BSE"},
    @{code="831330"; name="PuShiDaoHang"; cost=20.361; stop=18.0; note="NEEQ"},
    @{code="430046"; name="ShengBoRun"; cost=0.478; stop=0; note="NEEQ"}
)

foreach ($s in $holdings) {
    $r = Get-StockPrice -code $s.code
    if ($r.success) {
        $arrow = if ($r.pct -ge 0) { "+" } else { "" }
        if ($s.stop -gt 0) {
            $dist = [Math]::Round(($r.price - $s.stop) / $s.stop * 100, 1)
            $stopInfo = "STOP=$($s.stop) dist=${dist}%"
        } else { $stopInfo = "no-stop" }
        $note = if ($s.note) { "[$($s.note)]" } else { "" }
        $src = if ($r.source -ne "Tencent") { "<$($r.source)>" } else { "" }
        Write-Host "$($s.name): $($r.price) ${arrow}$($r.pct)% ${src} ${stopInfo} ${note}"
    } else {
        Write-Host "$($s.name): DATA-FAILED"
    }
}
