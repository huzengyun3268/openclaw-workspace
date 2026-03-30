$utf8 = [System.Text.Encoding]::UTF8
$body = [System.IO.File]::ReadAllText("C:\Users\Administrator\.openclaw\workspace\war_body.txt", $utf8)

$smtp = New-Object Net.Mail.SmtpClient("smtp.qq.com", 587)
$smtp.EnableSsl = $true
$smtp.Credentials = New-Object Net.NetworkCredential("66096170@qq.com", "qsluszirhwibbhcb")

$mail = New-Object Net.Mail.MailMessage
$mail.From = "66096170@qq.com"
$mail.To.Add("66096170@qq.com")
$mail.Subject = "War Day30 US-Israel-Iran 2026-03-30"
$mail.SubjectEncoding = $utf8
$mail.Body = $body
$mail.BodyEncoding = $utf8
$mail.IsBodyHtml = $false

$smtp.Send($mail)
Write-Host "OK"
