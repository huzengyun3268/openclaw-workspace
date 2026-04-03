# -*- coding: utf-8 -*-
import smtplib, os, glob
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

msg = MIMEMultipart()
msg['From'] = '66096170@qq.com'
msg['To'] = '66096170@qq.com'
msg['Subject'] = '\u5bb6\u8c31\u6a21\u677f\u5957\u88c5\uff087\u79cd\u683c\u5f0f\uff09'
body = '\u5bb6\u8c31\u6a21\u677f\u7b2c\u4e8c\u6279\uff1a\n\n5. \u8788\u8bb0\u4f53\u7248\uff1a\u7eaf\u6587\u5b57\u6bb5\u843d\uff0c\u6bcf\u4eba\u4e00\u6bb5\uff0c\u6309\u4ee3\u6570\u7f16\u6398\n6. \u56fe\u6587\u6df7\u6392\u7248\uff1a\u6bcf\u4eba\u4e00\u9875\uff0c\u53ef\u63d2\u5165\u7167\u7247\n7. \u7b80\u6d01\u7248\uff1a\u8868\u683c\u4f53\uff0c\u4e00\u9875A4\u7eb9\u5c3e20\u884c\uff0c\u6700\u7b80\u6d01\n\n\u6240\u6709\u6a21\u677f\u5747\u7528XX\u4ee3\u66ff\u4eba\u540d\uff0c\u76f4\u63a5\u586b\u5165\u5373\u53ef\u3002'
msg.attach(MIMEText(body, 'plain', 'utf-8'))

download_dir = 'C:/Users/Administrator/Downloads/'
files = glob.glob(download_dir + 'jiapu*.docx')
print(f"Found {len(files)} files: {[os.path.basename(f) for f in files]}")

for fpath in files:
    fname = os.path.basename(fpath)
    with open(fpath, 'rb') as f:
        data = f.read()
    part = MIMEApplication(data, Name=fname)
    part['Content-Disposition'] = f'attachment; filename="{fname}"'
    msg.attach(part)
    print(f"Attached: {fname}")

server = smtplib.SMTP('smtp.qq.com', 587)
server.starttls()
server.login('66096170@qq.com', 'qsluszirhwibbhcb')
server.sendmail('66096170@qq.com', '66096170@qq.com', msg.as_string())
server.quit()
print(f"Total sent: {len(files)}")
