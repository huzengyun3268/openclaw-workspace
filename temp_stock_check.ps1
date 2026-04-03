[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$pos = @(
  @{code='sh600352';name='浙江龙盛';vol=86700;cost=16.52;stop=12.0},
  @{code='sh600893';name='航发动力';vol=9000;cost=49.184;stop=42.0},
  @{code='sz300033';name='同花顺';vol=1200;cost=423.488;stop=280.0},
  @{code='sh601168';name='西部矿业';vol=11000;cost=26.169;stop=22.0},
  @{code='bj831330';name='普适导航';vol=7370;cost=20.361;stop=18.0},
  @{code='sh600487';name='亨通光电';vol=4000;cost=45.47;stop=38.0},
  @{code='sh688295';name='中复神鹰';vol=3000;cost=56.85;stop=0},
  @{code='sz430046';name='圣博润';vol=10334;cost=0.478;stop=0}
)
$wife = @(
  @{code='sh600114';name='东睦股份';vol=4900;cost=31.681;stop=25.0}
)
$margin = @(
  @{code='sh600089';name='特变电工';vol=52300;cost=24.765;stop=25.0}
)

$all_codes = (($pos+$wife+$margin) | ForEach-Object { $_.code }) -join ','

try {
  $wc = New-Object System.Net.WebClient
  $wc.Encoding = [System.Text.Encoding]::UTF8
  $html = $wc.DownloadString("https://qt.gtimg.cn/q=$all_codes")
  $lines = $html -split "`n"
  $pm = @{}
  foreach ($l in $lines) {
    if ($l -match 'hq_str_[a-z]+\d+="([^"]+)"') {
      $parts = $matches[1] -split '~'
      if ($parts.Count -ge 4) {
        $code_raw = $parts[0]
        $price = [double]$parts[3]
        if ($code_raw -and $price -gt 0) { $pm[$code_raw] = $price }
      }
    }
  }
  $wc.Dispose()
} catch { "Error fetching data: $_" }

$output = @()
foreach ($p in $pos) {
  $price = $pm[$p.code]
  if ($price) {
    $gain = [math]::Round(($price - $p.cost) * $p.vol, 0)
    $gainPct = [math]::Round((($price / $p.cost) - 1) * 100, 2)
    $stopped = ($p.stop -gt 0 -and $price -le $p.stop)
    $output += [PSCustomObject]@{
      Account='主账户'
      Name=$p.name
      Code=$p.code
      Vol=$p.vol
      Cost=$p.cost
      Price=$price
      Gain=$gain
      GainPct=$gainPct
      Stop=$p.stop
      Stopped=$stopped
    }
  }
}
foreach ($p in $wife) {
  $price = $pm[$p.code]
  if ($price) {
    $gain = [math]::Round(($price - $p.cost) * $p.vol, 0)
    $gainPct = [math]::Round((($price / $p.cost) - 1) * 100, 2)
    $stopped = ($p.stop -gt 0 -and $price -le $p.stop)
    $output += [PSCustomObject]@{
      Account='老婆账户'
      Name=$p.name
      Code=$p.code
      Vol=$p.vol
      Cost=$p.cost
      Price=$price
      Gain=$gain
      GainPct=$gainPct
      Stop=$p.stop
      Stopped=$stopped
    }
  }
}
foreach ($p in $margin) {
  $price = $pm[$p.code]
  if ($price) {
    $gain = [math]::Round(($price - $p.cost) * $p.vol, 0)
    $gainPct = [math]::Round((($price / $p.cost) - 1) * 100, 2)
    $stopped = ($p.stop -gt 0 -and $price -le $p.stop)
    $output += [PSCustomObject]@{
      Account='两融账户'
      Name=$p.name
      Code=$p.code
      Vol=$p.vol
      Cost=$p.cost
      Price=$price
      Gain=$gain
      GainPct=$gainPct
      Stop=$p.stop
      Stopped=$stopped
    }
  }
}

$output | Format-Table -AutoSize | Out-String -Width 300
