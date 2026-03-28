const nodemailer = require('nodemailer');
const fs = require('fs');
const path = require('path');

const transporter = nodemailer.createTransport({
  host: 'smtp.qq.com',
  port: 587,
  secure: false,
  auth: {
    user: '66096170@qq.com',
    pass: 'qsluszirhwibbhcb'
  }
});

const videoPath = 'C:/Users/Administrator/Desktop/war_video_0326.mp4';
const filename = 'war_video_0326.mp4';
const fileContent = fs.readFileSync(videoPath);

const mailOptions = {
  from: '66096170@qq.com',
  to: '66096170@qq.com',
  subject: '美以伊战事Day26视频 - 视频号素材',
  text: '老胡，视频附件。手机用视频播放器打开（MX Player或相册视频功能）。封面图在桌面war_cover_0326.png。视频号：满船清梦8496',
  attachments: [{
    filename: filename,
    content: fileContent,
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
