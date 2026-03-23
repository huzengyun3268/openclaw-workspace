const https = require('https');

function fetch(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0', 'Referer': 'https://finance.sina.com.cn' } }, (res) => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => resolve(d));
    }).on('error', reject);
  });
}

async function test() {
  // 试新浪API
  console.log('=== 新浪API测试 ===');
  const r1 = await fetch('https://hq.sinajs.cn/list=sh600352');
  console.log('新浪:', r1.substring(0, 150));

  // 试东方财富API
  console.log('\n=== 东方财富API测试 ===');
  const r2 = await fetch('https://push2.eastmoney.com/api/qt/stock/get?secid=1.600352&fields=f43,f170&ut=fa5fd1943c7b386f172d6893dbfba10b');
  console.log('东财:', r2.substring(0, 200));
}

test().catch(console.error);
