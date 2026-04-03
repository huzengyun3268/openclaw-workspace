$att = "C:\Users\Administrator\Downloads\家谱模板_现代通用版.docx"
Send-MailMessage -From "66096170@qq.com" -To "66096170@qq.com" -Subject "家谱Word模板（现代通用版）" -Body "眼镜制作的家谱模板，内含以下内容：

1. 封面
2. 谱序
3. 凡例（8条体例说明）
4. 世系图（五世一表示例）
5. 行传格式（7列表格，含世次/姓名/字号/生卒/配偶/子女/简历）
6. 迁徙录
7. 家训族规（8条）
8. 大事记
9. 后记

用叉叉代替了所有人名，直接填入即可。" -Attachments $att -SmtpServer "smtp.qq.com" -Port 587 -UseSsl -Credential (New-Object System.Management.Automation.PSCredential("66096170@qq.com", (ConvertTo-SecureString "qsluszirhwibbhcb" -AsPlainText -Force)))
Write-Host "OK"
