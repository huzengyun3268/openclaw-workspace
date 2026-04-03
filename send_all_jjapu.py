# -*- coding: utf-8 -*-
import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

templates = [
    (b'\xe5\xae\xb6\xe8\xb0\xb1\xe6\xa8\xa1\xe6\x9d\xbf_\xe7\x8e\xb0\xe4\xbb\xa3\xe9\x80\x9a\xe7\x94\xa8\xe7\x89\x88.docx', '\u73b0\u4ee3\u901a\u7528\u7248'),
    (b'\xe5\xae\xb6\xe8\xb0\xb1\xe6\xa8\xa1\xe6\x9d\xbf_\xe6\xac\xa7\u5f0f\u7248.docx', '\u6b27\u5f0f\u7248'),
    (b'\xe5\xae\xb6\xe8\xb0\xb1\xe6\xa8\xa1\xe6\x9d\xbf_\xe8\x8b\x8f\u5f0f\u7248.docx', '\u82cf\u5f0f\u7248'),
    (b'\xe5\xae\xb6\xe8\xb0\xb1\xe6\xa8\xa1\xe6\x9d\xbf_\xe4\xbc\xa0\xe7\xbb\x9f\xe7\xab\x96\xe6\x8e\x92\u7248.docx', '\u4f20\u7edf\u7ad6\u6392\u7248'),
]

msg = MIMEMultipart()
msg['From'] = '66096170@qq.com'
msg['To'] = '66096170@qq.com'
msg['Subject'] = '\u5bb6\u8c31\u6a21\u677f\u5957\u88c5\uff084\u79cd\u683c\u5f0f\uff09'
body = '\u4e09\u79cd\u5bb6\u8c31\u6a21\u677f\uff1a\n1. \u73b0\u4ee3\u901a\u7528\u7248\uff1a\u6a21\u677f\u4f53\uff0c\u6b27\u5f0f\u4e16\u7cfb\u56fe+\u8868\u683c\u884c\u4f20\n2. \u6b27\u5f0f\u7248\uff1a\u4e94\u4e16\u4e00\u8868\uff0c\u6a21\u884c\u00b7\u4e16\u7cfb\u6e05\u6670\n3. \u82cf\u5f0f\u7248\uff1a\u5782\u73e0\u4f53\uff0c\u76f4\u7cfb\u4f53\u4f53\n4. \u4f20\u7edf\u7ad6\u6392\u7248\uff1a\u7ad6\u6392\u53f3\u7ffb\uff0c\u7e41\u4f53\u5b57\n\n\u6240\u6709\u6a21\u677f\u5747\u7528XX\u4ee3\u66ff\u4eba\u540d\uff0c\u76f4\u63a5\u586b\u5165\u5373\u53ef\u3002'
msg.attach(MIMEText(body, 'plain', 'utf-8'))

download_dir = 'C:/Users/Administrator/Downloads/'
for fname_bytes, desc in templates:
    fname = fname_bytes.decode('utf-8')
    fpath = os.path.join(download_dir, fname)
    if os.path.exists(fpath):
        with open(fpath, 'rb') as f:
            part = MIMEApplication(f.read(), Name=desc + '.docx')
        part['Content-Disposition'] = f'attachment; filename="{desc}.docx"'
        msg.attach(part)
        print(f"Attached: {desc}")
    else:
        print(f"Not found: {fpath}")

server = smtplib.SMTP('smtp.qq.com', 587)
server.starttls()
server.login('66096170@qq.com', 'qsluszirhwibbhcb')
server.sendmail('66096170@qq.com', '66096170@qq.com', msg.as_string())
server.quit()
print("All sent!")
