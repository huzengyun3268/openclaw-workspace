const http = require('http');

// 强势行业个股 - 东方财富实时
const stocks = 'sh600487,sh600498,sh600776,sh601728,sh603236,sh002463,sh688981,sh688008,sh603986,sh002371,sh600584,sh688396,sh601600,sh600456,sh000630,sh601168,sh000878,sh600547,sh601989,sh600150,sh600760,sh002013,sh600893,sh600184';

const secids = stocks.split(',').map(c => {
  if (c.startsWith('sh6')) return '1.' + c.substring(2);
  if (c.startsWith('sz0')) return '0.' + c.substring(2);
  if (c.startsWith('sz3')) return '0.' + c.substring(2);
  return c;
}).join(',');

const url = '/api/qt/ulist.np/get?fltt=2&invt=2&fields=f1,f2,f3,f4,f12,f14,f15,f16,f17,f18&secids=' + secids + '&ut=fa5fd1943c7b386f172d6893dbfba10b';
const options = { hostname: 'push2.eastmoney.com', path: url, headers: { 'Referer': 'http://quote.eastmoney.com', 'User-Agent': 'Mozilla/5.0' } };

http.get(options, res => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    try {
      const d = JSON.parse(data);
      if (d.data && d.data.diff) {
        const results = d.data.diff.filter(s => s.f2 !== '-' && s.f3 !== '-');
        results.sort((a, b) => parseFloat(b.f3) - parseFloat(a.f3));
        console.log('=== 逆势走强股票 ===\n');
        results.forEach((s, i) => {
          const pct = parseFloat(s.f3);
          const arrow = pct >= 0 ? '+' : '';
          const color = pct > 2 ? '🟢🟢' : pct > 0 ? '🟢' : pct < -2 ? '🔴🔴' : '🔴';
          console.log((i+1) + '. ' + color + ' ' + s.f14 + '(' + s.f12 + ') | ' + s.f2 + ' | ' + arrow + pct + '% | 高:' + s.f15 + ' | 低:' + s.f16);
        });
        console.log('\n时间: ' + new Date().toLocaleTimeString());
      } else {
        console.log('无数据，当前时间: ' + new Date().toLocaleTimeString() + ' (A股09:30开盘)');
      }
    } catch(e) {
      console.log('解析失败: ' + e.message + ' 当前: ' + new Date().toLocaleTimeString());
    }
  });
}).on('error', e => console.log('Error: ' + e.message));
