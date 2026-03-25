const https = require('https');
const codes = ['sh600352','sh300033','sh688295','sh600487','sh601168','sh600893','sh600089','sh300499','bj920046','sh600114','sz301638'];
const url = 'http://hq.sinajs.cn/list=' + codes.join(',');
https.get(url, {headers: {'Referer':'http://finance.sina.com.cn','User-Agent':'Mozilla/5.0'}}, (res) => {
  let data = '';
  res.on('data', d => data += d);
  res.on('end', () => {
    const lines = data.split('\n');
    for(const line of lines) {
      const m = line.match(/"([^"]+)"/);
      if(m) {
        const parts = m[1].split(',');
        if(parts.length > 3) {
          const name = parts[0];
          const price = parseFloat(parts[3]).toFixed(2);
          const prev = parseFloat(parts[2]).toFixed(2);
          const pct = ((price - prev) / prev * 100).toFixed(2);
          console.log(name + ': ' + price + ' (' + (pct>=0?'+':'') + pct + '%)');
        }
      }
    }
  });
}).on('error', e => console.error(e));
