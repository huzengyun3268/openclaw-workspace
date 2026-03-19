// 补抓新三板行情
const https = require('https');

async function fetchEM(code) {
  return new Promise((resolve, reject) => {
    // 新三板用不同接口
    let url;
    if (code === '831330') {
      // 普适导航 - 新三板
      url = `https://push2.eastmoney.com/api/qt/stock/get?ut=fa5fd1943c7b386f172d6893dbfba10b&fields=f43,f44,f45,f46,f47,f48,f57,f58&secid=0.831330&_=1700000000000`;
    } else if (code === '430046') {
      // 圣博润 - 新三板
      url = `https://push2.eastmoney.com/api/qt/stock/get?ut=fa5fd1943c7b386f172d6893dbfba10b&fields=f43,f44,f45,f46,f47,f48,f57,f58&secid=0.430046&_=1700000000000`;
    } else {
      return reject(new Error('Unknown'));
    }
    
    https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0', 'Referer': 'https://quote.eastmoney.com/' } }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          const d = json.data;
          if (!d) return reject(new Error('No data'));
          // f43=最新价, f44=最高, f45=最低, f46=今开, f57=昨收
          const price = parseFloat(d.f43) / 100;
          const prevClose = parseFloat(d.f57) / 100;
          const changePct = prevClose > 0 ? ((price - prevClose) / prevClose * 100).toFixed(2) : '0.00';
          resolve({ price: price.toFixed(3), change: changePct });
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

async function main() {
  const results = {};
  for (const code of ['831330', '430046']) {
    try {
      const r = await fetchEM(code);
      results[code] = r;
      console.log(`${code}: price=${r.price}, change=${r.change}%`);
    } catch (e) {
      results[code] = null;
      console.log(`${code}: failed - ${e.message}`);
    }
    await new Promise(r => setTimeout(r, 500));
  }
  require('fs').writeFileSync('snb_report.txt', JSON.stringify(results), 'utf8');
}

main().catch(console.error);
