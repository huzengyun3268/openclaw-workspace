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
  // Try different codes for 亿能电力
  const codes = 'bj920046,sh920046,sz920046,920046,bj830800'.split(',');
  for (const code of codes) {
    const r = await req('https://hq.sinajs.cn/list=' + code, h);
    if (r && r.includes('"')) {
      const m = r.match(/hq_str_\w+="([^"]+)"/);
      if (m) {
        const p = m[1].split(',');
        if (p.length > 3) {
          const price = parseFloat(p[3]);
          const prev = parseFloat(p[2]);
          const pct = ((price - prev) / prev * 100);
          const amt = (parseFloat(p[9]) / 100000000).toFixed(2);
          console.log('CODE=' + code + ' NAME=' + p[0] + ' price=' + price.toFixed(2) + ' pct=' + pct.toFixed(2) + '% amt=' + amt + '亿');
        }
      }
    } else {
      console.log('CODE=' + code + ' NODATA');
    }
    await new Promise(r => setTimeout(r, 200));
  }
}
main();
