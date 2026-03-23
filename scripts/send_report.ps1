Add-Type -AssemblyName System.Net.Mail
$msg = New-Object System.Net.Mail.MailMessage
$msg.From = '66096170@qq.com'
$msg.To.Add('66096170@qq.com')
$msg.Subject = '亚马逊节日灯创业可行性分析报告'
$body = [System.IO.File]::ReadAllText('C:\Users\Administrator\.openclaw\workspace\reports\amazon_holiday_lights_report.md', [System.Text.Encoding]::UTF8)
$msg.Body = $body
$msg.BodyEncoding = [System.Text.Encoding]::UTF8
$smtp = New-Object System.Net.Mail.SmtpClient('smtp.qq.com', 587)
$smtp.EnableSsl = $true
$smtp.Credentials = New-Object System.Net.NetworkCredential('66096170@qq.com', 'qsluszirhwibbhcb')
try {
    $smtp.Send($msg)
    Write-Host "OK"
} catch {
    Write-Host ("Error: " + $_.Exception.Message)
}
