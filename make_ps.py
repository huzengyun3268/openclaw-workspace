content = """Add-Type -AssemblyName System.Net.Mail
Add-Type -AssemblyName System.Net
$from = '66096170@qq.com'
$to = '66096170@qq.com'
$body = [System.Text.Encoding]::UTF8.GetString([byte[]](230,136,145,229,173,151,232,191,153,232,175,149,230,156,159,230,150,185,32,240,159,146,162,32,229,144,141,231,148,168,230,135,125,229,156,159,32,232,140,145,232,186,165,32,232,161,179,32,231,154,176,228,184,128,232,175,149,236,185,148))
$msg = New-Object System.Net.Mail.MailMessage($from, $to, 'DALANGKENG', $body)
$attachment = New-Object System.Net.Mail.Attachment('C:\\Users\\Administrator\\Desktop\\大浪坑泳字幕版.mp4')
$msg.Attachments.Add($attachment)
$smtp = New-Object System.Net.Mail.SmtpClient('smtp.qq.com', 587)
$smtp.EnableSsl = $true
$smtp.Credentials = New-Object System.Net.NetworkCredential('66096170@qq.com', 'qsluszirhwibbhcb')
$smtp.Send($msg)
Write-Host 'OK'
"""
with open(r'C:\Users\Administrator\.openclaw\workspace\send_video_email.ps1', 'w', encoding='utf-8-sig') as f:
    f.write(content)
print('done')
