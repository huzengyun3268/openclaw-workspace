import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

body_text = '\u7b14\u8bcd\u81ea\u5df1\u52a0\uff0c\u6b64\u7248\u4e3a\u7eaf\u51c0\u539f\u59cb\u7248\uff0c\u7528\u526a\u6620\u52a0\u5b57\u66f4\u597d\u770b'

msg = MIMEMultipart()
msg['From'] = '66096170@qq.com'
msg['To'] = '66096170@qq.com'
msg['Subject'] = 'DALANGKENG_CLEAN'
msg.attach(MIMEText(body_text, 'plain', 'utf-8'))

filepath = r'C:\Users\Administrator\Desktop\大浪坑泳纯净版.mp4'
with open(filepath, 'rb') as f:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="dalangkeng_clean.mp4"')
    msg.attach(part)

smtp = smtplib.SMTP('smtp.qq.com', 587)
smtp.ehlo()
smtp.starttls()
smtp.login('66096170@qq.com', 'qsluszirhwibbhcb')
smtp.sendmail('66096170@qq.com', '66096170@qq.com', msg.as_string())
smtp.quit()
print('OK')
