const http = require('http');

function fetch(url) {
  return new Promise((resolve, reject) => {
    http.get(url, { headers: { 
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
      'Referer': 'https://quote.eastmoney.com/'
    } }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

async function main() {
  const stocks = [
    { name: '普适导航', code: '831330', secid: '0.831330', shares: 6370, cost: 20.415 },
    { name: '圣博润', code: '430046', secid: '0.430046', shares: 10334, cost: 0.478 },
  ];

  for (const s of stocks) {
    try {
      const url = `http://push2.eastmoney.com/api/qt/stock/get?secid=${s.secid}&fields=f43,f44,f45,f46,f47,f48,f57,f58,f107,f169,f170,f171&fltt=2&invt=2`;
      const raw = await fetch(url);
      const data = JSON.parse(raw);
      console.log(`${s.name}:`, JSON.stringify(data).substring(0, 300));
      if (data.data) {
        const price = data.data.f43 / 100;
        const prevClose = data.data.f44 / 100;
        const pct = ((price - prevClose) / prevClose * 100).toFixed(2);
        const pnl = ((price - s.cost) * s.shares).toFixed(2);
        const pnlPct = ((price - s.cost) / s.cost * 100).toFixed(2);
        console.log(`${s.name}|${s.code}|${price}|${pct}|${pnl}|${pnlPct}`);
      }
    } catch(e) {
      console.log(`${s.name}: ERROR ${e.message}`);
    }
  }
}

main().catch(console.error);
