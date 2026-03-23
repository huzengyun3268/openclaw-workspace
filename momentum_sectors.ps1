# Hot sectors and top gainers
Write-Output "=== HOT SECTORS (Rise rate) ==="
$url3 = "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=10&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:90+t:2&fields=f2,f3,f4,f12,f14&cb=jQuery"
$r3 = Invoke-WebRequest -Uri $url3 -Headers @{'User-Agent'='Mozilla/5.0'} -TimeoutSec 8
$j3 = $r3.Content -replace 'jQuery\(|\)\s*;?\s*$','' | ConvertFrom-Json
$j3.data.diff | ForEach-Object { Write-Output "Code: $($_.f12) | Name: $($_.f14) | Price: $($_.f2) | Chg%: $($_.f3)" }

Write-Output "=== TOP GAINERS (All A-share) ==="
$url4 = "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=10&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fields=f2,f3,f12,f14&cb=jQuery"
$r4 = Invoke-WebRequest -Uri $url4 -Headers @{'User-Agent'='Mozilla/5.0'} -TimeoutSec 8
$j4 = $r4.Content -replace 'jQuery\(|\)\s*;?\s*$','' | ConvertFrom-Json
$j4.data.diff | ForEach-Object { Write-Output "Code: $($_.f12) | Name: $($_.f14) | Price: $($_.f2) | Chg%: $($_.f3)" }

Write-Output "=== TOP LOSERS ==="
$url5 = "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=10&po=0&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fields=f2,f3,f12,f14&cb=jQuery"
$r5 = Invoke-WebRequest -Uri $url5 -Headers @{'User-Agent'='Mozilla/5.0'} -TimeoutSec 8
$j5 = $r5.Content -replace 'jQuery\(|\)\s*;?\s*$','' | ConvertFrom-Json
$j5.data.diff | ForEach-Object { Write-Output "Code: $($_.f12) | Name: $($_.f14) | Price: $($_.f2) | Chg%: $($_.f3)" }
