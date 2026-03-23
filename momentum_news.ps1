# Get sector names properly
Write-Output "=== SECTOR DETAILS ==="
$url = "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=10&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:90+t:2&fields=f2,f3,f12,f14&cb=jQuery"
$r = Invoke-WebRequest -Uri $url -Headers @{'User-Agent'='Mozilla/5.0'} -TimeoutSec 8
$contentBytes = [System.Text.Encoding]::GetEncoding('GB2312').GetBytes($r.Content)
$content = [System.Text.Encoding]::UTF8.GetString($contentBytes)
$j = $content -replace 'jQuery\(|\)\s*;?\s*$','' | ConvertFrom-Json
$j.data.diff | ForEach-Object { Write-Output "Sector: $($_.f14) | Chg%: $($_.f3)" }

Write-Output "=== MARKET NEWS ==="
$newsUrl = "https://np-anotice-stock.eastmoney.com/api/security/ann?sr=-1&page_size=10&page_index=1&ann_type=SHA,CYB,SZA&client_source=web&stock=&f_node=0&s_node=0"
$nr = Invoke-WebRequest -Uri $newsUrl -Headers @{'User-Agent'='Mozilla/5.0'} -TimeoutSec 8
$nj = $nr.Content | ConvertFrom-Json
$nj.data.list | ForEach-Object { Write-Output "$($_.notice_date) | $($_.title)" }
