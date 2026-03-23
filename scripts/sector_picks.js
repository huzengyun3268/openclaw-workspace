const https = require('https');
const iconv = require('iconv-lite');
function req(url, headers) {
  return new Promise((resolve) => {
    const r = https.get(url, {headers: headers}, res => {
      const chunks = []; res.on('data', c => chunks.push(c));
      res.on('end', () => resolve(iconv.decode(Buffer.concat(chunks), 'gbk')));
    });
    r.on('error', () => resolve(null));
  });
}
async function main() {
  const h = {'User-Agent':'Mozilla/5.0','Referer':'https://finance.sina.com.cn/'};
  // 光模块/光纤接入
  const opt = 'sz300308,sz300502,sh600353,sz300548,sh603083,sh002281';
  // 军工龙头
  const mil = 'sh600760,sh600893,sz000733,sh600435,sz000768,sh600316';
  // 半导体龙头
  const semi = 'sz002371,sh688981,sh603501,sh688008,sh600584,sh688396';

  function parse(raw) {
    const results = [];
    for (const line of raw.trim().split('\n')) {
      const m = line.match(/hq_str_(\w+)="([^"]+)"/);
      if (!m) continue;
      const p = m[2].split(',');
      const price = parseFloat(p[3]);
      const prev = parseFloat(p[2]);
      const pct = parseFloat(((price - prev) / prev * 100).toFixed(2));
      const high = parseFloat(p[4]);
      const low = parseFloat(p[5]);
      const vol = (parseFloat(p[8]) / 10000).toFixed(1);
      const amt = (parseFloat(p[9]) / 100000000).toFixed(2);
      results.push({code: m[1], name: p[0], price, pct, high, low, vol, amt});
    }
    return results;
  }

  const [r1,r2,r3] = await Promise.all([req('https://hq.sinajs.cn/list=' + opt, h), req('https://hq.sinajs.cn/list=' + mil, h), req('https://hq.sinajs.cn/list=' + semi, h)]);

  const sectors = [
    ['通信/光模块', parse(r1)],
    ['军工', parse(r2)],
    ['半导体', parse(r3)]
  ];

  for (const [sname, stocks] of sectors) {
    console.log('\n=== ' + sname + ' ===');
    for (const s of stocks.sort((a,b) => b.pct - a.pct)) {
      const flag = s.pct > 2 ? 'UP+' : s.pct > 0 ? 'UP' : s.pct < -2 ? 'DOWN' : 'DN';
      console.log(flag + ' ' + s.name + '(' + s.code + '): ' + s.price.toFixed(2) + ' (' + (s.pct>0?'+':'') + s.pct.toFixed(2) + '%)  high=' + s.high.toFixed(2) + ' low=' + s.low.toFixed(2) + ' amt=' + s.amt + '亿');
    }
  }
}
main();
