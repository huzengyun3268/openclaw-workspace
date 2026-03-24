const http = require('http');
const iconv = require('iconv-lite');

const indices = {
  's_sh000001': '上证指数',
  's_sz399001': '深证成指',
  's_sz399006': '创业板指',
  's_sh000300': '沪深300'
};

const stocks = {
  'sh600352': '浙江龙盛',
  'sh600089': '特变电工',
  'sh300033': '同花顺',
  'bj920046': '亿能电力',
  'sh831330': '普适导航',
  'sh430046': '圣博润'
};

function fetch(path, callback) {
  const options = { hostname: 'hq.sinajs.cn', path, headers: { 'Referer': 'http://finance.sina.com.cn' } };
  http.get(options, res => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => callback(iconv.decode(Buffer.from(data), 'GBK')));
  }).on('error', e => callback(''));
}

fetch('/list=' + Object.keys(indices).join(','), body => {
  const lines = body.trim().split('\n');
  console.log('=== 指数 ===');
  lines.forEach(line => {
    const m = line.match(/\"([^\"]+)\"/);
    if (m) {
      const f = m[1].split(',');
      if (f[1]) {
        const name = f[0];
        const price = parseFloat(f[1]).toFixed(2);
        const pct = parseFloat(f[3]).toFixed(2);
        const arrow = pct >= 0 ? '+' : '';
        console.log(`${name}: ${price} (${arrow}${pct}%)`);
      }
    }
  });
});

fetch('/list=' + Object.keys(stocks).join(','), body => {
  const lines = body.trim().split('\n');
  console.log('\n=== 持仓 ===');
  lines.forEach(line => {
    const m = line.match(/\"([^\"]+)\"/);
    if (m) {
      const f = m[1].split(',');
      if (f[1] && f[1] !== '0.000') {
        const name = f[0];
        const price = parseFloat(f[1]).toFixed(3);
        const pct = parseFloat(f[3]).toFixed(2);
        const arrow = pct >= 0 ? '+' : '';
        const color = pct > 0 ? '🟢' : pct < 0 ? '🔴' : '🟡';
        console.log(`${color} ${name}: ${price} (${arrow}${pct}%)`);
      }
    }
  });
});
