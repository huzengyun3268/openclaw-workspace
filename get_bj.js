const http = require('http');

function fetchStock(code, prefix) {
  return new Promise((resolve) => {
    const options = {
      hostname: 'hq.sinajs.cn',
      path: '/list=' + prefix + code,
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://finance.sina.com.cn/'
      }
    };
    http.get(options, (res) => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => {
        try {
          const m = d.match(/"([^"]+)"/);
          if (m) {
            const parts = m[1].split(',');
            const price = parseFloat(parts[3]);
            const prevClose = parseFloat(parts[2]);
            const chgPct = prevClose > 0 ? ((price - prevClose) / prevClose * 100).toFixed(2) : '0.00';
            resolve({ code, name: parts[0], price, prevClose, changePct: chgPct });
          } else {
            resolve({ code, error: 'no match', raw: d.substring(0, 200) });
          }
        } catch(e) {
          resolve({ code, error: e.message, raw: d.substring(0, 200) });
        }
      });
    }).on('error', e => resolve({ code, error: e.message }));
  });
}

async function main() {
  const results = await Promise.all([
    fetchStock('831330', 'sz'),  // 普适导航
    fetchStock('430046', 'bj'),  // 圣博润
  ]);
  console.log(JSON.stringify(results));
}
main().catch(console.error);
