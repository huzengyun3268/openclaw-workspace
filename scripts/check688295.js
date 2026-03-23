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
  const r = await req('https://hq.sinajs.cn/list=sh688295,sh603248', h);
  const lines = r.trim().split('\n');
  for (const line of lines) {
    const m = line.match(/hq_str_(\w+)="([^"]+)"/);
    if (!m) continue;
    const p = m[2].split(',');
    // format: name,open,prevClose,price,high,low,close,vol,amount,bid,ask,...date,time
    const name = p[0];
    const open = parseFloat(p[1]);
    const prev = parseFloat(p[2]);
    const price = parseFloat(p[3]);
    const high = parseFloat(p[4]);
    const low = parseFloat(p[5]);
    const pct = parseFloat(p[3] ? (((price - prev) / prev * 100)).toFixed(2) : 0);
    const amt = (parseFloat(p[9]) / 100000000).toFixed(2);
    const flag = pct > 2 ? 'UP+' : pct > 0 ? 'UP' : pct < -2 ? 'DOWN' : 'DN';
    console.log(flag + ' | ' + name + ' (' + m[1] + ')');
    console.log('  Price: ' + price.toFixed(2) + ' (' + (pct>0?'+':'') + pct + '%)');
    console.log('  Open: ' + open + '  PrevClose: ' + prev);
    console.log('  High: ' + high + '  Low: ' + low);
    console.log('  Amount: ' + amt + '亿');
  }
}
main();
