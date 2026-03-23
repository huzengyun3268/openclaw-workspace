# Market index data
$url = 'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&fields=f2,f3,f4,f12,f14&secids=1.000001,0.399001,0.399006,1.000300&ut=b2884a393a59ad64002292a3e90d46a5'
$r = Invoke-WebRequest -Uri $url -Headers @{'User-Agent'='Mozilla/5.0'} -TimeoutSec 6
$j = $r.Content -replace 'jQuery\(|\)\s*;?\s*$','' | ConvertFrom-Json
Write-Output "=== MAJOR INDICES ==="
$j.data.diff | ForEach-Object { Write-Output "Code: $($_.f12) | Price: $($_.f2) | Chg%: $($_.f3) | ChgAmt: $($_.f4)" }

# User stock data
Write-Output "=== USER STOCKS ==="
$stockCodes = @('1.600352','1.600089','0.301667','0.920046','0.300033','0.831330','0.300189','0.430046','0.600114','0.301638')
$secids = $stockCodes -join ','
$url2 = "https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&fields=f2,f3,f4,f12,f14&secids=$secids&ut=b2884a393a59ad64002292a3e90d46a5"
$r2 = Invoke-WebRequest -Uri $url2 -Headers @{'User-Agent'='Mozilla/5.0'} -TimeoutSec 8
$j2 = $r2.Content -replace 'jQuery\(|\)\s*;?\s*$','' | ConvertFrom-Json
$j2.data.diff | ForEach-Object { Write-Output "Code: $($_.f12) | Price: $($_.f2) | Chg%: $($_.f3) | ChgAmt: $($_.f4)" }
