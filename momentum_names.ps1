# Try different encoding - UTF-8 with GBK fallback
Write-Output "=== SECTOR NAMES (UTF8->GBK->UTF8 roundtrip) ==="
$url = "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=10&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:90+t:2&fields=f2,f3,f12,f14&cb=jQuery"
$r = Invoke-WebRequest -Uri $url -Headers @{'User-Agent'='Mozilla/5.0'} -TimeoutSec 8
# Try to decode as GBK
$gbk = [System.Text.Encoding]::GetEncoding('GBK').GetString($r.Content)
$j = $gbk -replace 'jQuery\(|\)\s*;?\s*$','' | ConvertFrom-Json
$j.data.diff | ForEach-Object { Write-Output "$($_.f12) | $($_.f14) | $($_.f3)%" }

Write-Output "=== TOP GAINER NAMES ==="
$url2 = "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=10&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fields=f2,f3,f12,f14&cb=jQuery"
$r2 = Invoke-WebRequest -Uri $url2 -Headers @{'User-Agent'='Mozilla/5.0'} -TimeoutSec 8
$gbk2 = [System.Text.Encoding]::GetEncoding('GBK').GetString($r2.Content)
$j2 = $gbk2 -replace 'jQuery\(|\)\s*;?\s*$','' | ConvertFrom-Json
$j2.data.diff | ForEach-Object { Write-Output "$($_.f12) | $($_.f14) | $($_.f3)%" }
