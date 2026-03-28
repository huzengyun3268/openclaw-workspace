const https = require('https');
const fs = require('fs');

const videoPath = 'C:/Users/Administrator/Desktop/war_video_0326.mp4';
const fileStream = fs.createReadStream(videoPath);

const req = https.request({
  hostname: '0x0.st',
  path: '/',
  method: 'POST',
  headers: {
    'Content-Type': 'application/octet-stream',
    'Content-Length': fs.statSync(videoPath).size,
    'User-Agent': 'Mozilla/5.0'
  }
}, (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    console.log('Status:', res.statusCode);
    console.log('URL:', data.trim());
  });
});

req.on('error', (e) => {
  console.error('Error:', e.message);
});

fileStream.pipe(req);
