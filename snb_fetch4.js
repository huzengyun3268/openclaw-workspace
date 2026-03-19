// 补抓新三板行情 - 使用eastmoney标准接口
const https = require('https');

async function fetchEM(code) {
  return new Promise((resolve, reject) => {
    const secid = '0.' + code;
    const url = `https://push2.eastmoney.com/api/qt/stock/get?ut=fa5fd1943c7b386f172d6893dbfba10b&fields=f43,f44,f45,f46,f47,f48,f57,f58,f107,f169,f170&secid=${secid}&_=1`;
    
    https.get(url, { headers: { 
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
      'Referer': 'https://quote.eastmoney.com/'
    }}, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          const d = json.data;
          if (!d) return reject(new Error('No data'));
          // f43=最新价, f57=昨收, f170=涨跌幅(万分制)
          const price = parseFloat(d.f43) / 100; // eastmoney价格单位是分
          const prevClose = parseFloat(d.f57) / 100;
          const changePct = d.f170 ? (parseFloat(d.f170) / 100).toFixed(2) : (prevClose > 0 ? ((price - prevClose) / prevClose * 100).toFixed(2) : '0.00');
          console.log(`  raw f43=${d.f43}, f57=${d.f57}, f170=${d.f170}`);
          resolve({ price: price.toFixed(3), change: changePct });
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
      const r = await fetchEM(code);
      console.log(`${code}: price=${r.price}, change=${r.change}%`);
    } catch (e) {
      console.log(`${code}: failed - ${e.message}`);
    }
    await new Promise(r => setTimeout(r, 1000));
  }
}

main().catch(console.error);
