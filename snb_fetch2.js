// 补抓新三板行情 - 使用不同API
const https = require('https');

async function fetchSina(code) {
  return new Promise((resolve, reject) => {
    const fullCode = 'bj' + code;
    const url = `https://hq.sinajs.cn/list=${fullCode}`;
    https.get(url, { headers: { 
      'User-Agent': 'Mozilla/5.0',
      'Referer': 'https://finance.sina.com.cn'
    }}, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          // 格式: var hq_bj831330="名称,现价,涨跌,涨跌幅,昨收,..."
          const match = data.match(/"([^"]+)"/);
          if (!match) return reject(new Error('No data'));
          const fields = match[1].split(',');
          if (fields.length < 10) return reject(new Error('Invalid'));
          const price = parseFloat(fields[1]);
          const prevClose = parseFloat(fields[4]);
          const changePct = prevClose > 0 ? ((price - prevClose) / prevClose * 100).toFixed(2) : '0.00';
          resolve({ price: price.toFixed(3), change: changePct });
          console.log(`  raw: ${match[1]}`);
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
      const r = await fetchSina(code);
      console.log(`${code}: price=${r.price}, change=${r.change}%`);
    } catch (e) {
      console.log(`${code}: failed - ${e.message}`);
    }
    await new Promise(r => setTimeout(r, 1000));
  }
}

main().catch(console.error);
