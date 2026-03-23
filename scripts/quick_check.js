const https = require('https');
const iconv = require('iconv-lite');
function req(url, h) {
  return new Promise((resolve) => {
    const r = https.get(url, {headers: h}, res => {
      const chunks = []; res.on('data', c => chunks.push(c));
      res.on('end', () => resolve(iconv.decode(Buffer.concat(chunks), 'gbk')));
    });
    r.on('error', () => resolve(null));
  });
}
async function main() {
  const h = {'User-Agent':'Mozilla/5.0','Referer':'https://finance.sina.com.cn/'};
  const r = await req('https://hq.sinajs.cn/list=sh600352,sh600089,bj920046', h);
  for (const line of r.trim().split('\n')) {
    const m = line.match(/hq_str_(\w+)="([^"]+)"/);
    if (!m) continue;
    const p = m[2].split(',');
    const price = parseFloat(p[3]);
    const prev = parseFloat(p[2]);
    const pct = ((price - prev) / prev * 100);
    const high = parseFloat(p[4]);
    const low = parseFloat(p[5]);
    const flag = pct > 2 ? 'UP+' : pct > 0 ? 'UP' : pct < -1 ? 'DOWN' : 'DN';
    console.log(flag + ' | ' + p[0] + '(' + m[1] + '): ' + price.toFixed(2) + ' (' + (pct>0?'+':'') + pct.toFixed(2) + '%)  H=' + high.toFixed(2) + ' L=' + low.toFixed(2));
  }
}
main();
