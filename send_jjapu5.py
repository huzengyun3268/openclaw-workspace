# -*- coding: utf-8 -*-
import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

att_path = 'C:/Users/Administrator/Downloads/\u5bb6\u8c31\u6a21\u677f_\u73b0\u4ee3\u901a\u7528\u7248.docx'

msg = MIMEMultipart()
msg['From'] = '66096170@qq.com'
msg['To'] = '66096170@qq.com'
msg['Subject'] = '\u5bb6\u8c31Word\u6a21\u677f\uff08\u73b0\u4ee3\u901a\u7528\u7248\uff09'
body = '\u5bb6\u8c31\u6a21\u677f\uff0c\u7528\u53c9\u53c9\u4ee3\u66ff\u6240\u6709\u4eba\u540d\uff0c\u4e0b\u8f7d\u540e\u76f4\u63a5\u586b\u5165\u5373\u53ef\u3002\u5305\u542b\u5c01\u9762\u3001\u8c31\u5e8f\u3001\u51e1\u4f8b\u3001\u4e16\u7cfb\u56fe\u3001\u884c\u4f20\u683c\u5f0f\u3001\u8fc1\u5c99\u5f55\u3001\u5bb6\u8bad\u65cf\u89c4\u3001\u5927\u4e8b\u8bb0\u3001\u540e\u8bb0\u3002'
msg.attach(MIMEText(body, 'plain', 'utf-8'))

if os.path.exists(att_path):
    with open(att_path, 'rb') as f:
        part = MIMEApplication(f.read(), Name='jiapu.docx')
    part['Content-Disposition'] = 'attachment; filename="jiapu.docx"'
    msg.attach(part)
    print(f"Found: {att_path}")
else:
    print("NOT found")

server = smtplib.SMTP('smtp.qq.com', 587)
server.starttls()
server.login('66096170@qq.com', 'qsluszirhwibbhcb')
server.sendmail('66096170@qq.com', '66096170@qq.com', msg.as_string())
server.quit()
print("Sent to QQ mail OK!")
