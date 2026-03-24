// 逆势走强股票扫描 - 获取ETF成分股及行业龙头
const http = require('http');

// 按行业扫描强势股
const sectors = [
  // 通信5G
  { name: '通信设备', codes: 'sh600487,sh600498,sh600776,sh601728,sh603236,sh002463' },
  // 芯片半导体
  { name: '半导体', codes: 'sh688981,sh688008,sh603986,sh002371,sh600584,sh688396' },
  // 有色金属
  { name: '有色金属', codes: 'sh601600,sh600456,sh000630,sh601168,sh000878,sh600547' },
  // 军工
  { name: '军工', codes: 'sh601989,sh600150,sh600760,sh002013,sh600893,sh600184' },
];

const allCodes = sectors.map(s => s.codes).join(',');

const options = { hostname: 'hq.sinajs.cn', path: '/list=' + allCodes, headers: { 'Referer': 'http://finance.sina.com.cn', 'User-Agent': 'Mozilla/5.0' } };

http.get(options, res => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    const iconv = require('iconv-lite');
    const str = iconv.decode(Buffer.from(data), 'GBK');
    const lines = str.trim().split('\n');
    
    const results = [];
    lines.forEach(line => {
      const idx = line.indexOf('="');
      if (idx > 0) {
        const code = line.substring(8, idx);
        const content = line.substring(idx + 2, line.length - 2);
        const f = content.split(',');
        if (f[1] && f[1] !== '0.000' && f[1] !== '-') {
          const name = f[0];
          const price = f[1];
          const pct = parseFloat(f[3]);
          const vol = parseInt(f[8]) || 0;
          const amount = parseInt(f[9]) || 0;
          if (vol > 0 || amount > 0) {
            results.push({ code, name, price: parseFloat(price), pct, vol, amount });
          }
        }
      }
    });

    if (results.length === 0) {
      console.log('数据未更新，等待09:30，当前时间: ' + new Date().toLocaleTimeString());
      return;
    }

    // 按涨跌幅排序
    results.sort((a, b) => b.pct - a.pct);

    console.log('=== 逆势走强股票（按强弱排序）===\n');
    results.forEach((s, i) => {
      const arrow = s.pct >= 0 ? '+' : '';
      const color = s.pct > 2 ? '🟢🟢' : s.pct > 0 ? '🟢' : s.pct < -2 ? '🔴🔴' : '🔴';
      const time = new Date().toLocaleTimeString();
      console.log((i + 1) + '. ' + color + ' ' + s.name + '(' + s.code + ') | 现价:' + s.price + ' | ' + arrow + s.pct.toFixed(2) + '%');
    });
    console.log('\n时间: ' + new Date().toLocaleTimeString());
  });
}).on('error', e => console.log('Error: ' + e.message));
