$ErrorActionPreference = 'SilentlyContinue'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$url = "https://qt.gtimg.cn/q=sh600352,sz300033,sh600487,sh600893,sh601168,sh518880,sh600114,sh600089,sz002471,sh688011,sz002491,sh601318,sh600256,sh600522"
$response = Invoke-WebRequest -Uri $url -TimeoutSec 10
$content = $response.Content
$lines = $content -split "`n"
$out = New-Object System.Text.StringBuilder
foreach ($line in $lines) {
    $fields = $line -split '~'
    if ($fields.Length -gt 32) {
        $code = $fields[0].Replace('v_','').Trim()
        $name = $fields[1]
        $price = $fields[3]
        $prev = $fields[4]
        $pct = $fields[32]
        $null = $out.AppendLine("$code|$name|$price|$prev|$pct")
    }
}
[System.IO.File]::WriteAllText("C:\Users\Administrator\.openclaw\workspace\stock_data_utf.txt", $out.ToString(), [System.Text.Encoding]::UTF8)
Write-Host "Done"
