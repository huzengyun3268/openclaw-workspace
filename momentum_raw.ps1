$url = "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=10&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:90+t:2&fields=f2,f3,f12,f14&cb=jQuery"
$bytes = Invoke-WebRequest -Uri $url -Headers @{'User-Agent'='Mozilla/5.0'} -TimeoutSec 8 -ResponseHeadersFormat Byte
[System.IO.File]::WriteAllBytes("$env:TEMP\sector_raw.txt", $bytes)
Write-Output "Saved sector data"

$url2 = "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=10&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fields=f2,f3,f12,f14&cb=jQuery"
$bytes2 = Invoke-WebRequest -Uri $url2 -Headers @{'User-Agent'='Mozilla/5.0'} -TimeoutSec 8 -ResponseHeadersFormat Byte
[System.IO.File]::WriteAllBytes("$env:TEMP\gainers_raw.txt", $bytes2)
Write-Output "Saved gainers data"
