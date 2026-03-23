const http = require('http');
const iconv = require('iconv-lite');

const stocks = [
  {code: 'sh600352', name: '浙江龙盛'},
  {code: 'sh600089', name: '特变电工'},
  {code: 'sh603248', name: '锡华科技'},
  {code: 'sz300033', name: '同花顺'},
  {code: 'sz300189', name: '神农种业'},
  {code: 'bj831330', name: '普适导航'},
  {code: 'sz430046', name: '圣博润'},
  {code: 'bj920046', name: '亿能电力'},
  {code: 'sh600114', name: '东睦股份(老婆)'},
  {code: 'sz301638', name: '南网数字(老婆)'},
];

const list = stocks.map(s => s.code).join(',');
const url = 'http://hq.sinajs.cn/list=' + list;

http.get(url, {headers: {'Referer': 'http://finance.sina.com.cn', 'User-Agent': 'Mozilla/5.0'}}, (res) => {
  const chunks = [];
  res.on('data', c => chunks.push(c));
  res.on('end', () => {
    const buf = Buffer.concat(chunks);
    const str = iconv.decode(buf, 'GBK');
    const lines = str.trim().split('\n');
    for (const line of lines) {
      const m = line.match(/="([^"]+)"/);
      if (!m) continue;
      const parts = m[1].split(',');
      if (parts.length < 10) continue;
      const code = line.match(/sh600352|sh600089|sh603248|sz300033|sz300189|bj831330|sz430046|bj920046|sh600114|sz301638/)?.[0];
      const info = stocks.find(s => s.code === code);
      const name = info ? info.name : parts[0];
      const price = parseFloat(parts[3]);
      const prev = parseFloat(parts[2]);
      const chg = ((price - prev) / prev * 100).toFixed(2);
      const sign = price >= prev ? '+' : '';
      const time = parts[30] || parts[31] || '';
      console.log(name + ' (' + code + '): ' + price + ' (' + sign + chg + '%)  [' + time + ']');
    }
  });
}).on('error', e => console.error(e.message));
