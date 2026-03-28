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
  subject: '美以伊战事Day26视频 - 视频号素材',
  text: '老胡，视频号/抖音素材，见附件。封面图：war_cover_0326.png',
  attachments: [
    {
      filename: 'war_video_0326.mp4',
      path: 'C:/Users/Administrator/Desktop/war_video_0326.mp4'
    }
  ]
};

transporter.sendMail(mailOptions, (err, info) => {
  if (err) {
    console.log('FAILED:', err.message);
  } else {
    console.log('SUCCESS - sent:', info.response);
  }
});
