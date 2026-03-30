[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[System.Reflection.Assembly]::LoadWithPartialName('System.Net.Mail') | Out-Null

$body = Get-Content 'C:\Users\Administrator\.openclaw\workspace\report_body.txt' -Raw

$msg = New-Object System.Net.Mail.MailMessage
$msg.From = '66096170@qq.com'
$msg.To.Add('66096170@qq.com')
$msg.Subject = '=?UTF-8?B?' + [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes('持仓监控 2026-03-30 13:30')) + '?='
$msg.Body = $body
$msg.BodyEncoding = [System.Text.Encoding]::UTF8
$msg.IsBodyHtml = $false

$smtp = New-Object System.Net.Mail.SmtpClient
$smtp.Host = 'smtp.qq.com'
$smtp.Port = 587
$smtp.EnableSsl = $true
$smtp.Credentials = New-Object System.Net.NetworkCredential('66096170@qq.com', 'qsluszirhwibbhcb')

$smtp.Send($msg)
Write-Host 'Send OK'
