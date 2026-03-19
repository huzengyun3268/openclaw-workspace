// 用日K线获取昨收价
const https = require('https');

async function fetchKLine(code) {
  return new Promise((resolve, reject) => {
    const secid = '0.' + code;
    // 获取最近5条日K线
    const url = `https://push2his.eastmoney.com/api/qt/stock/kline/get?ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&klt=101&fqt=1&secid=${secid}&beg=20260301&end=20500101&smplmt=5&lmt=5&_=1`;
    
    https.get(url, { headers: { 
      'User-Agent': 'Mozilla/5.0',
      'Referer': 'https://quote.eastmoney.com/'
    }}, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          console.log(`  ${code}: kline = ${JSON.stringify(json).substring(0, 500)}`);
          resolve(json);
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
      const r = await fetchKLine(code);
      if (r.data && r.data.klines && r.data.klines.length > 0) {
        // 取最新一条K线
        const last = r.data.klines[r.data.klines.length - 1];
        const fields = last.split(',');
        // f56=开, f57=高, f58=低, f59=收, f60=成交量
        const close = parseFloat(fields[6]); // 收盘
        console.log(`  last kline: open=${fields[5]}, close=${close}`);
        
        // 再取前一条K线
        if (r.data.klines.length > 1) {
          const prev = r.data.klines[r.data.klines.length - 2];
          const prevFields = prev.split(',');
          const prevClose = parseFloat(prevFields[6]);
          const changePct = prevClose > 0 ? ((close - prevClose) / prevClose * 100).toFixed(2) : '0.00';
          console.log(`  prev kline: close=${prevClose}, change=${changePct}%`);
        }
      }
    } catch (e) {
      console.log(`${code}: failed - ${e.message}`);
    }
    await new Promise(r => setTimeout(r, 1000));
  }
}

main().catch(console.error);
