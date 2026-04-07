const https = require('https');
const fs = require('fs');

const codes = ['sh600352','sz300033','sh600487','sh600893','sh601168','sh518880','sz430046','sh600114','sh600089'];

function getStock(code) {
  return new Promise((resolve) => {
    https.get('https://qt.gtimg.cn/q=' + code, (res) => {
      let data = '';
      res.on('data', d => data += d);
      res.on('end', () => {
        fs.appendFileSync('C:\\Users\\Administrator\\.openclaw\\workspace\\debug_price.txt', code + ' || ' + data.substring(0, 300) + '\n\n', 'utf8');
        resolve();
      });
    }).on('error', () => resolve());
  });
}

(async () => {
  for (const c of codes) await getStock(c);
})();
