const nodemailer = require('nodemailer');

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
  subject: 'War Video Day 26',
  text: 'This is a test email. Please check attachment.',
  attachments: [{
    filename: 'war_video_0326.mp4',
    path: 'C:/Users/Administrator/Desktop/war_video_0326.mp4',
    contentType: 'video/mp4'
  }]
};

transporter.sendMail(mailOptions, (err, info) => {
  if (err) {
    console.log('FAILED:', err.message);
  } else {
    console.log('SUCCESS');
  }
});
