$att = "C:\Users\Administrator\Downloads\家谱模板_现代通用版.docx"
$smtp = New-Object Net.Mail.SmtpClient("smtp.qq.com", 587)
$smtp.EnableSsl = $true
$smtp.Credentials = New-Object Net.NetworkCredential("66096170@qq.com", "qsluszirhwibbhcb")
$mail = New-Object Net.Mail.MailMessage
$mail.From = "66096170@qq.com"
$mail.To.Add("huzengyun@hotmail.com")
$utf8 = [System.Text.Encoding]::UTF8
$mail.Subject = "家谱Word模板（现代通用版）"
$mail.SubjectEncoding = $utf8
$mail.Body = "家谱模板用叉叉代替所有人名，下载后直接填入即可。包含封面、谱序、凡例、世系图、行传格式、迁徙录、家训族规、大事记、后记。"
$mail.BodyEncoding = $utf8
if (Test-Path $att) {
    $att2 = New-Object Net.Mail.Attachment($att)
    $mail.Attachments.Add($att2)
}
$smtp.Send($mail)
Write-Host "OK"
