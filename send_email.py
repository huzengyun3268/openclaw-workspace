import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from_addr = '66096170@qq.com'
to_addr = '66096170@qq.com'
subject = 'DALANGKENG'
body = '视频见附件，字幕已加好 😎'

msg = MIMEMultipart()
msg['From'] = from_addr
msg['To'] = to_addr
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain', 'utf-8'))

filepath = r'C:\Users\Administrator\Desktop\大浪坑泳字幕版.mp4'
filename = '大浪坑泳字幕版.mp4'
with open(filepath, 'rb') as f:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
    msg.attach(part)

smtp = smtplib.SMTP('smtp.qq.com', 587)
smtp.ehlo()
smtp.starttls()
smtp.login(from_addr, 'qsluszirhwibbhcb')
smtp.sendmail(from_addr, to_addr, msg.as_string())
smtp.quit()
print('OK')
