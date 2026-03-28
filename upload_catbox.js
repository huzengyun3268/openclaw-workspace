const https = require('https');
const fs = require('fs');

const videoPath = 'C:/Users/Administrator/Desktop/war_video_0326.mp4';
const fileName = 'war_video_0326.mp4';
const fileSize = fs.statSync(videoPath).size;
const fileContent = fs.readFileSync(videoPath);

console.log(`Uploading ${fileName} (${(fileSize/1024/1024).toFixed(1)} MB)...`);

const boundary = '----FormBoundary' + Math.random().toString(36).substring(2);

const body = Buffer.concat([
  Buffer.from(`--${boundary}\r\n`),
  Buffer.from(`Content-Disposition: form-data; name="reqtype"\r\n\r\n`),
  Buffer.from(`fileupload\r\n`),
  Buffer.from(`--${boundary}\r\n`),
  Buffer.from(`Content-Disposition: form-data; name="fileToUpload\"; filename="${fileName}"\r\nContent-Type: video/mp4\r\n\r\n`),
  fileContent,
  Buffer.from(`\r\n--${boundary}--\r\n`)
]);

const options = {
  hostname: 'catbox.moe',
  path: '/resources/internals/api/LocalFileUpload.php',
  method: 'POST',
  headers: {
    'Content-Type': `multipart/form-data; boundary=${boundary}`,
    'Content-Length': body.length,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
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
