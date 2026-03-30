Add-Type -AssemblyName System.Net.Mail
$smtp = New-Object System.Net.Mail.SmtpClient
$smtp.Host = "smtp.qq.com"
$smtp.Port = 587
$smtp.EnableSsl = $true
$smtp.Credentials = New-Object System.Net.NetworkCredential("66096170@qq.com", "qsluszirhwibbhcb")
$msg = New-Object System.Net.Mail.MailMessage
$msg.From = "66096170@qq.com"
$msg.To.Add("66096170@qq.com")
$utf8 = [System.Text.Encoding]::UTF8
$plainText = [System.IO.File]::ReadAllText("C:\Users\Administrator\.openclaw\workspace\war_body.txt", $utf8)
$av = New-Object System.Net.Mail.AlternateView([System.IO.MemoryStream]::new($utf8.GetBytes($plainText)), "text/plain; charset=`"UTF-8`"")
$msg.AlternateViews.Add($av)
$msg.Subject = "=?UTF-8?B?5LiA5aWL5aSq5aSp5aSn5aSq5aSP5aSP5aSn5aSl5aSq5aSl5aSo5aSnIDIwMjYtMDMtMzA=?="
$msg.SubjectEncoding = $utf8
$smtp.Send($msg)
Write-Host "DONE"
