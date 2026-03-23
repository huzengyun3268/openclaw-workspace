const nodemailer = require('nodemailer');
const fs = require('fs');
const path = require('path');

const body = fs.readFileSync(path.join(__dirname, '..', 'reports', 'amazon_holiday_lights_report.md'), 'utf8');

const transporter = nodemailer.createTransport({
  host: 'smtp.qq.com',
  port: 587,
  secure: false,
  auth: {
    user: '66096170@qq.com',
    pass: 'qsluszirhwibbhcb'
  }
});

const mailOptions = {
  from: '66096170@qq.com',
  to: '66096170@qq.com',
  subject: '亚马逊节日灯创业可行性分析报告',
  text: body
};

transporter.sendMail(mailOptions, (err, info) => {
  if (err) {
    console.error('Error:', err.message);
  } else {
    console.log('OK - Message sent:', info.response);
  }
});
