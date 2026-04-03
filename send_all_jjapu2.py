# -*- coding: utf-8 -*-
import smtplib, os, glob
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Find all jiapu templates
download_dir = 'C:/Users/Administrator/Downloads/'
all_files = glob.glob(os.path.join(download_dir, '*.docx'))

msg = MIMEMultipart()
msg['From'] = '66096170@qq.com'
msg['To'] = '66096170@qq.com'
msg['Subject'] = '\u5bb6\u8c31\u6a21\u677f\u5957\u88c5\uff084\u79cd\u683c\u5f0f\uff09'
body = '\u4e09\u79cd\u5bb6\u8c31\u6a21\u677f\uff0c\u6240\u6709\u5747\u7528XX\u4ee3\u66ff\u4eba\u540d\uff0c\u76f4\u63a5\u586b\u5165\u5373\u53ef\u3002'
msg.attach(MIMEText(body, 'plain', 'utf-8'))

count = 0
for fpath in all_files:
    fname = os.path.basename(fpath)
    if 'jiapu' in fname.lower() or '\u5bb6\u8c31' in fname or '\u6a21\u677f' in fname or 'family' in fname.lower():
        with open(fpath, 'rb') as f:
            data = f.read()
        part = MIMEApplication(data, Name='jiapu_template.docx')
        part['Content-Disposition'] = f'attachment; filename="{fname}"'
        msg.attach(part)
        count += 1
        print(f"Attached: {fname}")

if count == 0:
    # Find newest docx files
    files_sorted = sorted(all_files, key=os.path.getmtime, reverse=True)
    for fpath in files_sorted[:4]:
        fname = os.path.basename(fpath)
        if 'RustDesk' not in fname and 'TeamViewer' not in fname:
            with open(fpath, 'rb') as f:
                data = f.read()
            part = MIMEApplication(data, Name=fname)
            part['Content-Disposition'] = f'attachment; filename="{fname}"'
            msg.attach(part)
            count += 1
            print(f"Attached (recent): {fname}")

print(f"Total attachments: {count}")

server = smtplib.SMTP('smtp.qq.com', 587)
server.starttls()
server.login('66096170@qq.com', 'qsluszirhwibbhcb')
server.sendmail('66096170@qq.com', '66096170@qq.com', msg.as_string())
server.quit()
print("All sent!")
