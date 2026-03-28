const https = require('https');
const fs = require('fs');
const path = require('path');

const videoPath = 'C:/Users/Administrator/Desktop/war_video_0326.mp4';
const fileName = 'war_video_0326.mp4';
const fileSize = fs.statSync(videoPath).size;
const fileContent = fs.readFileSync(videoPath);

console.log(`Uploading ${fileName} (${(fileSize/1024/1024).toFixed(1)} MB)...`);

const boundary = '----FormBoundary' + Math.random().toString(36).substring(2);

const body = Buffer.concat([
  Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="file"; filename="${fileName}"\r\nContent-Type: video/mp4\r\n\r\n`),
  fileContent,
  Buffer.from(`\r\n--${boundary}--\r\n`)
]);

const options = {
  hostname: 'file.io',
  path: '/',
  method: 'POST',
  headers: {
    'Content-Type': `multipart/form-data; boundary=${boundary}`,
    'Content-Length': body.length,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
  }
};

const req = https.request(options, (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    console.log('Status:', res.statusCode);
    console.log('Response:', data);
  });
});

req.on('error', (e) => {
  console.error('Error:', e.message);
});

req.write(body);
req.end();
