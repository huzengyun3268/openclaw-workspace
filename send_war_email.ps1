$body = Get-Content "C:\Users\Administrator\.openclaw\workspace\war_body.txt" -Raw
Send-MailMessage -From "66096170@qq.com" -To "66096170@qq.com" -Subject "【第30天战况】美以伊战争实况 2026-03-30" -Body $body -SmtpServer "smtp.qq.com" -Port 587 -UseSsl -Credential (New-Object System.Management.Automation.PSCredential("66096170@qq.com", (ConvertTo-SecureString "qsluszirhwibbhcb" -AsPlainText -Force)))
Write-Host "DONE"
