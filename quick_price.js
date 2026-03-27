const http = require('http');

function fetchStock(code) {
  return new Promise((resolve) => {
    const options = {
      hostname: 'qt.gtimg.cn',
      path: '/q=' + code,
      headers: {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://gu.qq.com/'
      }
    };
    http.get(options, (res) => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => {
        try {
          const parts = d.split('~');
          if (parts && parts.length > 10 && parts[3]) {
            const price = parseFloat(parts[3]);
            const prevClose = parseFloat(parts[4]);
            const chgPct = prevClose > 0 ? ((price - prevClose) / prevClose * 100).toFixed(2) : '0.00';
            const name = parts[1];
            resolve({ code, name, price, prevClose, changePct: chgPct });
          } else {
            resolve({ code, error: 'empty', raw: d.substring(0, 100) });
          }
        } catch(e) {
          resolve({ code, error: e.message });
        }
      });
    }).on('error', e => resolve({ code, error: e.message }));
  });
}

async function main() {
  const codes = ['sz831330', 'bj430046', 'sh600352', 'sh600893', 'sz300033', 'sh601168', 'sh600487', 'sh688295', 'sh920046', 'sh600114', 'sz301638', 'sh600089'];
  const results = await Promise.all(codes.map(c => fetchStock(c)));
  console.log(JSON.stringify(results, null, 2));
}
main().catch(console.error);
