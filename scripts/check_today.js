const http = require('http');
const stocks = [
  'sh600352', // 浙江龙盛
  'sh600089', // 特变电工
  'sh300033', // 同花顺
  'bj920046', // 亿能电力
  'sh831330', // 普适导航
  'sh430046', // 圣博润
  'sh688295', // 中复神鹰
  'sh600114', // 东睦股份
  'sh301638', // 南网数字
];
const url = 'http://hq.sinajs.cn/list=' + stocks.join(',');
http.get(url, {headers: {'Referer':'http://finance.sina.com.cn', 'User-Agent':'Mozilla/5.0'}}, (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    const lines = data.split('\n');
    lines.forEach(line => {
      const m = line.match(/"([^"]+)"/);
      if (m) {
        const parts = m[1].split(',');
        if (parts.length >= 4) {
          const name = parts[0];
          const cur = parseFloat(parts[3]);
          const close = parseFloat(parts[2]);
          const pct = ((cur - close) / close * 100).toFixed(2);
          const open = parseFloat(parts[1]);
          const high = parseFloat(parts[4]);
          const low = parseFloat(parts[5]);
          console.log(name + ': ' + cur + ' (' + pct + '%) 开盘=' + open + ' H=' + high + ' L=' + low + ' 昨收=' + close);
        }
      }
    });
  });
}).on('error', e => console.error(e));
