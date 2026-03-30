$utf8 = [System.Text.Encoding]::UTF8
$body = [System.IO.File]::ReadAllText("C:\Users\Administrator\.openclaw\workspace\war_body.txt", $utf8)
$bodyBytes = $utf8.GetBytes($body)
$encodedBody = [Convert]::ToBase64String($bodyBytes)
$bodyWithCharset = "=?UTF-8?B?$encodedBody`?="

$smtp = New-Object Net.Mail.SmtpClient("smtp.qq.com", 587)
$smtp.EnableSsl = $true
$smtp.Credentials = New-Object Net.NetworkCredential("66096170@qq.com", "qsluszirhwibbhcb")

$mail = New-Object Net.Mail.MailMessage
$mail.From = "66096170@qq.com"
$mail.To.Add("66096170@qq.com")
$mail.Subject = "=?UTF-8?B?5LiA5aWL5aSq5aSp5aSn5aSq5aSP5aSP5aSn5aSl5aSq5aSl5aSo5aSnIDIwMjYtMDMtMzA=?="
$mail.SubjectEncoding = $utf8
$mail.Body = $body
$mail.BodyEncoding = $utf8
$mail.IsBodyHtml = $false

# Set charset in headers manually
$mail.Headers.Add("Content-Type", "text/plain; charset=UTF-8")

$smtp.Send($mail)
Write-Host "OK"
