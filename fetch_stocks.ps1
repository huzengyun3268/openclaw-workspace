$ErrorActionPreference = "SilentlyContinue"
$headers = @{}
$headers["User-Agent"] = "Mozilla/5.0"

$stocks = @{}
$stocks["600352"] = [char]::ConvertFromUtf32(0x6D59) + [char]::ConvertFromUtf32(0x6C5F) + [char]::ConvertFromUtf32(0x9F99) + [char]::ConvertFromUtf32(0x76DB)
$stocks["300033"] = [char]::ConvertFromUtf32(0x540C) + [char]::ConvertFromUtf32(0x82B1) + [char]::ConvertFromUtf32(0x987A)
$stocks["000988"] = [char]::ConvertFromUtf32(0x534E) + [char]::ConvertFromUtf32(0x5DE5) + [char]::ConvertFromUtf32(0x79D1) + [char]::ConvertFromUtf32(0x6280)
$stocks["688295"] = [char]::ConvertFromUtf32(0x4E2D) + [char]::ConvertFromUtf32(0x590D) + [char]::ConvertFromUtf32(0x795E) + [char]::ConvertFromUtf32(0x9E4F)
$stocks["600487"] = [char]::ConvertFromUtf32(0x4EA4) + [char]::ConvertFromUtf32(0x901A) + [char]::ConvertFromUtf32(0x5149) + [char]::ConvertFromUtf32(0x7535)
$stocks["300499"] = [char]::ConvertFromUtf32(0x9AD8) + [char]::ConvertFromUtf32(0x6F6E) + [char]::ConvertFromUtf32(0x80A1) + [char]::ConvertFromUtf32(0x4EFD)
$stocks["601168"] = [char]::ConvertFromUtf32(0x897F) + [char]::ConvertFromUtf32(0x90E8) + [char]::ConvertFromUtf32(0x77FF) + [char]::ConvertFromUtf32(0x4E1A)
$stocks["600893"] = [char]::ConvertFromUtf32(0x822A) + [char]::ConvertFromUtf32(0x53D1) + [char]::ConvertFromUtf32(0x52A8) + [char]::ConvertFromUtf32(0x529B)

$results = @()
foreach ($code in $stocks.Keys) {
    if ($code.StartsWith("6")) {
        $secid = "1.$code"
    } else {
        $secid = "0.$code"
    }
    
    $url = "https://push2.eastmoney.com/api/qt/stock/get?secid=$secid&fields=f43,f57,f58,f169&ut=fa5fd1943c7b386f172d6893dbfba10b&fltt=2&invt=2"
    
    try {
        $resp = Invoke-WebRequest -Uri $url -Headers $headers -TimeoutSec 8
        $json = $resp.Content | ConvertFrom-Json
        $data = $json.data
        if ($data) {
            $price = $data.f43 / 100
            $chgPct = $data.f169 / 100
            $name = $stocks[$code]
            $results += "$name($code): $price ($([math]::Round($chgPct,2))%)"
        }
    } catch {
        $results += "$($stocks[$code])($code): Get failed"
    }
}

foreach ($r in $results) {
    Write-Output $r
}
