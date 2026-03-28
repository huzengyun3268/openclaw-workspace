const https = require('https');
const fs = require('fs');

const videoPath = 'C:/Users/Administrator/Desktop/war_video_0326.mp4';
const fileName = 'war_video_0326.mp4';
const fileSize = fs.statSync(videoPath).size;
const fileContent = fs.readFileSync(videoPath);

console.log(`Uploading ${fileName} (${(fileSize/1024/1024).toFixed(1)} MB)...`);

const boundary = '----WebKitFormBoundary' + Math.random().toString(36).substring(2);

const body = Buffer.concat([
  Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="file\"; filename="${fileName}"\r\nContent-Type: video/mp4\r\n\r\n`),
  fileContent,
  Buffer.from(`\r\n--${boundary}--\r\n`)
]);

// Try file.io with follow-redirect
function post(url, body, headers) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const opts = {
      hostname: u.hostname,
      path: u.pathname,
      method: 'POST',
      headers: {
        ...headers,
        'Content-Length': body.length,
        'User-Agent': 'Mozilla/5.0'
      }
    };
    const req = https.request(opts, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => resolve({status: res.statusCode, headers: res.headers, body: data}));
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

(async () => {
  // Try file.io
  try {
    const r = await post('https://file.io', body, {'Content-Type': `multipart/form-data; boundary=${boundary}`});
    console.log('file.io:', r.status, r.body.substring(0, 300));
  } catch(e) {
    console.log('file.io error:', e.message);
  }
})();
