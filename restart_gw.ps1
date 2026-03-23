$gw = Get-Process | Where-Object { $_.CommandLine -like "*openclaw*" -and $_.CommandLine -like "*gateway*" }
if ($gw) {
    Write-Host "Stopping gateway pid $($gw.Id)..."
    Stop-Process $gw.Id -Force
    Start-Sleep 3
}
Write-Host "Starting gateway..."
Start-Process node -ArgumentList "C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw\openclaw.mjs","gateway","start" -WindowStyle Hidden
Start-Sleep 3
Write-Host "Done. Gateway should be restarting."
