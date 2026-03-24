const http = require('http');
const codes = ['sh600352','sh600089','sz300033','bj920046','sh688295','sh600487','sh600893','sh601168','sz300499','sh600114'];
const path = '/list=' + codes.join(',');
const options = { hostname: 'hq.sinajs.cn', path, headers: { 'Referer': 'http://finance.sina.com.cn' } };
http.get(options, res => {
  let data = '';
  res.on('data', c => data += c);
  res.on('end', () => {
    const iconv = require('iconv-lite');
    const str = iconv.decode(Buffer.from(data), 'GBK');
    const lines = str.trim().split('\n');
    lines.forEach(line => {
      const idx = line.indexOf('="');
      if (idx > 0) {
        const content = line.substring(idx+2, line.length-2);
        const f = content.split(',');
        if (f[1] && f[1] !== '0.000' && f[1] !== '-') {
          const pct = parseFloat(f[3]);
          const arrow = pct > 0 ? '▲' : pct < 0 ? '▼' : '—';
          console.log(arrow + ' ' + f[0] + ':' + f[1] + '(' + (pct>=0?'+':'') + pct.toFixed(2) + '%)');
        }
      }
    });
  });
}).on('error', e => console.log(e.message));
