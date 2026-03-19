// 补抓新三板行情 - 使用腾讯API
const https = require('https');

async function fetchTencent(code) {
  return new Promise((resolve, reject) => {
    const fullCode = 'bj' + code;
    const url = `https://qt.gtimg.cn/q=${fullCode}`;
    https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' }}, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          console.log(`  raw for ${code}: ${data.substring(0, 200)}`);
          const match = data.match(/"([^"]+)"/);
          if (!match) return reject(new Error('No data'));
          const fields = match[1].split('~');
          if (fields.length < 40) return reject(new Error('Invalid: ' + fields.length + ' fields'));
          const price = parseFloat(fields[3]);
          const prevClose = parseFloat(fields[4]);
          const name = fields[1];
          const changePct = prevClose > 0 ? ((price - prevClose) / prevClose * 100).toFixed(2) : '0.00';
          resolve({ name, price: price.toFixed(3), change: changePct });
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

async function main() {
  for (const code of ['831330', '430046']) {
    try {
      const r = await fetchTencent(code);
      console.log(`${code}: name=${r.name}, price=${r.price}, change=${r.change}%`);
    } catch (e) {
      console.log(`${code}: failed - ${e.message}`);
    }
    await new Promise(r => setTimeout(r, 1000));
  }
}

main().catch(console.error);
