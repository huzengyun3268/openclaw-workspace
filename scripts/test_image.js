// Test image generation via the OpenClaw completion endpoint
const https = require('https');

const apiKey = 'sk-cp-FPLfpyTxxDktH6V9nqDqm9_0Ya4';
const body = JSON.stringify({
  model: 'image-01',
  messages: [{role: 'user', content: 'a cat wearing sunglasses'}]
});

const options = {
  hostname: 'api.minimaxi.chat',
  path: '/v1/chat/completions',
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(body)
  }
};

const req = https.request(options, (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    console.log('Status:', res.statusCode);
    console.log('Response:', data.substring(0, 500));
  });
});
req.on('error', e => console.error('Error:', e));
req.write(body);
req.end();
