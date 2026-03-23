const nodemailer = require('nodemailer');
const fs = require('fs');

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
  subject: '【胡仲翰简历Word版】海康微影—海外营销推广专员',
  text: '胡仲翰简历Word版，详见附件，可直接转发给熟人或HR。\n\n简历亮点：\n- 布里斯托大学QS55硕士\n- 雅思7.0，海外业务能力强\n- 有独立站运营+海外KOL对接经验\n- 意向岗位：海康微影—海外营销推广专员',
  attachments: [
    {
      filename: '胡仲翰_简历_海康微影.docx',
      path: 'C:\\Users\\Administrator\\.openclaw\\workspace\\胡仲翰_简历_海康微影.docx'
    }
  ]
};

transporter.sendMail(mailOptions, (err, info) => {
  if (err) {
    console.error('Error:', err.message);
  } else {
    console.log('OK - Message sent:', info.response);
  }
});
