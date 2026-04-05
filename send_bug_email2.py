import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from_addr = '66096170@qq.com'
to_addr = 'steipete@gmail.com'
subject = 'Additional Info: Bug existed in older version but now fixed in latest update'

body = """Hi OpenClaw team,

Adding more details to my previous bug report:

The Care Mode TTS issue is a REGRESSION - it used to work fine in an earlier version of OpenClaw/WeChat channel, but stopped working after a recent update. This strongly suggests a recent code change introduced this regression.

The user's workflow before:
1. AI assistant sends a message
2. User taps once on the message
3. Care Mode reads it aloud automatically

After the update:
- Care Mode cannot read AI assistant messages at all
- User must copy the message, paste it back to the AI, and the AI's reply THEN becomes readable

This is a regression introduced by a recent update, not a long-standing limitation.

Please investigate what changed in the WeChat channel message format or API source type.

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
print('OK - Additional info sent')
