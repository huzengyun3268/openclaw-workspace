import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from_addr = '66096170@qq.com'
to_addr = 'steipete@gmail.com'
subject = 'Bug Report: WeChat Care Mode Cannot Read AI Assistant Messages'

body = """Hi OpenClaw Team,

I am an OpenClaw user via the WeChat channel.

Bug: When WeChat "Care Mode" (a text-to-speech feature for elderly users) is enabled, tapping on messages sent by the AI assistant does NOT trigger voice reading. Normal WeChat messages from other users work fine.

This is a critical accessibility issue for users who rely on Care Mode for hands-free reading while driving.

Temporary workaround: Copy the AI message, paste it back to the AI assistant, and the AI's reply will then be readable in Care Mode.

It would be great if this could be fixed so that WeChat Care Mode can properly read AI assistant messages.

Thanks!
"""

msg = MIMEMultipart()
msg['From'] = from_addr
msg['To'] = to_addr
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain', 'utf-8'))

smtp = smtplib.SMTP('smtp.qq.com', 587)
smtp.ehlo()
smtp.starttls()
smtp.login(from_addr, 'qsluszirhwibbhcb')
smtp.sendmail(from_addr, to_addr, msg.as_string())
smtp.quit()
print('OK - Bug report sent to steipete@gmail.com')
