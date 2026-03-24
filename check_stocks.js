const http = require('http');
const iconv = require('iconv-lite');

const codes = [
  'sh600352',  // 浙江龙盛
  'sh600089',  // 特变电工
  'sh300033',  // 同花顺
  'bj920046',  // 亿能电力
  'sh831330',  // 普适导航
  'sh430046'   // 圣博润
];

const path = '/list=' + codes.join(',');
const options = { hostname: 'hq.sinajs.cn', path, headers: { 'Referer': 'http://finance.sina.com.cn', 'User-Agent': 'Mozilla/5.0' } };

http.get(options, res => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    const buf = Buffer.from(data);
    const str = iconv.decode(buf, 'GBK');
    const lines = str.trim().split('\n');
    let found = false;
    lines.forEach(line => {
      const idx = line.indexOf('="');
      if (idx > 0) {
        const code = line.substring(8, idx);
        const content = line.substring(idx + 2, line.length - 2);
        const fields = content.split(',');
        if (fields[1] && fields[1] !== '0.000' && fields[1] !== '-') {
          const name = fields[0];
          const price = fields[1];
          const pct = parseFloat(fields[3]).toFixed(2);
          const high = fields[4];
          const low = fields[5];
          const open = fields[6];
          const prev = fields[2];
          const time = (fields[30] || '') + ' ' + (fields[31] || '');
          const arrow = pct >= 0 ? '+' : '';
          const color = pct > 0 ? '🟢' : pct < 0 ? '🔴' : '🟡';
          console.log(color + ' ' + name + '(' + code + ') | 现价:' + price + ' | ' + arrow + pct + '% | 开:' + open + ' | 高:' + high + ' | 低:' + low + ' | ' + time);
          found = true;
        }
      }
    });
    if (!found) {
      console.log('数据未更新，等待09:30开盘，当前时间: ' + new Date().toLocaleTimeString());
    }
  });
}).on('error', e => console.log('Error: ' + e.message));
