$att = "C:\Users\Administrator\Downloads\家谱模板_现代通用版.docx"
$msg = New-Object System.Net.Mail.MailMessage
$msg.From = "66096170@qq.com"
$msg.To.Add("huzengyun@hotmail.com")
$msg.Subject = "家谱Word模板（现代通用版）"
$msg.Body = "眼镜制作的家谱模板，内含：

1. 封面
2. 谱序
3. 凡例（8条体例说明）
4. 世系图（五世一表示例）
5. 行传格式（7列表格，含世次/姓名/字号/生卒/配偶/子女/简历）
6. 迁徙录
7. 家训族规（8条）
8. 大事记
9. 后记

用XX代替了所有人名，下载后直接填入即可。"

$utf8 = [System.Text.Encoding]::UTF8
$bodyBytes = $utf8.GetBytes($msg.Body)
$av = New-Object System.Net.Mail.AlternateView(([System.IO.MemoryStream]::new($bodyBytes)), "text/plain; charset=UTF-8")
$msg.AlternateViews.Add($av)

$smtp = New-Object System.Net.Mail.SmtpClient("smtp.qq.com", 587)
$smtp.EnableSsl = $true
$smtp.Credentials = New-Object System.Net.NetworkCredential("66096170@qq.com", "qsluszirhwibbhcb")

if (Test-Path $att) {
    $attachment = New-Object System.Net.Mail.Attachment($att, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    $msg.Attachments.Add($attachment)
}

$smtp.Send($msg)
Write-Host "OK - sent to huzengyun@hotmail.com"
